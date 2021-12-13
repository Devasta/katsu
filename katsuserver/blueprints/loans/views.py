import flask
import flask_login
from . import loans
from . import schemas
from . import models

from ...models import requires_permission, get_config


@loans.route('/', methods=['GET'])
@flask_login.login_required
@requires_permission('loans_get')
def loan_search():

    schema = schemas.LoanSearchSchema(data=flask.request.args)

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

            results = models.loans_get(loanid=flask.request.args.get('loanid'),
                                       memberid=flask.request.args.get('memberid'),
                                       status=flask.request.args.get('statusid'),
                                       offset=((page - 1)*int(limit)),
                                       limit=int(limit)
                                       )
            if len(results) == 0:
                return '', 204
            else:
                response = {'loans': results}
                return flask.jsonify(response), 200, {'ContentType': 'application/json'}
        except Exception as e:
            response = {'errors': str(e)}
            return flask.jsonify(response), 500, {'ContentType': 'application/json'}
    else:
        response = {'errors': schema.errors}
        return flask.jsonify(response), 400, {'ContentType': 'application/json'}


@loans.route('/<int:loanid>/', methods=['GET'])
@flask_login.login_required
@requires_permission('loans_get')
def loan_get(loanid):
    try:
        loan = models.loans_get(loanid=loanid)
    except Exception as e:
        flask.abort(500, e)

    if len(loan) == 0:
        flask.abort(404)
    else:
        return flask.jsonify({'loan': loan[0]}), 200


@loans.route('/', methods=['POST'])
@flask_login.login_required
@requires_permission('loans_create')
def loan_create():

    schema = schemas.LoanSchema(data=flask.request.json)

    if schema.validate('NEW'):
        try:
            loanid = models.loan_create(memberid=flask.request.json.get('memberid'),
                                        amount=flask.request.json.get('amount'),
                                        currency=flask.request.json.get('currency'),
                                        purpose=flask.request.json.get('purpose')
                                        )
            return flask.jsonify(loanid), 201
        except KeyError:
            flask.abort(404)
        except Exception as e:
            flask.abort(500, e)
    else:
        flask.abort(400, schema.errors)


@loans.route('/<int:loanid>/', methods=['PATCH'])
@flask_login.login_required
@requires_permission('loans_update')
def loan_update(loanid):

    schema = schemas.LoanSchema(data=flask.request.json)

    if schema.validate('UPDATE'):

        loan = models.loans_get(loanid=loanid)

        if len(loan) == 0:
            flask.abort(404)
        elif loan[0]['statusid'] == 'C':
            flask.abort(400, 'Cannot amend closed loan')
        else:
            try:
                models.loan_update(loanid=loanid, userid=flask_login.current_user.userid, original=loan[0], updates=flask.request.json)
                return '', 204
            except ValueError as e:
                if str(e).startswith('User loan approval limit is'):
                    flask.abort(403, e)
                else:
                    flask.abort(400, e)
            except Exception as e:
                flask.abort(500, e)
    else:
        flask.abort(400, schema.errors)
