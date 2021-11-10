--+---------------------------------------------------+
--|               The rules of the game               |
--+-----------------------------+----------+----------+
--|        Account Type         |  Debit   |  Credit  |
--+-----------------------------+----------+----------+
--| Assets                      | Increase | Decrease |
--| Liabilities                 | Decrease | Increase |
--| Equity                      | Decrease | Increase |
--| Income                      | Decrease | Increase |
--| Expenses                    | Increase | Decrease |
--+-----------------------------+----------+----------+
--| Assets = Liabilities + Equity + Income - Expenses |
--+-----------------------------+----------+----------+
CREATE TABLE IF NOT EXISTS accounttypes (
    accounttype char(1) PRIMARY KEY,
    description varchar(9) NOT NULL,
    debitincrease boolean
    CONSTRAINT UPPERCASE_TYPE_ONLY CHECK (accounttype ~ '[A-Z0-9]{1,1}')
);