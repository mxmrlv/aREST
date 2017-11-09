
from ..constants import METHODS
from ..core import aria
from . import handler_base


class Log(handler_base.AbstractHandler):

    __endpoint__ = 'log'
    __mapper__ = {
        METHODS.GET: 'get',
    }

    @staticmethod
    def get(request):
        import pydevd; pydevd.settrace('localhost', suspend=False)
        task_id = request.args.get('id')
        if task_id:
            return aria.model.log.get(task_id)
        execution_id = request.args.get('execution_id')
        if execution_id:
            return aria.model.log.list(filters={'execution_fk':execution_id})


handler = Log()
