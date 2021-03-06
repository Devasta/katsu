import flask
import flask_login
from . import comments
from . import models
from . import schemas

from ...models import requires_permission, get_config


# Important Note: Do NOT create a URL that'll allow updating or deletion of comments, except to have a custom 405 error.
# There is no scenario where editing comments can be considered a good idea.
# Likewise, deletion should only be done as part of some archiving process.


@comments.route('/', methods=['GET'])
@flask_login.login_required
@requires_permission('comments_get')
def comments_search():

    schema = schemas.CommentSearchSchema(data=flask.request.args)

    if schema.validate():
        try:

            try:
                if flask.request.args.get('page') > 1:
                    page = int(flask.request.args.get('page'))
                else:
                    page = 1
            except TypeError:
                page = 1

            limit = flask.request.args.get('limit') or get_config('PAGINATION_COUNT')['configvalue']

            comments = models.comments_get(accountid=flask.request.args.get('accountid'),
                                           memberid=flask.request.args.get('memberid'),
                                           offset=((page - 1) * int(limit)),
                                           limit=int(limit)
                                           )

            if len(comments) == 0:
                return '', 204
            else:
                return flask.jsonify({'comments': comments}), 200
        except Exception as e:
            flask.abort(500, e)
    else:
        flask.abort(400, schema.errors)


@comments.route('/', methods=['POST'])
@flask_login.login_required
@requires_permission('comments_create')
def comment_entry():

    schema = schemas.CommentSchema(data=flask.request.json)

    if schema.validate():
        try:
            comment = models.comment_create(accountid=flask.request.json('accountid'),
                                            comment=flask.request.json('commenttext'),
                                            userid=flask_login.current_user.userid)

            return flask.jsonify({'commentid': comment}), 201
        except KeyError:
            flask.abort(404)
        except Exception as e:
            flask.abort(500, e)
    else:
        flask.abort(400, schema.errors)
