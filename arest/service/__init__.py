
from flask import Flask

from . import (
    execution,
    plugin,
    service,
    service_template,
    core
)

app = Flask(__name__)


def register_api(**app_kwargs):
    app.config.update(**app_kwargs)
    for entity in (execution, plugin, service, service_template, core):
        endpoints = (
            entity.handler.__endpoint__
            if isinstance(entity.handler.__endpoint__, (list, tuple)) else
            (entity.handler.__endpoint__,)
        )
        for endpoint_suffix in endpoints:
            endpoint = '/{0}'.format(endpoint_suffix)
            app.route(endpoint, methods=entity.handler.methods)(entity.handler)



register_api(
    SQLALCHEMY_DATABASE_URI='sqlite://///home/maxim-pcu/.aria/models/db.sqlite',
    SQLALCHEMY_TRACK_MODIFICATIONS=True
)