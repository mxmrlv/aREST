import pickle

import requests
from aria.storage import api

from . import wrappers


class RESTClient(api.ModelAPI):

    ENDPOINT = 'http://127.0.0.1:5000'

    def __init__(self, *args, **kwargs):
        super(RESTClient, self).__init__(*args, **kwargs)
        # Used by the operation context itself, we should probably create a `close` method per mapi
        # instead.
        self._session = type('MockSession', (object,), {'remove': lambda *a, **kw: None})()
        self._engine = type('MockSession', (object,), {'dispose': lambda *a, **kw: None})()

    def put(self, entry, **kwargs):
        response = requests.put(
            '/'.join([self.ENDPOINT, 'core', self.name]),
            data=pickle.dumps(entry._obj if isinstance(entry, wrappers.WrapperBase) else entry)
        )
        return self._respond(response, self.name)

    def create(self, **kwargs):
        pass

    def get(self, entry_id, **kwargs):
        suffix = '/'.join([self.name, str(entry_id)])
        response = requests.get('/'.join([self.ENDPOINT, 'core', suffix]))
        return self._respond(response, suffix)

    def refresh(self, entry):
        return self.get(entry.id)

    def iter(self, **kwargs):
        response = requests.get('/'.join([self.ENDPOINT, 'core', self.name]), json=kwargs)
        for item in self._respond(response, self.name):
            yield item

    def update(self, entry, **kwargs):
        suffix = '/'.join([self.name, str(entry.id)])
        response = requests.patch('/'.join([self.ENDPOINT, 'core', suffix]),
                                  data=pickle.dumps(entry._obj))
        return self._respond(response, suffix)

    def delete(self, entry_id, **kwargs):
        pass

    @classmethod
    def _respond(cls, response, attribute_path):
        try:
            return cls._wrap(pickle.loads(response.json()), attribute_path)
        except:
            raise Exception(response.text)

    @classmethod
    def _wrap(cls, value, attribute_path):
        from aria.modeling.mixins import ModelMixin

        if isinstance(value, dict):
            return wrappers.DictWrapper(
                _attribute_path=attribute_path,
                _query=cls._get_query,
                **dict(
                    (key, cls._wrap(value, '/'.join([attribute_path, key])))
                    for key, value in (value or {}).items()
                )
            )
        elif isinstance(value, list):
            return wrappers.ListWrapper(
                _attribute_path=attribute_path,
                _query=cls._get_query,
                seq=[cls._wrap(item, '/'.join([attribute_path, str(getattr(item, 'id', i))]))
                     for i, item in enumerate(value or [])]
            )
        elif isinstance(value, ModelMixin):
            return wrappers.ObjectWrapper(
                _attribute_path=attribute_path,
                _query=cls._get_query,
                obj=value
            )

        return value

    @classmethod
    def _get_query(cls, entry_path):
        response = requests.get('/'.join([cls.ENDPOINT, 'core', entry_path]))
        return cls._respond(response, entry_path)


