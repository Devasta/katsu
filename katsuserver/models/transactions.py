import flask

"""
+---------------------------------------------------+
|               The rules of the game               |
+-----------------------------+----------+----------+
|        Account Type         |  Debit   |  Credit  |
+-----------------------------+----------+----------+
| Assets                      | Increase | Decrease |
| Liabilities                 | Decrease | Increase |
| Equity                      | Decrease | Increase |
| Income                      | Decrease | Increase |
| Expenses                    | Increase | Decrease |
+-----------------------------+----------+----------+
| Assets = Liabilities + Equity + Income - Expenses |
+-----------------------------+----------+----------+
"""


def transaction_create(description, transactions):
    # Transactions is a list of Tuples.
    # (accountid integer, debit boolean, amount numeric)
    with flask.current_app.db.db_cursor() as cur:
        cur.execute("""select transaction_create(%(description)s, 
                                                        %(transactions)s::fintransaction[]
                                                        ) as newtransactionID""", {'description': description,
                                                                                   'transactions': transactions})
        transID = cur.fetchone()
        return transID


