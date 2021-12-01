import flask
import flask_login
from . import schemas


def register_views(app):

    @app.route('/login/', methods=['GET'])
    @flask_login.login_required
    def isloggedin():
        return flask.jsonify({'userid': flask_login.current_user.userid}), 200

    @app.route('/login/', methods=['POST'])
    def login():
        schema = schemas.LoginSchema(flask.request.json)
        if schema.validate():
            try:
                loggeduser = app.models.User()
                if loggeduser.validateid(email=flask.request.json['email'],
                                         password=flask.request.json['password']):
                    flask_login.login_user(loggeduser)
                    return '', 201
                else:
                    flask.abort(401)
            except ValueError:
                flask.abort(401)
        else:
            return flask.abort(400, schema.errors)

    @app.route('/login/', methods=['DELETE'])
    @flask_login.login_required
    def logout():
        flask_login.logout_user()
        return '', 204

