import flask
import flask_wtf


def register_errorhandlers(app):
    @app.errorhandler(flask_wtf.csrf.CSRFError)
    def csrf_error(CSRFError):
        return flask.jsonify({'error': 'CSRF token missing or expired.'}), 401

    @app.errorhandler(400)
    def error_400(e):
        return flask.jsonify({'errors': e.description}), 400

    @app.errorhandler(401)
    def error_401(e):
        return flask.jsonify({'errors': 'Login required'}), 401

    @app.errorhandler(403)
    def error_403(e):
        return flask.jsonify({'errors': f'Access denied. {e}'}), 403

    @app.errorhandler(404)
    def error_404(e):
        return flask.jsonify({'errors': 'Resource not found'}), 404

    @app.errorhandler(405)
    def error_405(e):
        return flask.jsonify({'errors': 'Method not supported'}), 405

    @app.errorhandler(409)
    def error_409(e):
        return flask.jsonify({'errors': 'Resource conflict'}), 409

    @app.errorhandler(500)
    def error_500(errors):
        return flask.jsonify({'errors': errors}), 500
