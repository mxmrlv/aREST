from aria.modeling.mixins import ModelMixin

class HandlerBase(object):
    mapper = {}

    @staticmethod
    def _to_string(value):
        if isinstance(value, ModelMixin):
            value = value.to_dict()
        return str(value)

    def __call__(self, *args, **kwargs):
        from flask import request
        func_name = self.mapper[request.method.upper()]
        return getattr(self, func_name)(request)

    @property
    def __name__(self):
        return self.__class__.__name__
