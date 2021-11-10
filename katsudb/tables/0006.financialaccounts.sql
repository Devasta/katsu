--Primary Account table to which all other transactions link. Every single account
--in the Database (Saving, Loan, Internal, etc.) has a unique ID generated from this table.
CREATE TABLE IF NOT EXISTS financialaccounts (
    accountID SERIAL PRIMARY KEY,
    accounttype char(1) NOT NULL REFERENCES accounttypes(accounttype),
    accountgroup char(4) NOT NULL, --SAVE, LOAN, INTL.
    entrydate timestamp NOT NULL DEFAULT NOW(),
    currentbalance numeric(10,2) NOT NULL DEFAULT 0,
    currency char(3) NOT NULL REFERENCES currencies(currencyID)
  );
CREATE INDEX IF NOT EXISTS financialaccounts_accountype_NUI on financialaccounts(accounttype);
