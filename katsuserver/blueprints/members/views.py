import flask
import flask_login
from . import members
from . import forms
from . import models

from ...models import requires_permission, get_config
import psycopg2


@members.route('/', methods=['GET'])
@flask_login.login_required
@requires_permission('members_get')
def membersearch():
    """
        Allows the user to search for members. Note: We might externalise such an API call in future so it checks
        if the user has a memberid, and if it does overrides search criteria to only return that member ID.
    """
    form = forms.membersearchform(formdata=flask.request.args)

    # If the user does not provide a pagenumber or provides something that is not an integer, we just set to 1.
    try:
        if flask.request.args.get('page') > 1:
            page = int(flask.request.args.get('page'))
        else:
            page = 1
    except TypeError:
        page = 1

    limit = flask.request.args.get('limit') or get_config('PAGINATION_COUNT')['configvalue']
    if form.validate():
        try:
            if flask_login.current_user.memberid:
                memberid = flask_login.current_user.memberid
            elif form.memberid.data == '':
                memberid = None
            else:
                memberid = form.memberid.data

            memberslist = models.member_get(memberid=memberid,
                                            surname=None if form.surname.data == '' else form.surname.data,
                                            addressline1=None if form.addressline1.data == '' else form.addressline1.data,
                                            county=None if form.county.data == '' else form.county.data,
                                            postcode=None if form.postcode.data == '' else form.postcode.data,
                                            offset=((page - 1)*int(limit)),
                                            limit=int(limit)
                                            )
            if len(memberslist) == 0:
                return '', 204
            return flask.jsonify({'members': memberslist}), 200
        except Exception as e:
            flask.abort(500, e)
    else:
        flask.abort(400, form.errors)


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

    form = forms.memberdetailsform.from_json(flask.request.json)

    if form.validate():
        try:
            newid = models.member_create(entryuserid=flask_login.current_user.userid,
                                         title=form.title.data,
                                         forename=form.forename.data,
                                         surname=form.surname.data,
                                         companyname=form.companyname.data,
                                         addressline1=form.addressline1.data,
                                         addressline2=form.addressline2.data,
                                         city=form.city.data,
                                         county=form.county.data,
                                         country=form.country.data,
                                         postcode=form.postcode.data,
                                         homephone=form.homephone.data,
                                         mobilephone=form.mobilephone.data,
                                         dateofbirth=form.dateofbirth.data,
                                         gender=form.gender.data
                                         )

            return flask.jsonify({'memberid': newid}), 201
        except Exception as e:
            flask.abort(500, e)
    else:
        flask.abort(400, form.errors)


@members.route('/<int:memberid>/', methods=['PUT'])
@flask_login.login_required
@requires_permission('members_update')
def member_update(memberid):

    form = forms.memberdetailsform.from_json(flask.request.json)

    if form.validate():
        try:
            models.member_update(memberid=memberid,
                                 title=form.title.data,
                                 forename=form.forename.data,
                                 surname=form.surname.data,
                                 companyname=form.companyname.data,
                                 addressline1=form.addressline1.data,
                                 addressline2=form.addressline2.data,
                                 city=form.city.data,
                                 county=form.county.data,
                                 country=form.country.data,
                                 postcode=form.postcode.data,
                                 homephone=form.homephone.data,
                                 mobilephone=form.mobilephone.data,
                                 dateofbirth=form.dateofbirth.data,
                                 gender=form.gender.data
                                 )
            return '', 204
        except KeyError as e:
            flask.abort(404)
        except Exception as e:
            flask.abort(500, e)
    else:
        flask.abort(400, form.errors)
