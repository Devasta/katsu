import flask
import flask_login
from . import loans
from . import forms
from . import models
import psycopg2

from ...models import requires_permission, get_config


@loans.route('/', methods=['GET'])
@flask_login.login_required
@requires_permission('loans_get')
def loan_search():

    form = forms.LoanSearchForm(formdata=flask.request.args)

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

            results = models.loans_get(loanid=form.loanid.data,
                                       memberid=form.memberid.data,
                                       status=form.status.data,
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
        response = {'errors': form.errors}
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
    form = forms.MainLoanForm.from_json(formdata=flask.request.json)
    if form.validate('NEW'):
        try:
            loanid = models.loan_create(memberid=form.memberid.data,
                                        amount=form.amount.data,
                                        purpose=form.purpose.data,
                                        )
            return flask.jsonify(loanid), 201
        except KeyError:
            flask.abort(404)
        except Exception as e:
            flask.abort(500, e)
    else:
        flask.abort(400, form.errors)


@loans.route('/<int:loanid>/', methods=['PATCH'])
@flask_login.login_required
@requires_permission('loans_update')
def loan_update(loanid):

    form = forms.MainLoanForm.from_json(formdata=flask.request.json)
    if form.validate('UPDATE'):

        loan = models.loans_get(loanid=loanid)

        if len(loan) == 0:
            flask.abort(404)
        elif loan[0]['statusid'] == 'C':
            flask.abort(400, 'Cannot amend closed loan')
        else:
            try:
                models.loan_update(loanid=loanid, userid=flask_login.current_user.userid, original=loan[0], updates=form.patch_data)
                return '', 204
            except ValueError as e:
                if str(e).startswith('User loan approval limit is'):
                    flask.abort(403, e)
                else:
                    flask.abort(400, e)
            except Exception as e:
                flask.abort(500, e)
    else:
        flask.abort(400, form.errors)
