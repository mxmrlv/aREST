
from ..constants import METHODS
from ..core import aria
from . import handler_base



class ServiceTemplate(handler_base.HandlerBase):

    mapper = {
        METHODS.PUT: 'upload',
        METHODS.GET: 'get',
        METHODS.DELETE: 'delete'
    }

    def upload(self, request):
        "Handle both uploading and retrieval of service template "
        return self._to_string(
            aria.create_service_template(**dict(request.form.items())))

    def get(self, request):
        service_template_id = request.args.get('id')
        return self._to_string(aria.model.service_template.get(
            service_template_id))

    def delete(self, request):
        service_template_id = request.args.get('id')
        return self._to_string(
            aria.model.service_template.delete(service_template_id))

handler = ServiceTemplate()
