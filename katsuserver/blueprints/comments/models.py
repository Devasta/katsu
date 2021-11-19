import flask


def comments_get(accountid=None, memberid=None, offset=0, limit=None):
    with flask.current_app.db.db_cursor() as cur:
        cur.execute(""" SELECT
                            commentid,
                            accountid,
                            memberid,
                            entrydate,
                            comment,
                            entryuserid,
                            entryuserforename,
                            entryusersurname
                        FROM vw_comments
                        WHERE (%(accountid)s IS NULL or accountid = %(accountid)s)
                            AND (%(memberid)s IS NULL or memberid = %(memberid)s)
                        ORDER BY entrydate
                        OFFSET %(offset)s
                        LIMIT %(limit)s
        """, {'accountid': accountid,
              'memberid': memberid,
              'offset': offset,
              'limit': limit})
        comments = cur.fetchall()
        return comments


def comment_create(accountid, comment, userid):
    with flask.current_app.db.db_cursor() as cur:
        cur.execute("""SELECT comment_create(%(accountid)s, %(userid)s, %(comment)s)""",
                    {'accountid': accountid,
                     'userid': userid,
                     'comment': comment})
        commentID = cur.fetchone()

    return commentID
