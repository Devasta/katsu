CREATE TABLE IF NOT EXISTS members (
    memberID integer PRIMARY KEY,
    title varchar(6),
    forename varchar(35),
    surname varchar(35),
    companyname varchar(100),
    addressline1 varchar(50) NOT NULL,
    addressline2 varchar(50),
    City varchar(50),
    County varchar(50) NOT NULL,
    Country varchar(50),
    PostCode varchar(10) NOT NULL,
    HomePhone varchar(20),
    MobilePhone varchar(20),
    DateOfBirth DATE,
    entryuserID INTEGER NOT NULL REFERENCES users (userID),
    entrydate timestamp NOT NULL DEFAULT NOW()
    --Add Check Constraints
    --1: Need Person or Company Name
    CONSTRAINT proper_contact CHECK(surname IS NOT NULL OR companyname IS NOT NULL)
);
--MemberID starting from 100001, no reason other than I think members wouldn't like to have a single
--digit number for when they are conducting their business.
CREATE SEQUENCE IF NOT EXISTS members_memberid_seq START 100001;
ALTER TABLE members ALTER COLUMN memberID SET DEFAULT nextval('members_memberid_seq');
