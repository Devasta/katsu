import flask
import flask_login
from . import members
from . import schemas
from . import models

from ...models import requires_permission, get_config


@members.route('/', methods=['GET'])
@flask_login.login_required
@requires_permission('members_get')
def membersearch():
    """
        Allows the user to search for members. Note: We might externalise such an API call in future so it checks
        if the user has a memberid, and if it does overrides search criteria to only return that member ID.
    """
    schema = schemas.membersearchschema(data=flask.request.args)

    # If the user does not provide a pagenumber or provides something that is not an integer, we just set to 1.
    try:
        if flask.request.args.get('page') > 1:
            page = int(flask.request.args.get('page'))
        else:
            page = 1
    except TypeError:
        page = 1

    limit = flask.request.args.get('limit') or get_config('PAGINATION_COUNT')['configvalue']
    if schema.validate():
        try:
            if flask_login.current_user.memberid:
                memberid = flask_login.current_user.memberid
            else:
                memberid = flask.request.args.get('memberid')

            memberslist = models.member_get(memberid=memberid,
                                            surname=flask.request.args.get('surname'),
                                            addressline1=flask.request.args.get('addressline1'),
                                            county=flask.request.args.get('county'),
                                            postcode=flask.request.args.get('postcode'),
                                            offset=((page - 1)*int(limit)),
                                            limit=int(limit)
                                            )
            if len(memberslist) == 0:
                return '', 204
            return flask.jsonify({'members': memberslist}), 200
        except Exception as e:
            flask.abort(500, e)
    else:
        flask.abort(400, schema.errors)


@members.route('/<int:memberid>/', methods=['GET'])
@flask_login.login_required
@requires_permission('members_get')
def member_main(memberid):
    """
        Allows the user to get member details. Note: We might externalise such an API call in future so it checks
        if the user has a memberid, and if it does overrides search criteria to only return that member ID.
    """
    if flask_login.current_user.memberid == memberid:
        member = models.member_get(memberid=memberid)
    elif flask_login.current_user.memberid is None:
        member = models.member_get(memberid=memberid)
    else:
        flask.abort(403)

    if len(member) == 0:
        flask.abort(404)
    else:
        return flask.jsonify({'member': member[0]}), 200


@members.route('/', methods=['POST'])
@flask_login.login_required
@requires_permission('members_create')
def new_member_entry():

    schema = schemas.memberdetailsschema(data=flask.request.json)

    if schema.validate():
        try:
            newid = models.member_create(entryuserid=flask_login.current_user.userid,
                                         title=flask.request.json.get('title'),
                                         forename=flask.request.json.get('forename'),
                                         surname=flask.request.json.get('surname'),
                                         companyname=flask.request.json.get('companyname'),
                                         addressline1=flask.request.json.get('addressline1'),
                                         addressline2=flask.request.json.get('addressline2'),
                                         city=flask.request.json.get('city'),
                                         county=flask.request.json.get('county'),
                                         country=flask.request.json.get('country'),
                                         postcode=flask.request.json.get('postcode'),
                                         homephone=flask.request.json.get('homephone'),
                                         mobilephone=flask.request.json.get('mobilephone'),
                                         dateofbirth=flask.request.json.get('dateofbirth')
                                         )

            return flask.jsonify({'memberid': newid}), 201
        except Exception as e:
            flask.abort(500, e)
    else:
        flask.abort(400, schema.errors)


@members.route('/<int:memberid>/', methods=['PUT'])
@flask_login.login_required
@requires_permission('members_update')
def member_update(memberid):

    schema = schemas.memberdetailsschema(data=flask.request.json)

    if schema.validate():
        try:
            models.member_update(title=flask.request.json.get('title'),
                                 forename=flask.request.json.get('forename'),
                                 surname=flask.request.json.get('surname'),
                                 companyname=flask.request.json.get('companyname'),
                                 addressline1=flask.request.json.get('addressline1'),
                                 addressline2=flask.request.json.get('addressline2'),
                                 city=flask.request.json.get('city'),
                                 county=flask.request.json.get('county'),
                                 country=flask.request.json.get('country'),
                                 postcode=flask.request.json.get('postcode'),
                                 homephone=flask.request.json.get('homephone'),
                                 mobilephone=flask.request.json.get('mobilephone'),
                                 dateofbirth=flask.request.json.get('dateofbirth')
                                 )
            return '', 204
        except KeyError as e:
            flask.abort(404)
        except Exception as e:
            flask.abort(500, e)
    else:
        flask.abort(400, schema.errors)
