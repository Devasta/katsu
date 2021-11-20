CREATE OR REPLACE VIEW vw_documents AS
    SELECT
        COALESCE(d.memberid, e.memberid) as memberid,
        a.documentid,
        a.accountid,
        a.uploaddate,
        c.accountgroup,
        a.documentname,
        a.description,
        d.savingsaccountid,
        e.loanid,
        a.uploaduserid,
        b.forename as uploaduserforename,
        b.surname as uploadusersurname
    FROM documents a
    INNER JOIN users b
    ON a.uploaduserid = b.userid
    INNER JOIN financialaccounts c
    ON a.accountID = c.accountid
    LEFT JOIN savingsaccounts d
    ON c.accountid = d.savingsaccountid
    LEFT JOIN loans e
    ON c.accountid = e.loanid;
