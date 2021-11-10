CREATE OR REPLACE VIEW vw_savingsaccounts AS
    SELECT
        sva.savingsaccountID,
        sva.Status,
        sva.OpenDate,
        sva.CloseDate,
        fa.currentbalance,
        fa.entrydate,
        sva.memberid
    FROM savingsaccounts sva
    INNER JOIN financialaccounts fa
    ON sva.savingsaccountID = fa.accountID;