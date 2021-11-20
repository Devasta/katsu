import flask

members = flask.Blueprint('members', __name__, url_prefix='/members')
from . import views
