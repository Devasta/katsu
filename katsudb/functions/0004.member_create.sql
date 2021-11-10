CREATE OR REPLACE FUNCTION member_create(v_title varchar,
                                                v_forename varchar,
                                                v_surname varchar,
                                                v_companyname varchar,
                                                v_addressline1 varchar,
                                                v_addressline2 varchar,
                                                v_City varchar,
                                                v_County varchar,
                                                v_Country varchar,
                                                v_PostCode varchar,
                                                v_HomePhone varchar,
                                                v_MobilePhone varchar,
                                                v_DateOfBirth date,
                                                v_entryuserid integer) RETURNS INTEGER AS $$
declare inserted_id integer;
    BEGIN
        INSERT INTO members(title, forename, surname, companyname, addressline1,
                                   addressline2, City, County, Country, PostCode,
                                   HomePhone, MobilePhone, DateOfBirth, entryuserid)
        VALUES(v_title, v_forename, v_surname, v_companyname,
               v_addressline1, v_addressline2, v_City, v_County,
               v_Country, v_PostCode, v_HomePhone, v_MobilePhone,
               v_DateOfBirth, v_entryuserid)
        returning memberid into inserted_id;

        RETURN inserted_id;
    END
$$ language plpgsql;