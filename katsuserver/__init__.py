import flask


def create_app(config_name='default'):

    app = flask.Flask(__name__)

    if config_name is not None:
        app.config.from_object(config.config[config_name])

        config.config[config_name].init_app(app)

    from app import models
    app.models = models

    LoginManager = flask_login.LoginManager()
    LoginManager.init_app(app)
    LoginManager.session_protection = "strong"

    @LoginManager.user_loader
    def load_user(tokenid):
        try:
            theuser = models.User()
            theuser.get(tokenid[0])
            return theuser
        except Exception as e:
            return None

    csrf = flask_wtf.CSRFProtect()
    csrf.init_app(app)
    wtforms_json.init()

    from app import errors
    errors.register_errorhandlers(app)

    from app import views
    views.register_views(app)

    from app import database
    app.db = database.db()
    app.db.init_app(app)

    return app
