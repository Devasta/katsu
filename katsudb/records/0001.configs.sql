DO $$
Declare inserted_id integer;
BEGIN

    PERFORM config_create('CU_NAME', 'Demo Credit Union', 'The credit unions name.');

END
$$ LANGUAGE plpgsql;