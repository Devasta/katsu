CREATE OR REPLACE FUNCTION internalaccount_create(v_insertaccounttype varchar,
                                                    v_insertaccountgroup varchar,
                                                    v_insertaccountname varchar,
                                                    v_insertdescription varchar,
                                                    v_currency varchar) RETURNS integer AS  $$
  DECLARE inserted_id integer;
  BEGIN
    INSERT INTO financialaccounts(accounttype,accountgroup, currency)
      VALUES (v_insertaccounttype, v_insertaccountgroup, v_currency)
      RETURNING accountid INTO inserted_id;

    INSERT INTO internalaccounts(internalaccountID, accountname, description)
      VALUES (inserted_id, v_insertaccountname, v_insertdescription);

    RETURN inserted_id;
  END
$$ LANGUAGE plpgsql;

