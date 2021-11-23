--Sample Roles. Must be updated to reflect real positions in CU.

--There is another file that handled the default role for the credit union member, it will also populate the configuration table.

INSERT INTO roles
    (rolename, members_get, members_create, members_update, savings_get, savings_create, savings_update, savings_withdrawalimit, loans_get, loans_create, loans_update, loans_approvelimit, configs_get, configs_create, configs_update, comments_get, comments_create)
VALUES
    ('Member Services Officer', True, True, True, True, True, True, 1000,True, False, False, 0, False, False, False, True, True),
    ('Loan Officer',True, False, False, True, False, False, 0,True, True, True, 5000, True, False, False, True, True),
    ('Manager', True, True, True, True, True, True, 5000, True, True, True, 0, True, False, False, True, True),
    ('Auditor', True, False, False, True, False, False, 0, True, False, False, 0, True, False, False, True, False),
    ('Sysadmin', False, False, False, False, False, False, 0, False, False, False, 0, True, True, True, False, False);
