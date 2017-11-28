from arest.constants import METHODS
from . aria_interface import interface
from . import handler_base


class Execution(handler_base.BaseHandler):
    __endpoint__ = 'execution'
    __mapper__ = {METHODS.POST: 'start', METHODS.GET: 'get'}

    @staticmethod
    def start(request):
        "Handle both uploading and retrieval of service template "
        return interface.execute_workflow(**dict(request.form.items()))

    @staticmethod
    def get(request):
        execution_id = request.args.get('id')
        return interface.model.execution.get(execution_id)


handler = Execution()
