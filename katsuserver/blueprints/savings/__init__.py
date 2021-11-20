import flask

savings = flask.Blueprint('savings', __name__, url_prefix='/savings')
from . import views

