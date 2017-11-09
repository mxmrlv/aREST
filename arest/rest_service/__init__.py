
from flask import Flask

from .. constants import METHODS
from . import (
    service_template,
    service,
    plugin,
    execution
)

app = Flask(__name__)


app.route('/service_template',
          methods=[METHODS.PUT, METHODS.GET, METHODS.DELETE]
          )(service_template.handler)

app.route('/service',
          methods=[METHODS.POST, METHODS.GET, METHODS.DELETE]
          )(service.handler)

app.route('/execution',
          methods=[METHODS.POST, METHODS.GET]
          )(execution.handler)


