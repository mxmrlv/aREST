

from ..constants import METHODS
from . aria_interface import interface
from . import handler_base


class Service(handler_base.BaseHandler):

    __endpoint__ = 'service'
    __mapper__ = {METHODS.POST: 'create', METHODS.DELETE: 'delete', METHODS.GET: 'get'}

    @staticmethod
    def create(request):
        return interface.create_service(**dict(request.form.items()))

    @staticmethod
    def delete(request):
        service_id = request.args.get('id')
        return interface.model.service.delete(service_id)

    @staticmethod
    def get(request):
        service_id = request.args.get('id')
        return interface.model.service.get(service_id)


handler = Service()
