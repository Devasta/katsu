--Comments shared between loans and savings accounts. It'll be no trouble to add them to
--internal accounts later if needed.
CREATE TABLE IF NOT EXISTS comments(
    commentID SERIAL PRIMARY KEY,
    accountid INTEGER NOT NULL REFERENCES financialaccounts(accountID),
    entrydate timestamp DEFAULT NOW(),
    entryuserid INTEGER NOT NULL REFERENCES users(UserID),
    comment varchar(200) NOT NULL
);
CREATE INDEX IF NOT EXISTS comments_accountid_NUI on comments(accountid);
