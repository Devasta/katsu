CREATE OR REPLACE FUNCTION comment_create(v_accountid integer,
                                                 v_userid integer,
                                                 v_comment varchar
                                                ) RETURNS INTEGER AS $$
DECLARE inserted_id integer;
BEGIN
    INSERT INTO comments(accountid, entrydate, entryuserid, comment)
        VALUES(v_accountid, NOW(), v_userid, v_comment)
    RETURNING commentid into inserted_id;

    RETURN inserted_id;
END;
$$ LANGUAGE plpgsql;
