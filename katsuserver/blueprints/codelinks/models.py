import flask


def codelinks_get(codelinkname=None):
    with flask.current_app.db.db_cursor() as cur:
        cur.execute(""" SELECT
                          codelinkname,
                          accountid,
                          description
                        FROM vw_codelinks
                        WHERE %(codelinkname)s IS NULL or codelinkname LIKE %(codelinkname)s
                    """, {'codelinkname': codelinkname})
        codelinks = cur.fetchall()

        return codelinks


def codelink_create(codelinkname, accountid, description):
    with flask.current_app.db.db_cursor() as cur:

        cur.execute("""
                        SELECT codelink_create(%(codelinkname)s,
                                              %(accountid)s,
                                              %(description)s
                                              )""", {'codelinkname': codelinkname,
                                                     'accountid': accountid,
                                                     'description': description})

        return


def codelink_update(codelinkname, accountid, description):
    with flask.current_app.db.db_cursor() as cur:
        cur.execute("""SELECT codelink_update(%(codelinkname)s,
                                             %(accountid)s,
                                             %(description)s
                                             )""", {'codelinkname': codelinkname,
                                                    'accountid': accountid,
                                                    'description': description})
        return
