--Need to seriously consider revising this.
--Should I instead have one-many relation to a separate permissions table?
CREATE TABLE IF NOT EXISTS roles (
    roleID SERIAL PRIMARY KEY,
    rolename varchar(40) UNIQUE,
    members_get boolean NOT NULL,
    members_create boolean NOT NULL,
    members_update boolean NOT NULL,
    savings_get boolean NOT NULL,
    savings_create boolean NOT NULL,
    savings_update boolean NOT NULL,
    savings_withdrawalimit numeric(10,2) NOT NULL,
    loans_get boolean NOT NULL,
    loans_create boolean NOT NULL,
    loans_update boolean NOT NULL,
    loans_approvelimit numeric(10,2) NOT NULL,
    configs_get boolean NOT NULL,
    configs_create boolean NOT NULL,
    configs_update boolean NOT NULL,
    comments_get boolean NOT NULL,
    comments_create boolean NOT NULL
);
