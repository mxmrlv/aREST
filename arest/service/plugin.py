from ..core import aria
from ..constants import METHODS
from . import handler_base


class Plugin(handler_base.AbstractHandler):
    __endpoint__ = 'plugin'
    __mapper__ = {
        METHODS.PUT: 'install',
        METHODS.GET: 'get',
    }

    @staticmethod
    def install(request):
        "Handle both uploading and retrieval of service template "
        return aria.install_plugin(**dict(request.form.items()))

    @staticmethod
    def get(request):
        plugin_id = request.args.get('id')
        return aria.model.plugin.get(plugin_id)


handler = Plugin()
