
from arest.core import aria

from . import handler_base
from ..constants import METHODS


class Service(handler_base.HandlerBase):

    mapper = {
        METHODS.POST: 'create',
        METHODS.GET: 'get',
        METHODS.DELETE: 'delete'
    }

    def create(self, request):
        return self._to_string(aria.create_service(**dict(request.form.items())))

    def get(self, request):
        service_id = request.args.get('id')
        return self._to_string(aria.model.service.get(service_id))

    def delete(self, request):
        service_id = request.args.get('id')
        return self._to_string(aria.model.service.delete(service_id))


handler = Service()
