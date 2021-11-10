CREATE OR REPLACE FUNCTION config_update(v_configname varchar,
                                                v_configvalue varchar,
                                                v_description varchar) RETURNS VOID as $$
BEGIN
    UPDATE configvalues
        SET configvalue = v_configvalue,
            description = v_description
    WHERE configname = v_configname;
    IF NOT FOUND
        then RAISE EXCEPTION 'Config not found' USING ERRCODE = 'P0002';
    END IF;
END;
$$ LANGUAGE plpgsql;