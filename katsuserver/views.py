import flask
import flask_login
import flask_wtf.csrf
from . import forms


def register_views(app):

    @app.route('/CSRF/', methods=['GET'])
    def csrf():
        return flask.jsonify({'CSRF': flask_wtf.csrf.generate_csrf()}), 200

    @app.route('/login/', methods=['GET'])
    @flask_login.login_required
    def isloggedin():
        return flask.jsonify({'userid': flask_login.current_user.userid}), 200

    @app.route('/login/', methods=['POST'])
    def login():
        form = forms.LoginForm.from_json(flask.request.json)
        if form.validate():
            try:
                loggeduser = app.models.User()
                if loggeduser.validateid(email=form.email.data,
                                         password=form.password.data):
                    flask_login.login_user(loggeduser)
                    return '', 201
                else:
                    flask.abort(401)
            except ValueError:
                flask.abort(401)
        else:
            return flask.abort(400, form.errors)

    @app.route('/login/', methods=['DELETE'])
    @flask_login.login_required
    def logout():
        flask_login.logout_user()
        return '', 204

