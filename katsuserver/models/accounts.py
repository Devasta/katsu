import flask


def account_details_get(accountid):
    with flask.current_app.db.db_cursor() as cur:
        cur.execute("""
            SELECT
                accountid,
                memberid,
                accounttype,
                accountgroup,
                debitincrease
            FROM vw_accounts
            where accountid = %(accountid)s
        """, {'accountid': accountid}
                    )
        account = cur.fetchone()
        return account
