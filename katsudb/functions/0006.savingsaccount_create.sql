CREATE OR REPLACE FUNCTION savingsaccount_create(v_memberID integer) RETURNS integer AS  $$
    DECLARE inserted_id integer;
    BEGIN
        INSERT INTO financialaccounts(accounttype,accountgroup)
            VALUES ('L', 'SAVE')
        RETURNING accountid INTO inserted_id;

        INSERT INTO savingsaccounts(savingsaccountID, memberid, status, opendate)
            VALUES (inserted_id, v_memberID, 'A', NOW());

        RETURN inserted_id;
    END
$$ LANGUAGE plpgsql;