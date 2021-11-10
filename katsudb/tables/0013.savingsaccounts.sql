--Customer savings accounts.
CREATE TABLE IF NOT EXISTS savingsaccounts(
    savingsaccountID integer PRIMARY KEY REFERENCES financialaccounts(accountID),
    memberID integer NOT NULL REFERENCES members(memberID),
    Status char(1), --Active, Closed
    ClosereasonID INTEGER REFERENCES savingsaccountclosecodes(ClosereasonID),
    OpenDate timestamp,
    CloseDate timestamp
);
CREATE INDEX IF NOT EXISTS savingsaccounts_memberID_NUI on members(memberID);
