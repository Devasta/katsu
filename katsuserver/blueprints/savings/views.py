import flask
import flask_login
from . import savings
from . import schemas
from . import models

from ...models import requires_permission, get_config


@savings.route('/', methods=['GET'])
@flask_login.login_required
@requires_permission('savings_get')
def savingsaccount_search():

    schema = schemas.SavingSearchSchema(data=flask.request.args)

    if schema.validate():
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

            results = models.savingsaccount_get(accountid=int(flask.request.args.get('accountid')) if flask.request.args.get('accountid') is not None else None,
                                                memberid=int(flask.request.args.get('memberid')) if flask.request.args.get('memberid') is not None else None,
                                                status=flask.request.args.get('status'),
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
        flask.abort(400, schema.errors)


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

    schema = schemas.SavingsAccountSchema(data=flask.request.json)
    if schema.validate():
        try:
            newacc = models.savingsaccount_create(memberid=flask.request.json.get('memberid'),
                                                  currency=flask.request.json.get('currency'),
                                                  )

            return flask.jsonify({'accountid': newacc}), 201
        except KeyError:
            flask.abort(404)
        except Exception as e:
            flask.abort(500, e)
    else:
        flask.abort(400, schema.errors)
