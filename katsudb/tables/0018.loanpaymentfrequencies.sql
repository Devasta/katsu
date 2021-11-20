--Payment frequencies for loans. Uses Postgres interval functionality to determine.
CREATE TABLE IF NOT EXISTS loanpaymentfrequencies(
    frequencyID char(1) PRIMARY KEY,
    description varchar(11) NOT NULL,
    paymentinterval varchar(20) NOT NULL, --Postgres intervals only.
    timesperyear INTEGER
);