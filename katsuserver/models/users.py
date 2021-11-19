import functools
import flask
import flask_login
import bcrypt





"""
    A lot of the stuff down here is dealing with logins and the like. I have a users blueprint, but it seems more
    appropriate to keep that just for dealing with users being set up, configured and the like, while leaving the details
    of authentication all here.
"""


def requires_permission(permission):
    def wrapper(func):
        @functools.wraps(func)
        def permcheck(*args, **kwargs):
            if permission in flask_login.current_user.permissions:
                if flask_login.current_user.permissions[permission]:
                    return func(*args, **kwargs)
                else:
                    return flask.abort(403)
            else:
                return flask.abort(500)
        return permcheck
    return wrapper


class User:

    def __init__(self):
        self.is_authenticated = False
        self.is_active = True
        self.is_anonymous = True
        self.userid = None
        self.tokenid = None
        self.memberid = None
        self.email = None
        self.forename = None
        self.surname = None
        self.password = None
        self.roleid = None
        self.rolename = None
        self.permissions = None
        self.STAFF = False
        return

    def validateid(self, email, password):
        # if email supplied, get the details and validate
        with flask.current_app.db.db_cursor() as cur:
            cur.execute("""SELECT userid, email, forename, surname, password, tokenid, memberid from users \
                           WHERE email like %(email)s""", {'email': email})
            userresult = cur.fetchone()
            if userresult is not None:
                if bcrypt.checkpw(password.encode('utf-8'), userresult['password'].encode('utf-8')):
                    self.userid = userresult['userid']
                    self.tokenid = userresult['tokenid']
                    self.memberid = userresult['memberid']
                    return True
                else:
                    return False
            else:
                return False

    def get(self, tokenid):
        # If the client is logged in, they'll have an ID. Get the rest of the details here.
        with flask.current_app.db.db_cursor() as cur:
            cur.execute(""" SELECT
                                a.userID,
                                a.tokenid,
                                a.memberid,
                                a.email,
                                a.forename,
                                a.surname,
                                a.password,
                                a.roleID,
                                a.rolename,
                                a.members_get,
                                a.members_create,
                                a.members_update,
                                a.savings_get,
                                a.savings_create,
                                a.savings_update,
                                a.savings_withdrawalimit,
                                a.loans_get,
                                a.loans_create,
                                a.loans_update,
                                a.loans_approvelimit,
                                a.configs_get,
                                a.configs_create,
                                a.configs_update,
                                a.comments_get,
                                a.comments_create
                            FROM vw_userdetails a
                            WHERE tokenid = %(tokenid)s""", {'tokenid': tokenid})
            userresult = cur.fetchone()
            if userresult is None:
                raise Exception('User ID not found.')
            else:
                if userresult['memberid']:
                    self.memberid = userresult['memberid']
                else:
                    self.STAFF = True
                self.userid = userresult['userid']
                self.tokenid = userresult['tokenid']
                self.email = userresult['email']
                self.forename = userresult['forename']
                self.surname = userresult['surname']
                self.password = userresult['password']
                self.roleid = userresult['roleid']
                self.rolename = userresult['rolename']
                self.is_authenticated = True
                self.is_active = True
                self.is_anonymous = False
                self.permissions = {
                    'members_get': userresult['members_get'],
                    'members_create': userresult['members_create'],
                    'members_update': userresult['members_update'],
                    'savings_get': userresult['savings_get'],
                    'savings_create': userresult['savings_create'],
                    'savings_update': userresult['savings_update'],
                    'savings_withdrawalimit': userresult['savings_withdrawalimit'],
                    'loans_get': userresult['loans_get'],
                    'loans_create': userresult['loans_create'],
                    'loans_update': userresult['loans_update'],
                    'loans_approvelimit': userresult['loans_approvelimit'],
                    'configs_get': userresult['configs_get'],
                    'configs_create': userresult['configs_create'],
                    'configs_update': userresult['configs_update'],
                    'comments_get': userresult['comments_get'],
                    'comments_create': userresult['comments_create'],
                }

    def get_id(self):  # Flask_Login depends on this.
        return str(self.tokenid if self.tokenid is not None else None)
