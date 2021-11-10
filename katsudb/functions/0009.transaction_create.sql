CREATE OR REPLACE FUNCTION transaction_create(v_description text,
                                                     v_transactions fintransaction[]
                                                     ) RETURNS integer AS $$
    DECLARE
        inserted_id integer;
        debitcreditbalance numeric(10,2);
        newbal numeric(10,2);
        t fintransaction;
        acc record;
    BEGIN

        debitcreditbalance = 0;

        FOREACH t IN ARRAY v_transactions
            LOOP
                IF t.amount = 0 THEN
                    RAISE EXCEPTION 'Amount cannot be zero.';
                END IF;
                IF t.debit IS TRUE
                    THEN debitcreditbalance = debitcreditbalance + t.amount;
                    ELSE debitcreditbalance = debitcreditbalance - t.amount;
                END IF;
        END LOOP;

        IF debitcreditbalance <> 0 THEN
            RAISE EXCEPTION 'Debit and Credit totals do not match!';
        END IF;

        INSERT INTO transactionheaders(description)
            VALUES (v_description)
            RETURNING transactionid INTO inserted_id;

        FOREACH t IN ARRAY v_transactions
            LOOP
                select INTO acc
                    a.currentbalance,
                    b.debitincrease
                FROM financialaccounts a
                INNER JOIN accounttypes b
                on a.accounttype = b.accounttype
                WHERE a.accountid = t.accountid;

            IF t.debit = acc.debitincrease
                THEN newbal = acc.currentbalance + t.amount;
                ELSE newbal = acc.currentbalance - t.amount;
            END IF;

            UPDATE financialaccounts
            SET currentbalance = newbal
            WHERE financialaccounts.accountID = t.accountID;

            INSERT INTO transactiondetails(transactionID, accountID, debit, amount, newbalance)
            VALUES (inserted_id, t.accountid, t.debit, t.amount, newbal);

        END LOOP;

        RETURN inserted_id;
    END
$$ LANGUAGE plpgsql;