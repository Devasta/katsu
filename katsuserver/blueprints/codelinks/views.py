import flask
import flask_login
from . import codelinks
from . import forms
from . import models


from ...models import requires_permission


@codelinks.route('/', methods=['GET'])
@flask_login.login_required
@requires_permission('configs_get')
def all_codelinks():

    form = forms.CodelinkSearchForm.from_json(formdata=flask.request.args)

    if form.validate():
        try:

            results = models.codelinks_get(codelinkname=form.codelinkname.data)

            if len(results) == 0:
                return '', 204
            else:
                return flask.jsonify({'codelinks': results}), 200
        except Exception as e:
            flask.abort(500, str(e))
    else:
        flask.abort(400, form.errors)


@codelinks.route('/', methods=['POST'])
@flask_login.login_required
@requires_permission('configs_create')
def new_codelink():

    form = forms.CodelinksForm.from_json(formdata=flask.request.json)

    if form.validate():
        try:
            models.codelink_create(codelinkname=form.codelinkname.data,
                                   accountid=form.accountid.data,
                                   description=form.description.data)
            return '', 201
        except KeyError:
            flask.abort(409)
        except Exception as e:
            flask.abort(500, e)
    else:
        flask.abort(400, form.errors)


@codelinks.route('/<string:codelink>/', methods=['PUT'])
@flask_login.login_required
@requires_permission('configs_update')
def edit_codelink(codelink):

    form = forms.CodelinksForm.from_json(formdata=flask.request.json)

    if codelink != form.codelinkname.data:
        flask.abort(400, 'Payload Codelink name does not match resource URL')

    if form.validate():
        try:
            models.codelink_update(codelinkname=codelink,
                                   accountid=form.accountid.data,
                                   description=form.description.data)

            return '', 204
        except KeyError:
            flask.abort(404)
        except Exception as e:
            flask.abort(500, e)
    else:
        flask.abort(400, form.errors)
