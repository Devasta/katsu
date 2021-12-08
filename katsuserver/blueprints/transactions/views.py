import flask
import flask_login
from . import transactions
from . import schemas
from . import models

from ...models import get_config, get_codelink, account_details_get, transaction_create

"""
    NEVER EVER CREATE A METHOD TO EDIT TRANSACTIONS.
    NEVER EVER CREATE A METHOD TO DELETE TRANSACTIONS.
"""


@transactions.route('/', methods=['GET'])
@flask_login.login_required
def financial_transactions_search():

    schema = schemas.TransactionSearchSchema(data=flask.request.args)

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

            transactions = models.transaction_get(transactionid=flask.request.json.get('transactionid'),
                                                  accountid=flask.request.json.get('accountid'),
                                                  offset=((page - 1) * int(limit)),
                                                  limit=int(limit)
                                                  )
            if len(transactions) == 0:
                return '', 204
            else:
                return flask.jsonify({'transactions': transactions}), 200
        except Exception as e:
            flask.abort(500, e)
    else:
        flask.abort(400, schema.errors)


@transactions.route('/<int:transactionid>/', methods=['GET'])
@flask_login.login_required
def financial_transactions_view(transactionid):
    try:
        transaction = models.transaction_get(transactionid=transactionid)
    except Exception as e:
        flask.abort(500)
    if transaction:
        return flask.jsonify({'transactions': transaction}), 200
    else:
        flask.abort(404)


@transactions.route('/', methods=['POST'])
@flask_login.login_required
def financial_transaction_new():

    """

        This endpoint can take multiple transaction layouts.

            Basic:      Just add/remove from savings/loans. Will be used for withdrawals and stuff where we don't know
                        the other account entries or the debit/credit flags in the client.

            Explicit:   All details should be provided, both the accounts of all entries and the debit/credit flags.

    """

    if flask.request.args.get('mode') in ['basic', 'explicit']:
        mode = flask.request.args.get('mode')
    else:
        flask.abort(400, 'Invalid Transaction booking mode set.')

    if mode == 'basic':
        schema = schemas.BasicTransactionSchema(data=flask.request.json)

        if schema.validate():

            account = account_details_get(flask.request.args.get('accountid'))

            if account is None:
                flask.abort(404)
            else:

                cashacc = get_codelink('CASH_ACCOUNT')

                if account['accountgroup'] in ['SAVE', 'LOAN']:

                    description = flask.request.json.get('description')
                    transactions = [
                        (
                            flask.request.json.get('accountid'),
                            True  if (flask.request.json.get('amount') > 0 and account['debitincrease'] is True) else False,
                            abs(flask.request.json.get('amount'))
                        ),
                        (
                            cashacc,
                            False if (flask.request.json.get('amount') > 0 and account['debitincrease'] is True) else True,
                            abs(flask.request.json.get('amount'))
                        )
                    ]
                else:
                    flask.abort(400, 'Account is not a savings or loan.')

        else:
            flask.abort(400, schema.errors)

    elif mode == 'explicit':

        schema = schemas.DetailedTransactionSchema(data=flask.request.json)

        if schema.validate():

            description = flask.request.json.get('description')
            transactions = []
            for entry in flask.request.json.get('entries'):
                t = (entry['accountid'],
                     True if entry['debit'] == 'Debit' else False,
                     entry['amount'])
                transactions.append(t)

        else:
            flask.abort(400, schema.errors)

    else:
        flask.abort(400, 'Invalid Transaction booking mode set.')

    """
        The actual database transaction begins here.
    """
    try:
        transactionid = transaction_create(description=description,
                                           transactions=transactions)

        return flask.jsonify({'transactionid': transactionid}), 201
    except KeyError as e:
        flask.abort(404, 'Account ID not found.')
    except Exception as e:
        flask.abort(500, e)
