from arest.constants import METHODS
from ..core import aria
from . import handler_base


class Execution(handler_base.AbstractHandler):
    __endpoint__ = 'execution'
    __mapper__ = {
        METHODS.POST: 'start',
        METHODS.GET: 'get',
    }

    @staticmethod
    def start(request):
        "Handle both uploading and retrieval of service template "
        return aria.execute_workflow(**dict(request.form.items()))

    @staticmethod
    def get(request):
        execution_id = request.args.get('id')
        return aria.model.execution.get(execution_id)


handler = Execution()
