CREATE OR REPLACE FUNCTION member_update(v_memberid integer,
                                                v_title varchar,
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
                                                v_DateOfBirth date
                                        ) RETURNS VOID AS  $$
    BEGIN
        UPDATE members
            set title = v_title,
                forename = v_forename,
                surname = v_surname,
                companyname = v_companyname,
                addressline1 = v_addressline1,
                addressline2 = v_addressline2,
                City = v_City,
                County = v_County,
                Country = v_Country,
                PostCode = v_PostCode,
                HomePhone = v_HomePhone,
                MobilePhone = v_MobilePhone,
                DateOfBirth = v_DateOfBirth
        WHERE memberid = v_memberid;
        IF NOT FOUND
            then RAISE EXCEPTION 'Member not found' USING ERRCODE = 'P0002';
        END IF;
    END
$$ LANGUAGE plpgsql;
