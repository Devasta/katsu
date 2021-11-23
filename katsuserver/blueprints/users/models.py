import flask
import bcrypt


def users_get(userid=None, email=None, memberid=None, offset=0, limit=None):
    with flask.current_app.db.db_cursor() as cur:
        cur.execute("""
            SELECT
                userid,
                memberid,
                email,
                forename,
                surname,
                members_get,
                members_create,
                members_update,
                savings_get,
                savings_create,
                savings_update,
                savings_withdrawalimit,
                loans_get,
                loans_create,
                loans_update,
                loans_approvelimit,
                configs_get,
                configs_create,
                configs_update,
                comments_get,
                comments_create
            FROM vw_userdetails
            WHERE (%(userid)s IS NULL or userid = %(userid)s)
            AND (%(email)s IS NULL or email = %(email)s)
            AND (%(memberid)s IS NULL or memberid = %(memberid)s)
            OFFSET %(offset)s
            LIMIT %(limit)s
        """, {
                'userid': userid,
                'email': email,
                'memberid': memberid,
                'offset': offset,
                'limit': limit
              }
                     )

        users = cur.fetchall()

        return users


def create_user(email, forename, surname, password, rolename):
    with flask.current_app.db.db_cursor() as cur:
        hashedpassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cur.execute("""select * from roles""")
        print(cur.fetchall)
        cur.execute("""INSERT INTO users(email,forename,surname,password, roleid)
                       VALUES (%(email)s,%(forename)s,%(surname)s,%(password)s, 
                       (select roleid from roles where rolename = %(rolename)s)
                       )""",
                    {
                        'email': email,
                        'forename': forename,
                        'surname': surname,
                        'password': hashedpassword.decode("utf-8"),
                        'rolename': rolename
                     })
        return cur.lastrowid


def user_password_reset():
    pass
