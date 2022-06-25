import flask
import flask_login
import lxml.etree as ET
from . import codelinks
from . import schemas
from . import models


from ...models import requires_permission


@codelinks.route('/', methods=['GET'])
#@flask_login.login_required
#@requires_permission('configs_get')
def all_codelinks():

    schema = schemas.CodelinkSearchSchema(data=flask.request.args)

    if schema.validate():
        try:

            results = models.codelinks_get(codelinkname=flask.request.args.get('codelinkname'))

            if len(results) == 0:
                return '', 204
            else:
                NS = flask.current_app.config.get('NAMESPACE_URI')
                response = ET.Element(f'{{{NS}}}codelinks')
                for c in results:
                    code = ET.SubElement(response, f'{{{NS}}}codelink')
                    code.set('name', c['codelinkname'])
                    code.set('accountid', str(c['accountid']))
                    code.set('description', c['description'])

                print(ET.tostring(response).decode())
                return flask.jsonify({'codelinks': results}), 200
        except Exception as e:
            flask.abort(500, str(e))
    else:
        flask.abort(400, schema.errors)


@codelinks.route('/', methods=['POST'])
@flask_login.login_required
@requires_permission('configs_create')
def new_codelink():

    schema = schemas.CodelinkSchema(data=flask.request.json)

    if schema.validate():
        try:
            models.codelink_create(codelinkname=flask.request.json.get('codelinkname'),
                                   accountid=flask.request.json.get('accountid'),
                                   description=flask.request.json.get('description'))
            return '', 201
        except KeyError:
            flask.abort(409)
        except Exception as e:
            flask.abort(500, e)
    else:
        flask.abort(400, schema.errors)


@codelinks.route('/<string:codelink>/', methods=['PUT'])
@flask_login.login_required
@requires_permission('configs_update')
def edit_codelink(codelink):

    schema = schemas.CodelinkSchema(data=flask.request.json)

    if codelink != flask.request.json.get('codelinkname'):
        flask.abort(400, 'Payload Codelink name does not match resource URL')

    if schema.validate():
        try:
            models.codelink_update(codelinkname=flask.request.json.get('codelinkname'),
                                   accountid=flask.request.json.get('accountid'),
                                   description=flask.request.json.get('description'))

            return '', 204
        except KeyError:
            flask.abort(404)
        except Exception as e:
            flask.abort(500, e)
    else:
        flask.abort(400, schema.errors)
