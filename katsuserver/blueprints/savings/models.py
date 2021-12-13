import flask


def savingsaccount_get(accountid=None, memberid=None, status=None, offset=0, limit=None):
    with flask.current_app.db.db_cursor() as cur:
        cur.execute(""" SELECT
                            savingsaccountID,
                            Status,
                            OpenDate,
                            CloseDate,
                            currentbalance,
                            entrydate,
                            memberid
                        FROM vw_savingsaccounts
                        WHERE (%(accountid)s IS NULL or savingsaccountID = %(accountid)s)
                          AND (%(memberid)s IS NULL or memberid = %(memberid)s)
                          AND (%(status)s IS NULL or Status = %(status)s)
                        OFFSET %(offset)s
                        LIMIT %(limit)s
        """, {'accountid': accountid,
              'memberid': memberid,
              'status': status,
              'offset': offset,
              'limit': limit,
              })
        accounts = cur.fetchall()
        return accounts


def savingsaccount_create(memberid, currency):
    with flask.current_app.db.db_cursor() as cur:
        cur.execute("""SELECT savingsaccount_create(
                                                %(memberid)s,
                                                %(currency)s
                                                )""",
                    {
                        'memberid': memberid,
                        'currency': currency
                    })
        accountid = cur.fetchone()
        return accountid['savingsaccount_create']

