import flask


def configs_get(configname=None):
    with flask.current_app.db.db_cursor() as cur:
        cur.execute(""" SELECT
                          configname,
                          configvalue,
                          description
                        FROM vw_configs
                        WHERE %(configname)s is NULL or configname LIKE %(configname)s""", {'configname': configname})
        config = cur.fetchall()

        return config


def config_create(configname, configvalue, description):
    with flask.current_app.db.db_cursor() as cur:
        cur.execute("""SELECT config_create(%(configname)s,
                                                %(configvalue)s,
                                                %(description)s
                                                )""", {'configname': configname,
                                                       'configvalue': configvalue,
                                                       'description': description})
        return


def config_update(configname, configvalue, description):
    with flask.current_app.db.db_cursor() as cur:
        cur.execute("""SELECT config_update(%(configname)s,
                                                   %(configvalue)s,
                                                   %(description)s
                                                  )""", {'configname': configname,
                                                         'configvalue': configvalue,
                                                         'description': description})
        return

