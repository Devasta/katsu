CREATE OR REPLACE FUNCTION loan_status_update(v_loanid integer,
                                              v_status varchar,
                                              v_userid integer,
                                              v_closereason integer default null,
                                              v_savingsaccountid integer default null
                                                ) RETURNS VOID AS $$
    DECLARE
    loanacc record;
    useracc record;
    savingacc record;
    BEGIN

        SELECT into loanacc
            loanID, memberid, statusid, amount, currentbalance, interestrate, paymentamount,paymentmethod FROM vw_loans
        where loanID = v_loanID;

        IF loanacc.loanID IS NULL THEN
            RAISE EXCEPTION 'Loan ID not found.' USING ERRCODE = 'P0002';
        END IF;
        IF loanacc.statusid = 'C' THEN
            RAISE EXCEPTION 'Loan is closed and cannot be amended.' USING ERRCODE = 'P0001';
        END IF;

        IF loanacc.statusid = v_status THEN
            RAISE EXCEPTION 'Loan is already on that status.' USING ERRCODE = 'P0001';
        END IF;

        IF loanacc.statusid = 'A' and v_status <> 'C' THEN
            RAISE EXCEPTION 'Loan repayments are already active, cannot change status.' USING ERRCODE = 'P0001';
        END IF;

        --If Loan is being closed, make sure a reason is populated.
        IF v_status = 'C' THEN
            IF v_closereason IS NULL THEN
                RAISE EXCEPTION 'Need cancellation reason to close loan.' USING ERRCODE = 'P0001';
            END IF;

            IF coalesce(loanacc.currentbalance, 0) > 0 THEN
                RAISE EXCEPTION 'Cannot close loan, balance outstanding' USING ERRCODE = 'P0001';
            END IF;

            UPDATE loans
                SET status = 'C',
                    closereason = v_closereason,
                    closedate = now()
                WHERE loans.loanid = v_loanid;
            IF NOT FOUND
                then RAISE EXCEPTION 'Loan ID not found.' USING ERRCODE = 'P0002';
            END IF;

            PERFORM comment_create(v_loanid, v_userid, 'Loan Closed.');

        END IF;

        IF loanacc.statusid = 'P' and v_status = 'A' THEN
            RAISE EXCEPTION 'Loan must be approved before loan can be activated.' USING ERRCODE = 'P0001';
        END IF;
        --If the loan is being approved, do a quick check to make sure the user has the approval limit to do so.
        IF loanacc.statusid = 'P' and v_status = 'D' THEN

            IF coalesce(loanacc.amount,0) <= 0 THEN
                RAISE EXCEPTION 'Cannot approve, no loan amount set.' USING ERRCODE = 'P0001';
            END IF;
            IF coalesce(loanacc.interestrate,0) <= 0 THEN
                RAISE EXCEPTION 'Cannot approve, check interest rate.' USING ERRCODE = 'P0001';
            END IF;
            IF coalesce(loanacc.paymentamount,0) <= 0 THEN
                RAISE EXCEPTION 'Cannot approve, check repayment amount.' USING ERRCODE = 'P0001';
            END IF;

            SELECT into useracc
                coalesce(loans_approvelimit, 0) as loanapprovelimit
            from vw_userdetails
                where userid = v_userid;

            IF useracc.loanapprovelimit < loanacc.amount THEN
                RAISE EXCEPTION 'User loan approval limit is %', useracc.loanapprovelimit USING ERRCODE = 'P0001';
            END IF;

            UPDATE loans
                SET status = v_status,
                    approvaluser = v_userid ,
                    approvaldate = now()
                WHERE loans.loanid = v_loanid;
            IF NOT FOUND
                then RAISE EXCEPTION 'Loan ID not found.' USING ERRCODE = 'P0002';
            END IF;

            PERFORM comment_create(v_loanid, v_userid, 'Loan Status updated from ' || loanacc.statusid || ' to ' || v_status);
        END IF;

        IF loanacc.statusid = 'D' and v_status = 'A' THEN

            IF loanacc.paymentmethod IS NULL THEN
                RAISE EXCEPTION 'No repayment method configured' USING ERRCODE = 'P0001';
            end if;
            IF v_savingsaccountid IS NULL THEN
                RAISE EXCEPTION 'No Savings Account ID provided' USING ERRCODE = 'P0001';
            END IF;

            SELECT into savingacc
                savingsaccountid, memberid
            from savingsaccounts
            where savingsaccountid = v_savingsaccountid;

            IF savingacc.savingsaccountid IS NULL THEN
                RAISE EXCEPTION 'Invalid Savings Account ID provided' USING ERRCODE = 'P0002';
            END IF;

            IF savingacc.memberid <> loanacc.memberid THEN
                RAISE EXCEPTION 'Savings Account member ID does not match loan.' USING ERRCODE = 'P0002';
            END IF;

            UPDATE loans
                SET status = v_status,
                    outstandingloanamount = loanacc.amount
                WHERE loans.loanid = v_loanid;
            IF NOT FOUND
                then RAISE EXCEPTION 'Loan ID not found.' USING ERRCODE = 'P0002';
            END IF;

            PERFORM transaction_create('Approval - Loan '|| v_loanid,
                                        array[
                                                (v_loanid, True, loanacc.amount),
                                                (savingacc.savingsaccountid, False, loanacc.amount)
                                                ]::fintransaction[]
                                        );

            PERFORM comment_create(v_loanid, v_userid, 'Loan Status updated from ' || loanacc.statusid || ' to ' || v_status);
        END IF;

    END
$$ LANGUAGE plpgsql;