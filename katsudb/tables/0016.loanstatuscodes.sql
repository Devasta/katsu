--These codes are important indicators for certain processes.
--For example, Direct Debit collections will only generate for loans with a status 'A'.
--Same with interest accruals.
CREATE TABLE IF NOT EXISTS loanstatuscodes(
    loanstatusid char(1) PRIMARY KEY,
    description varchar(30) NOT NULL
);