import flask
import flask_login
from . import users
from . import forms
from . import models
import app.models

from app.models import get_config, get_codelink

"""
    NEVER EVER CREATE A METHOD TO EDIT TRANSACTIONS.
    NEVER EVER CREATE A METHOD TO DELETE TRANSACTIONS.
"""


@users.route('/users/', methods=['GET'])
@flask_login.login_required
def users_get():

    form = forms.UserSearchForm.from_json(formdata=flask.request.args)

    if form.validate():
        try:

            # If the user does not provide a pagenumber or provides something that is not an integer, we just set to 1.
            try:
                if flask.request.args.get('page') > 1:
                    page = int(flask.request.args.get('page'))
                else:
                    page = 1
            except TypeError:
                page = 1

            limit = flask.request.args.get('limit') or get_config('PAGINATION_COUNT')['configvalue']

            users = models.users_get(
                                    userid=form.userid.data,
                                    memberid=form.memberid.data,
                                    email=form.email.data,
                                    offset=((page - 1) * int(limit)),
                                    limit=int(limit)
            )

            if len(users) == 0:
                return '', 204
            else:
                return flask.jsonify({'users': users}), 200
        except Exception as e:
            flask.abort(500, e)
    else:
        flask.abort(400, form.errors)


@users.route('/users/<int:userid>/', methods=['GET'])
@flask_login.login_required
def user_get(userid):
    try:

        user = models.users_get(userid=userid)

        if len(user) == 0:
            flask.abort(404)
        else:
            return flask.jsonify({'user': users[0]}), 200
    except Exception as e:
        flask.abort(500, e)


@users.route('/users/', methods=['POST'])
@flask_login.login_required
def user_create():
    pass


@users.route('/users/<int:userid>/', methods=['PUT'])
@flask_login.login_required
def user_update(userid):
    pass

