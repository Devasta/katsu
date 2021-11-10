import flask

'''Users covers both staff and customers'''

users = flask.Blueprint('users', __name__, url_prefix='/users')
from . import views

