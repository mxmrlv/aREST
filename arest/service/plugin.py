from ..constants import METHODS
from . aria_interface import interface
from . import handler_base


class Plugin(handler_base.BaseHandler):
    __endpoint__ = 'plugin'
    __mapper__ = {METHODS.PUT: 'install', METHODS.GET: 'get'}

    @staticmethod
    def install(request):
        "Handle both uploading and retrieval of service template "
        return interface.install_plugin(**dict(request.form.items()))

    @staticmethod
    def get(request):
        plugin_id = request.args.get('id')
        return interface.model.plugin.get(plugin_id)


handler = Plugin()
