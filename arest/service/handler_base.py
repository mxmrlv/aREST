

from flask import request, jsonify
from aria.modeling.mixins import ModelMixin


class BaseHandler(object):
    __mapper__ = {}
    __endpoint__ = None

    def _respond(self, value):
        if isinstance(value, (list, tuple, set)):
            return tuple(self._respond(item) for item in value)
        elif isinstance(value, dict):
            return dict((k, self._respond(v)) for k, v in value.items())
        elif isinstance(value, ModelMixin):
            return value.to_dict()
        else:
            return value

    def __call__(self, *args, **kwargs):
        import pydevd; pydevd.settrace('localhost', suspend=False, port=55555)

        try:
            func_name = self.__mapper__[request.method.upper()]
            response = getattr(self, func_name)(request=request, *args, **kwargs)
            wrapped_response = self._respond(response)
            return jsonify(wrapped_response)
        except BaseException as e:
            return str(e)

    @staticmethod
    def _split_path(path):
        return path.split('/', 1) if '/' in path else (path, '')

    @staticmethod
    def _traverse_entity(entity, path):
        current_entity = entity
        for key in path.split('/'):
            if key:
                if isinstance(current_entity, dict):
                    current_entity = current_entity[key]
                elif isinstance(current_entity, list):
                    current_entity = current_entity[int(key)]
                else:
                    try:
                        current_entity = getattr(current_entity, key)
                        if callable(current_entity):
                            current_entity = current_entity()
                    except AttributeError:
                        raise Exception("Invalid path")
        return current_entity

    @property
    def __name__(self):
        return self.__class__.__name__

    @property
    def methods(self):
        return self.__mapper__.keys()
