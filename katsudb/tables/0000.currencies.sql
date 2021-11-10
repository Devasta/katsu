CREATE TABLE IF NOT EXISTS hermes.currencies(
  currencyID char(3) PRIMARY KEY, --ISO code.
  symbol varchar(3),
  currencyname varchar(40) UNIQUE NOT NULL
);
