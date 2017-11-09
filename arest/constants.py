
from collections import namedtuple

_methods = namedtuple('Method', 'GET, POST, PUT, DELETE, PATCH')
METHODS = _methods(GET='GET',
                   POST='POST',
                   PUT='PUT',
                   DELETE='DELETE',
                   PATCH='PATCH')
