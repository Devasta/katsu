import flask
import flask_login
from app.blueprints.savings import savings
from . import forms
from . import models
import psycopg2

from app.models import requires_permission, get_config


@savings.route('/', methods=['GET'])
@flask_login.login_required
@requires_permission('savings_get')
def savingsaccount_search():

    form = forms.SavingsSearchForm(formdata=flask.request.args)

    if form.validate():
        try:
            # If the user does not provide a pagenumber or provides something that is not an integer, we just set to 1.
            try:
                if flask.request.args.get('page') > 1:
                    page = int(flask.request.args.get('page'))
                else:
                    page = 1
            except TypeError:
                page = 1

            limit = flask.request.args.get('limit') or get_config('PAGINATION_COUNT')['configvalue']

            results = models.savingsaccount_get(accountid=form.accountid.data,
                                                memberid=form.memberid.data,
                                                status=form.status.data,
                                                offset=((page - 1)*int(limit)),
                                                limit=int(limit)
                                                )
            if len(results) == 0:
                return '', 204
            else:
                return flask.jsonify({'savingsaccounts': results}), 200
        except Exception as e:
            flask.abort(500, e)
    else:
        flask.abort(400, form.errors)


@savings.route('/<int:accountid>/', methods=['GET'])
@flask_login.login_required
@requires_permission('savings_get')
def savingsaccount_main(accountid):
    try:
        account = models.savingsaccount_get(accountid=accountid)
    except Exception as e:
        flask.abort(500, e)

    if len(account) == 0:
        flask.abort(404)
    else:
        return flask.jsonify({'savingsaccount': account[0]}), 200


@savings.route('/', methods=['POST'])
@flask_login.login_required
@requires_permission('savings_create')
def savingsaccount_insert():

    form = forms.SavingsAccountForm.from_json(flask.request.json)

    if form.validate():
        try:
            newacc = models.savingsaccount_create(memberid=form.memberid.data)

            return flask.jsonify({'accountid': newacc}), 201
        except KeyError:
            flask.abort(404)
        except Exception as e:
            flask.abort(500, e)
    else:
        flask.abort(400, form.errors)
