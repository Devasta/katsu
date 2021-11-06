import flask


users = flask.Blueprint('users', __name__, url_prefix='/users')
from . import views

