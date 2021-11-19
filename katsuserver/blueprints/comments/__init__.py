import flask

comments = flask.Blueprint('comments', __name__, url_prefix='/comments')
from . import views
