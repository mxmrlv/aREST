import json

from ..constants import METHODS
from ..core import aria
from . import handler_base


class Core(handler_base.AbstractHandler):

    __endpoint__ = 'query'
    __mapper__ = {
        METHODS.GET: 'get',
        METHODS.PATCH: 'update'
    }

    @staticmethod
    def get(request):
        entity = request.args.get('entity')
        type_ = request.args.get('type')
        filters = request.args.get('filters')
        id_ = request.args.get('id')
        kwargs = json.loads(request.form.get('kwargs', '{}'))

        entity_handler = getattr(aria.model, entity)
        if type_ == 'get':
            kwargs.setdefault('entry_id', id_)
        elif type_ == 'list':
            kwargs.setdefault('filters', filters)

        return getattr(entity_handler, type_)(**kwargs)

    @staticmethod
    def update(request):
        entity = request.args.get('entity')
        id_ = request.args.get('id')
        kwargs = json.loads(request.form.get('kwargs', '{}'))

        entity_handler = getattr(aria.model, entity)
        entity = entity_handler.get(id_)
        for key, value in kwargs.items():
            setattr(entity, key, value)
        entity_handler.update(entity)

        return entity_handler.get(id_)


handler = Core()
