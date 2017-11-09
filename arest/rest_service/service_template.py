
from ..constants import METHODS
from ..core import aria
from . import handler_base


class ServiceTemplate(handler_base.AbstractHandler):

    __endpoint__ = 'service_template'
    __mapper__ = {
        METHODS.PUT: 'upload',
        METHODS.GET: 'get',
        METHODS.DELETE: 'delete'
    }

    @staticmethod
    def upload(request):
        return aria.create_service_template(**dict(request.form.items()))

    @staticmethod
    def get(request):
        service_template_id = request.args.get('id')
        return aria.model.service_template.get(service_template_id)

    @staticmethod
    def delete(request):
        service_template_id = request.args.get('id')
        return aria.model.service_template.delete(service_template_id)


handler = ServiceTemplate()
