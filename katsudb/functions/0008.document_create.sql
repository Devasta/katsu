CREATE OR REPLACE FUNCTION document_create(v_accountid INTEGER,
                                                  v_uploaduserid INTEGER,
                                                  v_documentname varchar,
                                                  v_description varchar) RETURNS INTEGER AS $$
    DECLARE v_inserted_id INTEGER;
    --Incomplete function. This function merely logs the details of the file in the database.
    --The python model deals with the file storage.
    BEGIN
        INSERT INTO documents(accountid, uploaduserid,  documentname, description)
            VALUES (v_accountid, v_uploaduserid, v_documentname, v_description)
            RETURNING documentid into v_inserted_id;
        RETURN v_inserted_id;
    END
$$ LANGUAGE plpgsql;
