
CREATE OR REPLACE VIEW vw_loans AS
    SELECT
        a.loanID,
        a.memberID,
        a.purpose,
        a.ApplicationDate,
        a.StartDate,
        a.CloseDate,
        a.amount,
        a.approvaldate,
        a.approvaluser,
        a.interestrate,
        a.outstandingloanamount,
        a.paymentamount,
        a.paymentmethodid,
        e.description as paymentmethod,
        a.paymentfrequency,
        b.currentbalance,
        b.entrydate,
        c.loanstatusid as statusid,
        c.description as status,
        d.forename as approvalforename,
        d.surname as approvalsurname
    FROM loans a
    INNER JOIN financialaccounts b
    ON a.loanID = b.accountID
    INNER JOIN loanstatuscodes c
    ON a.status = c.loanstatusid
    LEFT JOIN users d
    ON a.approvaluser = d.userID
    LEFT JOIN paymentmethods e
    on a.paymentmethodid = e.paymentmethodid;
