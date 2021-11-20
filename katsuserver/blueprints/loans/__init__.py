import flask

loans = flask.Blueprint('loans', __name__, url_prefix='/loans')
from . import views
from . import models
