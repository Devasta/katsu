import flask


def loans_get(loanid=None, memberid=None, status=None, offset=0, limit=None):
    with flask.current_app.db.db_cursor() as cur:
        cur.execute(""" SELECT
                            loanID,
                            memberID,
                            purpose,
                            ApplicationDate,
                            StartDate,
                            CloseDate,
                            amount,
                            approvaldate,
                            approvaluser,
                            interestrate,
                            outstandingloanamount,
                            paymentmethodid,
                            paymentmethod,
                            paymentamount,
                            paymentfrequency,
                            currentbalance,
                            entrydate,
                            statusid,
                            status,
                            approvalforename,
                            approvalsurname
                        FROM vw_loans
                        WHERE (%(loanid)s IS NULL or loanID = %(loanid)s)
                            AND (%(memberid)s IS NULL or memberid = %(memberid)s)
                            AND (%(status)s IS NULL or status = %(status)s)
                        OFFSET %(offset)s
                        LIMIT %(limit)s
        """, {'loanid': loanid,
              'memberid': memberid,
              'status': status,
              'offset': offset,
              'limit': limit,
              })
        loans = cur.fetchall()
        return loans


def loan_create(memberid, amount, purpose):
    with flask.current_app.db.db_cursor() as cur:
        cur.execute("""SELECT loan_create(%(memberid)s, %(amount)s, %(purpose)s) as loanid""",
                    {'memberid': memberid,
                     'amount': amount,
                     'purpose': purpose})
        newloanid = cur.fetchone()
        return newloanid


def loan_update(loanid, userid, original, updates):
    """
        An unbelievably complicated function. This contains a crazy amount of process flow, should probably be moved
        to its own file. First thing it'll do it grab a copy of the loan as its currently saved, then it will
        get together a list of the changes that need to be done, and call the necessary functions.

    :param loanid:
    :param updates:
    :return:
    """

    with flask.current_app.db.db_cursor() as cur:
        updateablefields = set(['amount', 'purpose', 'interestrate', 'paymentamount', 'nextpaymentdate', 'paymentfrequency','paymentmethodid'])

        if set(updates.keys()).intersection(updateablefields):
            cur.execute("""SELECT loan_update(  %(loanid)s,
                                                %(amount)s,
                                                %(purpose)s,
                                                %(interestrate)s,
                                                %(paymentamount)s,
                                                %(nextpaymentdate)s,
                                                %(paymentfrequency)s,
                                                %(paymentmethodid)s
                                                )""",
                        {
                            'loanid': loanid,
                            'amount': updates.get('amount', original.get('amount')),
                            'purpose': updates.get('purpose', original.get('purpose')),
                            'interestrate': updates.get('interestrate', original.get('interestrate')),
                            'paymentamount': updates.get('paymentamount', original.get('paymentamount')),
                            'nextpaymentdate': updates.get('nextpaymentdate', original.get('nextpaymentdate')),
                            'paymentfrequency': updates.get('paymentfrequency', original.get('paymentfrequency')),
                            'paymentmethodid': updates.get('paymentmethodid', original.get('paymentmethodid'))
                        }
                        )
        if 'statusid' in updates:
            cur.execute("""SELECT loan_status_update(%(loanid)s, %(statusid)s, %(userid)s, %(closecode)s, %(savingsaccountid)s)""",
                        {
                            'loanid': loanid,
                            'statusid': updates.get('statusid', original.get('statusid')),
                            'userid': userid,
                            'closecode': updates.get('closecode'),
                            'savingsaccountid': updates.get('savingsaccountid')
                        }
                        )

    return