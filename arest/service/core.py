import pickle

from ..constants import METHODS
from . aria_interface import interface
from . import handler_base


class Core(handler_base.BaseHandler):
    __endpoint__ = ('core', 'core/<path:path>')
    __mapper__ = {METHODS.PATCH: 'update', METHODS.GET: 'get', METHODS.PUT: 'put'}

    def get(self, path, request):
        entity_name, entity_path = self._split_path(path)
        entity_handler = getattr(interface.model, entity_name)
        if entity_path:
            entity_id, attribute_path = self._split_path(entity_path)
            entity = entity_handler.get(entity_id)
            return self._traverse_entity(entity, attribute_path)

        return entity_handler.list(**request.json)

    def update(self, path, request):
        entity_name, entity_path = self._split_path(path)
        entity_handler = getattr(interface.model, entity_name)
        entity_id, attribute_path = self._split_path(entity_path)
        entity = self._traverse_entity(entity_handler.get(entity_id), attribute_path)

        updated_entity = pickle.loads(request.data)

        for key in updated_entity._sa_instance_state.committed_state:
            setattr(entity, key, getattr(updated_entity, key))

        entity_handler.update(entity)

        return entity

    def put(self, path, request):
        entity_name, _ = self._split_path(path)
        entity_handler = getattr(interface.model, entity_name)
        return entity_handler.put(pickle.loads(request.data))

    def _respond(self, value):
        return pickle.dumps(value)


handler = Core()
