import flask

documents = flask.Blueprint('documents', __name__, url_prefix='/documents')
from . import views
