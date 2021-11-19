import flask


def get_config(configname):
    """
        We store a lot of constants in the database, for stuff like pagination counts and the like.
        We use the below to fetch those.
    """
    with flask.current_app.db.db_cursor() as cur:
        cur.execute(""" SELECT
                          configname,
                          configvalue
                        FROM vw_configs
                        WHERE configname = %(configname)s""", {'configname': configname})
        config = cur.fetchone()
        return config


def get_codelink(codelinkname):
    """
        We store a lot of constants in the database, for the opposite account in financial transactions.
        We use the below to fetch those.
    """
    with flask.current_app.db.db_cursor() as cur:
        cur.execute(""" SELECT
                          codelinkname,
                          accountid
                        FROM vw_codelinks
                        WHERE codelinkname = %(codelinkname)s
                    """, {'codelinkname': codelinkname})
        codelink = cur.fetchone()

        if codelink is None:
            raise KeyError(f'CodeLink {codelinkname} not found.')
        else:
            return codelink['accountid']
