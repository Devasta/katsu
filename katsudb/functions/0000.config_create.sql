CREATE OR REPLACE FUNCTION config_create(v_configname varchar,
                                                v_configvalue varchar,
                                                v_description varchar) RETURNS VOID as $$
BEGIN

    INSERT INTO configvalues(configname, configvalue, description)
        VALUES(v_configname, v_configvalue, v_description);

END;
$$ LANGUAGE plpgsql;
