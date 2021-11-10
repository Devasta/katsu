CREATE OR REPLACE FUNCTION codelink_update(v_codelinkname varchar,
                                                  v_accountid integer,
                                                  v_description varchar) RETURNS VOID as $$
BEGIN
    UPDATE codelinks
    SET accountID = v_accountid,
        description = v_description
    WHERE codelinkname = v_codelinkname;
    IF NOT FOUND
        then RAISE EXCEPTION 'Codelink not found' USING ERRCODE = 'P0002';
    END IF;
END;
$$ LANGUAGE plpgsql;
