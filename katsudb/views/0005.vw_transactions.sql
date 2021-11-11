CREATE OR REPLACE VIEW vw_transactions AS
SELECT
    a.transactionid,
    a.transactiondetailid,
    b.entrydate,
    b.description,
    a.accountid,
    a.debit,
    case
        WHEN e.debitincrease and a.debit THEN a.amount
        WHEN NOT e.debitincrease and NOT a.debit THEN a.amount
        WHEN e.debitincrease and NOT a.debit THEN a.amount * -1
        WHEN NOT e.debitincrease and a.debit THEN a.amount * -1
    end AS amount,
    a.newbalance
FROM transactiondetails a
INNER JOIN transactionheaders b
ON a.transactionid = b.transactionid
INNER JOIN financialaccounts c
ON a.accountid = c.accountid
LEFT JOIN accounttypes e
ON c.accounttype = e.accounttype;
