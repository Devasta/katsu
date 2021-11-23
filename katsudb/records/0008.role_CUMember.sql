DO $$
Declare inserted_id integer;
BEGIN
INSERT INTO roles
    (rolename, members_get, members_create, members_update, savings_get, savings_create, savings_update, savings_withdrawalimit, loans_get, loans_create, loans_update, loans_approvelimit, configs_get, configs_create, configs_update, comments_get, comments_create)
VALUES
    ('CU Member', True, False, False, False, False, False, 0, False, False, False, 0, False, False, False, False, False)
    returning roleid into inserted_id;
PERFORM config_create('DEFAULT_ROLEID', cast(inserted_id as varchar), 'Role ID assigned to new users');
END
$$ LANGUAGE plpgsql;
