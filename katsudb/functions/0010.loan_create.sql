CREATE OR REPLACE FUNCTION loan_create(v_memberID integer,
                                       v_loanamount numeric,
                                       v_purpose varchar) RETURNS integer AS  $$
DECLARE inserted_id integer;
    BEGIN
        INSERT INTO financialaccounts(accounttype,accountgroup)
        VALUES ('A', 'LOAN')
        RETURNING accountid INTO inserted_id;

        INSERT INTO loans(loanID, memberid, applicationdate, amount, purpose, status)
            VALUES (inserted_id, v_memberID, NOW(), v_loanamount, v_purpose, 'P');

        RETURN inserted_id;
    END
$$ LANGUAGE plpgsql;