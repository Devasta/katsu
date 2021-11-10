CREATE OR REPLACE VIEW vw_member AS
    SELECT
        memberid,
        title,
        forename,
        surname,
        companyname,
        addressline1,
        addressline2,
        city,
        county,
        country,
        postcode,
        homephone,
        mobilephone,
        dateofbirth,
        entrydate,
        entryuserid
    FROM members;