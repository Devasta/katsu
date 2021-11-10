--To ensure that filenames are always unique, files are stored as follows:
--The DOCUMENT_ARCHIVE setting in the configvalues table is the main directory.
--Then there is a subdirectory for each accountid to ensure the directory doesn't become unmanageable.
--The files are stored with documentid as the name, to ensure they are unique. We store the actual filename in the DB.
CREATE TABLE IF NOT EXISTS documents(
    documentID SERIAL PRIMARY KEY,
    accountid INTEGER NOT NULL REFERENCES financialaccounts(accountID),
    uploaddate timestamp NOT NULL DEFAULT NOW(),
    uploaduserid INTEGER NOT NULL REFERENCES users(UserID),
    documentname varchar(255) NOT NULL,
    description varchar(1000)
);
CREATE INDEX documents_accountid_NUI on documents(accountid);

