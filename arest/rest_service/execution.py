from arest.constants import METHODS
from ..core import aria
from . import handler_base


class Execution(handler_base.HandlerBase):
    mapper = {
        METHODS.POST: 'start',
        METHODS.GET: 'get',
    }
    def start(self, request):
        "Handle both uploading and retrieval of service template "
        return self._to_string(
            aria.execute_workflow(**dict(request.form.items())))

    def get(self, request):
        execution_id = request.args.get('id')
        return self._to_string(aria.model.execution.get(execution_id))

handler = Execution()
