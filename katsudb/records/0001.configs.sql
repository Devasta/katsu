DO $$
Declare inserted_id integer;
BEGIN

    PERFORM config_create('CU_NAME', 'Demo Credit Union', 'The credit unions name.');
    PERFORM config_create('PAGINATION_COUNT', '20', 'Number of records per page');

END
$$ LANGUAGE plpgsql;