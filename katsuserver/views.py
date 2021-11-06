import flask
import flask_login
import flask_wtf.csrf


def register_views(app):
    @app.route('/CSRF/', methods=['GET'])
    def csrf():
        return flask.jsonify({'CSRF': flask_wtf.csrf.generate_csrf()}), 200