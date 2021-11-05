import flask


def create_app(config_name='default'):

    app = flask.Flask(__name__)

    from app import errors
    errors.register_errorhandlers(app)
    from app import views
    views.register_views(app)


    return app