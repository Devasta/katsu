--Internal accounts related to the running of the credit union.
--ACCOUNTS PAYABLE, BAD DEBT, various vendors, etc.
CREATE TABLE IF NOT EXISTS internalaccounts(
    internalaccountID integer PRIMARY KEY REFERENCES financialaccounts(accountID),
    accountname varchar(20) UNIQUE,
    description varchar(200) NOT NULL
);
