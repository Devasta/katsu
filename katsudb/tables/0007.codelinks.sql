--This is not a good table
--Basically, this table will provide defaults for the other side of accounting entries.
--For example: Imagine a member deposits money in the credit union. Their account will be
--credited with the money, but we need a corresponding debit to the cash account.
--The staff members will be able to specify the member account, having them keep track of the
--other side of the transaction will be messy.
--I have no idea how to do this properly. Will consult an expert some time.
CREATE TABLE IF NOT EXISTS codelinks (
    codelinkname varchar(20) PRIMARY KEY, --Some unique name
    description varchar(50) NOT NULL,   --Some unique description
    accountID integer NOT NULL REFERENCES financialaccounts(accountID)
);
