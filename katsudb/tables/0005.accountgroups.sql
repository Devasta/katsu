--SAVE - Savings Accounts
--LOAN - Loan Accounts
--INTL - Internal accounts.
--Don't think we need anything else.
CREATE TABLE IF NOT EXISTS accountgroups (
    accounttype char(4) PRIMARY KEY --SAVE, LOAN, INTL
    CONSTRAINT UPPERCASE_TYPE_ONLY CHECK (accounttype ~ '[A-Z0-9]{4,4}')
);