import flask
import os
import werkzeug.utils


def documents_get(accountid=None, memberid=None, documentid=None, offset=0, limit=None):
    with flask.current_app.db.db_cursor() as cur:
        cur.execute(""" SELECT
                            memberid,
                            documentid,
                            accountid,
                            uploaddate,
                            documentname,
                            description,
                            uploaduserid,
                            uploaduserforename,
                            uploadusersurname
                        FROM vw_documents
                        WHERE (%(documentid)s IS NULL or documentid = %(documentid)s)
                        AND (%(accountid)s IS NULL or accountID = %(accountid)s)
                        AND (%(memberid)s IS NULL or memberid = %(memberid)s)    
                        ORDER BY documentid
                        OFFSET %(offset)s
                        LIMIT %(limit)s
        """, {'accountid': accountid,
              'documentid': documentid,
              'memberid': memberid,
              'offset': offset,
              'limit': limit})
        documents = cur.fetchall()
        return documents


def document_create(accountid, file, description, directory, uploaduserid):
    with flask.current_app.db.db_cursor() as cur:
        directory = os.path.join(directory, str(accountid))

        os.makedirs(directory, exist_ok=True)

        cur.execute("""SELECT document_create(%(accountid)s,
                                             %(userid)s,
                                             %(documentname)s,
                                             %(description)s) as new_DocID""",
                        {
                         'accountid': accountid,
                         'userid': uploaduserid,
                         'documentname': werkzeug.utils.secure_filename(file.filename),
                         'description': description
                        }
                    )

        docID = cur.fetchone()
        file.save(os.path.join(directory, str(docID['new_docid'])))

    return docID
