CREATE TABLE IF NOT EXISTS loans(
    loanID integer PRIMARY KEY REFERENCES financialaccounts(accountID),
    memberID integer NOT NULL REFERENCES members(memberID),
    ApplicationDate DATE NOT NULL,
    amount numeric(10,2) NOT NULL CONSTRAINT positive_loanamount CHECK (amount > 0),
    approvaldate DATE,
    approvaluser integer REFERENCES users(userID),
    purpose varchar(100) NOT NULL,
    StartDate DATE,
    CloseDate DATE,
    outstandingloanamount numeric(10,2) CONSTRAINT positive_outstandingloanamount CHECK (outstandingloanamount >= 0),
    interestrate numeric(10,2),
    paymentmethodID char(2) references paymentmethods(paymentmethodID),
    paymentamount numeric(10,2) CONSTRAINT positive_paymentamount CHECK (paymentamount > 0),
    nextpaymentdate DATE,
    paymentfrequency char(1) REFERENCES loanpaymentfrequencies(frequencyID),
    status char(1) NOT NULL REFERENCES loanstatuscodes(loanstatusid),
    closereason integer REFERENCES loanclosecodes(closereasonid)
);
CREATE INDEX IF NOT EXISTS  loans_memberID_NUI on loans(memberID);