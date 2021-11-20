CREATE OR REPLACE FUNCTION loan_update(v_loanid integer,
                                       v_loanamount numeric,
                                       v_purpose varchar,
                                       v_interestrate numeric,
                                       v_paymentamount numeric,
                                       v_nextpaymentdate date,
                                       v_paymentfrequency varchar,
                                       v_paymentmethodid varchar
                                       ) RETURNS integer AS  $$
    DECLARE
    acc record;
    BEGIN

        SELECT into acc
            loanID, amount, purpose, status FROM loans
        where loanID = v_loanID;

        IF acc.loanID IS NULL THEN
            RAISE EXCEPTION 'Loan ID not found.' USING ERRCODE = 'P0002';
        END IF;
        IF acc.status = 'C' THEN
            RAISE EXCEPTION 'Loan is closed and cannot be amended.' USING ERRCODE = 'P0001';
        end if;
        IF acc.status <> 'P' and (acc.amount <> v_loanamount or acc.purpose <> v_purpose) THEN
            RAISE EXCEPTION 'Loan amount or purpose cannot be amended after approval.' USING ERRCODE = 'P0002';
        END IF;
--        IF v_paymentmethodid NOT IN (select paymentmethodid from paymentmethods)
--            THEN RAISE EXCEPTION 'Invalid payment method ID.' USING ERRCODE ='P0002';
--        END IF;

        UPDATE loans
            SET amount = v_loanamount,
                purpose = v_purpose,
                interestrate = v_interestrate,
                paymentamount = v_paymentamount,
                nextpaymentdate = v_nextpaymentdate,
                paymentfrequency = v_paymentfrequency,
                paymentmethodID = v_paymentmethodid
            WHERE loanid = v_loanid;

        IF NOT FOUND
            then RAISE EXCEPTION 'Loan ID not found.' USING ERRCODE = 'P0002';
        END IF;

        RETURN v_loanid;
    END
$$ LANGUAGE plpgsql;