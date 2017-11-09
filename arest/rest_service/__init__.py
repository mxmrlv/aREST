
from flask import Flask

from . import (
    execution,
    plugin,
    service,
    service_template,
    task,
    log
)

app = Flask(__name__)

for entity in (execution, plugin, service, service_template, task, log):
    endpoint = '/{0}'.format(entity.handler.__endpoint__)
    app.route(endpoint, methods=entity.handler.methods)(entity.handler)
