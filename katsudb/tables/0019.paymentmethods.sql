CREATE TABLE IF NOT EXISTS paymentmethods(
  paymentmethodID char(2) PRIMARY KEY,
  description varchar(100) NOT NULL,
  --Add Check Constraints
  --1: Only uppercase codes.
  CONSTRAINT UPPERCASE_PM_ONLY CHECK (paymentmethodID ~ '[A-Z0-9]{2,2}')
);