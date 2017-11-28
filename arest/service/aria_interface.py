
import os
import errno

import aria as aria_
from aria import core as aria_core
from aria.orchestrator import plugin, execution_preparer
from aria.orchestrator.context.workflow import WorkflowContext
from aria.orchestrator.workflows.core import engine
from aria.orchestrator.workflows.executor.process import ProcessExecutor
from aria.storage import sql_mapi, ModelStorage
from aria.storage import filesystem_rapi


class AriaCore():

    def __init__(self, root_dir=None):
        self._root_dir = root_dir or \
                         os.path.join(os.path.expanduser('~'), '.aria')

        models_dir = os.path.join(self._root_dir, 'models')
        resource_dir = os.path.join(self._root_dir, 'resources')
        plugins_dir = os.path.join(self._root_dir, 'plugins')
        self._create_paths(models_dir, resource_dir, plugins_dir)

        # Create a model storage
        self._model_storage = aria_.application_model_storage(
            api=sql_mapi.SQLAlchemyModelAPI,
            initiator_kwargs={'base_dir': models_dir}
        )

        self._resource_storage = aria_.application_resource_storage(
            api=filesystem_rapi.FileSystemResourceAPI,
            api_kwargs={'directory': resource_dir}
        )

        self._plugin_manager = plugin.PluginManager(
            model=self._model_storage,
            plugins_dir=plugins_dir
        )

        self._core = aria_core.Core(
            model_storage=self.model,
            resource_storage=self.resource,
            plugin_manager=self._plugin_manager
        )

    @property
    def model(self):
        return self._model_storage

    @property
    def resource(self):
        return self._resource_storage

    def install_plugin(self, source):
        self._plugin_manager.validate_plugin(source)
        self._plugin_manager.install(source)

    def create_service_template(self, path, name):
        aria_.install_aria_extensions()
        self._core.create_service_template(path, os.path.dirname(path), name)
        return str(self.model.service_template.get_by_name(name).id)

    def create_service(self, *args, **kwargs):
        aria_.install_aria_extensions()
        kwargs.setdefault('inputs', {})
        self._core.create_service(*args, **kwargs)

    def execute_workflow(self, service_id, workflow_name, **kwargs):
        ctx = self._create_execution(service_id, workflow_name, **kwargs)

        # Create a mapi based executor
        ctx = WorkflowContext(
            name=ctx.workflow_name,
            model_storage=self._get_rest_mapi(),
            resource_storage=ctx.resource,
            service_id=service_id,
            execution_id=ctx.execution.id,
            workflow_name=ctx.workflow_name,
            task_max_attempts=ctx._task_max_attempts,
            task_retry_interval=ctx._task_retry_interval,
        )

        engine.Engine(ProcessExecutor()).execute(ctx)

    @staticmethod
    def _get_rest_mapi():
        from aria.rest_mapi.core import RESTClient
        from aria.modeling import models

        return ModelStorage(
            api_cls=RESTClient,
            items=models.models_to_register,
            initiator=False

        )

    def _create_execution(self, service_id, workflow_name, **kwargs):
        exec_inputs = kwargs.pop('inputs', None)
        return execution_preparer.ExecutionPreparer(
            self.model,
            self.resource,
            self._plugin_manager,
            self.model.service.get(service_id),
            workflow_name,
            **kwargs
        ).prepare(execution_inputs=exec_inputs)

    def delete_service(self, *args, **kwargs):
        self._core.delete_service(*args, **kwargs)

    def delete_service_template(self, *args, **kwargs):
        self._core.delete_service_template(*args, **kwargs)

    @staticmethod
    def _create_paths(*paths):
        existing_paths = []
        for path in paths:
            try:
                os.makedirs(path)
                existing_paths += path
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
                else:
                    existing_paths += path
        return existing_paths


interface = AriaCore()

if __name__ == '__main__':
    interface.execute_workflow(1, 'install')