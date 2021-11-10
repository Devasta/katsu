--transactionheaders and transactiondetails are the two tables for all transactions into the database.
--We should never edit records in these tables.
--We should never remove records from these tables, except in cases where those records
--have been archived, but even then I am not sure.
--Insert data with the fintransaction_insert() function.
CREATE TABLE IF NOT EXISTS transactiondetails (
    transactiondetailID SERIAL PRIMARY KEY,
    transactionID INTEGER NOT NULL REFERENCES transactionheaders(transactionID),
    accountID integer NOT NULL REFERENCES financialaccounts(accountID),
    debit boolean NOT NULL,
    amount numeric(10,2) NOT NULL,
    newbalance numeric(10,2) NOT NULL
);
CREATE INDEX IF NOT EXISTS transactiondetails_transactionID_NUI on transactiondetails(transactionID);
CREATE INDEX IF NOT EXISTS transactiondetails_accountID_NUI on transactiondetails(accountID);

