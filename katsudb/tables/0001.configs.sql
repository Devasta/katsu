--Config Values table is for once off hard-coded items that don't really
--make sense anywhere else. (For example, the root directory of all documents
--mentioned in the documents table.)
CREATE TABLE IF NOT EXISTS configvalues(
    configname varchar(20) PRIMARY KEY,
    configvalue varchar(50) NOT NULL,
    description varchar(50) NOT NULL
);