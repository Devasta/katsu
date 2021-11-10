--transactionheaders and transactiondetails are the two tables for all transactions into the database.
--We should never edit records in these tables.
--We should never remove records from these tables, except in cases where those records
--have been archived, but even then I am not sure.
--Insert data with the fintransaction_insert() function.
CREATE TABLE IF NOT EXISTS transactionheaders (
    transactionID SERIAL PRIMARY KEY,
    entrydate timestamp NOT NULL DEFAULT NOW(),
    description varchar(200) NOT NULL
);