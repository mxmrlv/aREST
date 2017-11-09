
from arest.core import aria

from . import handler_base
from ..constants import METHODS


class Service(handler_base.AbstractHandler):

    __endpoint__ = 'service'
    __mapper__ = {
        METHODS.POST: 'create',
        METHODS.GET: 'get',
        METHODS.DELETE: 'delete'
    }

    @staticmethod
    def create(request):
        return aria.create_service(**dict(request.form.items()))

    @staticmethod
    def get(request):
        service_id = request.args.get('id')
        return aria.model.service.get(service_id)

    @staticmethod
    def delete(request):
        service_id = request.args.get('id')
        return aria.model.service.delete(service_id)


handler = Service()
