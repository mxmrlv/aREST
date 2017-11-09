from aria.modeling.mixins import ModelMixin


class AbstractHandler(object):
    __mapper__ = {}

    @staticmethod
    def _to_string(value):
        if isinstance(value, ModelMixin):
            value = value.to_dict()
        return str(value)

    def __call__(self, *args, **kwargs):
        from flask import request
        func_name = self.__mapper__[request.method.upper()]
        return self._to_string(getattr(self, func_name)(request))

    @property
    def __name__(self):
        return self.__class__.__name__

    @property
    def methods(self):
        return self.__mapper__.keys()
