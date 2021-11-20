import flask


def transaction_get(transactionid=None, accountid=None, offset=0, limit=None):
    with flask.current_app.db.db_cursor() as cur:
        cur.execute("""SELECT
                           transactionid,
                           transactiondetailid,
                           entrydate,
                           description,
                           accountid,
                           debit,
                           amount,
                           newbalance
                       FROM vw_transactions
                       WHERE (%(transactionid)s IS NULL OR transactionid = %(transactionid)s)
                       AND   (%(accountid)s IS NULL OR accountid = %(accountid)s)
                       ORDER BY entrydate DESC
                       OFFSET %(offset)s
                       LIMIT %(limit)s
        """, {'transactionid': transactionid,
              'accountid': accountid,
              'offset': offset,
              'limit': limit
              })
        transactiondetail = cur.fetchall()
        return transactiondetail
