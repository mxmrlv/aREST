import collections

from aria.modeling.mixins import ModelMixin


class AbstractHandler(object):
    __mapper__ = {}

    def _to_string(self, value):
        if isinstance(value, collections.Iterable):
            value = tuple(self._to_string(item) for item in value)
        elif isinstance(value, ModelMixin):
            value = value.to_dict()
        return str(value)

    def __call__(self, *args, **kwargs):
        from flask import request
        try:
            func_name = self.__mapper__[request.method.upper()]
            return self._to_string(getattr(self, func_name)(request))
        except BaseException as e:
            return str(e)

    @property
    def __name__(self):
        return self.__class__.__name__

    @property
    def methods(self):
        return self.__mapper__.keys()
