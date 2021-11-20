import flask
import flask_login
from . import documents
from . import forms
from . import models
import os

from ...models import requires_permission, get_config

# Important Note:
# There is no scenario where someone should want to delete or edit these files, so it will not be implemented.
# Any deletion of files should be done as part of some sort of archiving project.


@documents.route('/', methods=['GET'])
@flask_login.login_required
def document_search():

    form = forms.documentsearchform(flask.request.args)

    if form.validate():
        try:
            try:
                if flask.request.args.get('page') > 1:
                    page = int(flask.request.args.get('page'))
                else:
                    page = 1
            except TypeError:
                page = 1

            limit = flask.request.args.get('limit') or get_config('PAGINATION_COUNT')['configvalue']

            documents = models.documents_get(
                                             accountid=form.accountid.data,
                                             memberid=form.memberid.data,
                                             offset=((page - 1)*int(limit)),
                                             limit=int(limit)
                                             )
            if len(documents) ==0:
                return '', 204
            else:
                return flask.jsonify({'documents': documents}), 200
        except Exception as e:
            flask.abort(500, e)
    else:
        flask.abort(400, form.errors)


@documents.route('/<int:documentid>/', methods=['GET'])
@flask_login.login_required
def document_download(documentid):

    doc = models.documents_get(documentid=documentid)[0]
    if doc is None:
        flask.abort(404)
    else:
        try:
            directory = get_config('DOCUMENT_ARCHIVE')['configvalue']

            return flask.send_from_directory(directory=os.path.join(directory, str(doc['accountid'])),
                                             filename=str(documentid),
                                             as_attachment=True,
                                             attachment_filename=str(doc['documentname'])
                                             ), 200
        except Exception as e:
            flask.abort(500, e)


@documents.route('/', methods=['POST'])
@flask_login.login_required
def document_upload():

    form = forms.documentuploadform()

    if form.validate():
        try:
            directory = get_config('DOCUMENT_ARCHIVE')['configvalue']

            newid = models.document_create(
                                           accountid=form.accountid.data,
                                           file=form.document.data,
                                           description=form.description.data,
                                           directory=directory,
                                           uploaduserid=flask_login.current_user.userid
                                           )
            return flask.jsonify({'DocumentID': newid}), 201
        except Exception as e:
            flask.abort(500, e)
    else:
        flask.abort(400, form.errors)
