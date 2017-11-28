
from ..constants import METHODS
from . aria_interface import interface
from . import handler_base


class ServiceTemplate(handler_base.BaseHandler):

    __endpoint__ = 'service_template'
    __mapper__ = {METHODS.PUT: 'upload', METHODS.DELETE: 'delete', METHODS.GET: 'get'}

    @staticmethod
    def upload(request):
        return interface.create_service_template(**dict(request.form.items()))

    @staticmethod
    def delete(request):
        service_template_id = request.args.get('id')
        return interface.model.service_template.delete(service_template_id)

    @staticmethod
    def get(request):
        service_template_id = request.args.get('id')
        return interface.model.service_template.get(service_template_id)


handler = ServiceTemplate()
