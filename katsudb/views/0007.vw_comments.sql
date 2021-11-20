CREATE OR REPLACE VIEW vw_comments AS
    SELECT
        a.commentid,
        a.accountid,
        a.entrydate,
        a.comment,
        a.entryuserid,
        b.forename as entryuserforename,
        b.surname as entryusersurname,
        d.savingsaccountid,
        e.loanid,
        COALESCE(d.memberid, e.memberid) as memberid
    FROM comments a
    INNER JOIN users b
    ON a.entryuserid = b.userid
    INNER JOIN financialaccounts c
    ON a.accountID = c.accountid
    LEFT JOIN savingsaccounts d
    ON c.accountid = d.savingsaccountid
    LEFT JOIN loans e
    ON c.accountid = e.loanid;

