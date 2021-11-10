CREATE TYPE fintransaction AS (
    accountid integer,
    debit boolean,
    amount numeric(10,2)
);