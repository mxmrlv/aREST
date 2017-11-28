
from flask import Flask

from . import (
    core,
    execution,
    plugin,
    service,
    service_template,
    task,
    log,
)

app = Flask(__name__)

for entity in (core, execution, plugin, service, service_template, task, log):
    endpoint = '/{0}'.format(entity.handler.__endpoint__)
    app.route(endpoint, methods=entity.handler.methods)(entity.handler)
