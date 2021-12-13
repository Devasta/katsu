CREATE OR REPLACE FUNCTION savingsaccount_create(v_memberID integer,
                                                 v_currency varchar) RETURNS integer AS  $$
    DECLARE inserted_id integer;
    BEGIN
        INSERT INTO financialaccounts(accounttype,accountgroup, currency)
            VALUES ('L', 'SAVE', v_currency)
        RETURNING accountid INTO inserted_id;

        INSERT INTO savingsaccounts(savingsaccountID, memberid, status, opendate)
            VALUES (inserted_id, v_memberID, 'A', NOW());

        RETURN inserted_id;
    END
$$ LANGUAGE plpgsql;