CREATE OR REPLACE VIEW vw_userdetails AS
    SELECT
        a.userID,
        a.tokenid,
        a.memberid,
        a.email,
        a.forename,
        a.surname,
        a.password,
        a.roleID,
        b.rolename,
        b.members_get,
        b.members_create,
        b.members_update,
        b.savings_get,
        b.savings_create,
        b.savings_update,
        b.savings_withdrawalimit,
        b.loans_get,
        b.loans_create,
        b.loans_update,
        b.loans_approvelimit,
        b.configs_get,
        b.configs_create,
        b.configs_update,
        b.comments_get,
        b.comments_create
    FROM users a
    INNER JOIN roles b
    ON a.roleID = b.roleID;