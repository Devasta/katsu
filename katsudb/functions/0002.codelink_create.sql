CREATE OR REPLACE FUNCTION codelink_create(v_codelinkname varchar,
                                                  v_accountid integer,
                                                  v_description varchar) RETURNS VOID as $$
BEGIN

    INSERT INTO codelinks(codelinkname, description, accountID)
    VALUES (v_codelinkname, v_description, v_accountid);

END;
$$ LANGUAGE plpgsql;


