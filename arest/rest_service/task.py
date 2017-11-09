
from ..constants import METHODS
from ..core import aria
from . import handler_base


class Task(handler_base.AbstractHandler):

    __endpoint__ = 'task'
    __mapper__ = {
        METHODS.GET: 'get',
    }

    @staticmethod
    def get(request):
        task_id = request.args.get('id')
        if task_id:
            return aria.model.task.get(task_id)
        execution_id = request.args.get('execution_id')
        if execution_id:
            return aria.model.task.list(filters={'execution_fk':execution_id})


handler = Task()
