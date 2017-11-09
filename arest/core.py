
import os
import errno

import aria as aria_
from aria import core as aria_core
from aria.orchestrator import (
    plugin,
    workflow_runner
)
from aria.storage import sql_mapi
from aria.storage import filesystem_rapi


class AriaCore():

    def __init__(self, root_dir=None):
        self._root_dir = root_dir or \
                         os.path.join(os.path.expanduser('~'), '.arest')

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

    def execute_workflow(self, **kwargs):
        wf_runner = workflow_runner.WorkflowRunner(
            self.model,
            self.resource,
            self._plugin_manager,
            **kwargs
        )

        wf_runner.execute()

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


aria = AriaCore()
