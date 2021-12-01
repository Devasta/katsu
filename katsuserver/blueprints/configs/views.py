import flask
import flask_login
from . import configs
from . import models
from . import schemas

from ...models import requires_permission


@configs.route('/', methods=['GET'])
@flask_login.login_required
@requires_permission('configs_get')
def all_configs():

    schema = schemas.ConfigSearchSchema(data=flask.request.args)

    if schema.validate():
        try:

            results = models.configs_get(configname=flask.request.args.get('configname'))

            if len(results) == 0:
                return '', 204
            else:
                return flask.jsonify({'configs': results}), 200
        except Exception as e:
            flask.abort(500, e)
    else:
        flask.abort(400, schema.errors)


@configs.route('/', methods=['POST'])
@flask_login.login_required
@requires_permission('configs_create')
def new_config():

    schema = schemas.ConfigSchema(data=flask.request.json)

    if schema.validate():
        try:
            models.config_create(configname=flask.request.json['configname'],
                                 configvalue=flask.request.json['configvalue'],
                                 description=flask.request.json['description'])
            return '', 201
        except KeyError:
            flask.abort(409)
        except Exception as e:
            flask.abort(500, e)
    else:
        flask.abort(400, schema.errors)


@configs.route('/<string:config>/', methods=['PUT'])
@flask_login.login_required
@requires_permission('configs_update')
def edit_config(config):

    schema = schemas.ConfigSchema(data=flask.request.json)

    if config != flask.request.json['configname']:
        flask.abort(400, 'Payload Config name does not match resource URL')

    if schema.validate():
        try:
            models.config_update(configname=flask.request.json['configname'],
                                 configvalue=flask.request.json['configvalue'],
                                 description=flask.request.json['description'])

            return '', 204
        except KeyError:
            flask.abort(404)
        except Exception as e:
            flask.abort(500, e)
    else:
        flask.abort(400, schema.errors)
