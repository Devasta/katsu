import flask
import flask_login
#import flask_wtf
#import wtforms_json
import config


def create_app(config_name='default'):

    app = flask.Flask(__name__)

    if config_name is not None:
        app.config.from_object(config.config[config_name])

        config.config[config_name].init_app(app)

    from . import models
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

    from . import errors
    errors.register_errorhandlers(app)

    from . import views
    views.register_views(app)

    from . import database
    app.db = database.db()
    app.db.init_app(app)

    from .blueprints.codelinks import codelinks
    app.register_blueprint(codelinks)
    from .blueprints.comments import comments
    app.register_blueprint(comments)
    from .blueprints.configs import configs
    app.register_blueprint(configs)
    #from .blueprints.documents import documents
    #app.register_blueprint(documents)
    #from .blueprints.loans import loans
    #app.register_blueprint(loans)
    from .blueprints.members import members
    app.register_blueprint(members)
    from .blueprints.savings import savings
    app.register_blueprint(savings)
    #from .blueprints.transactions import transactions
    #app.register_blueprint(transactions)

    return app
