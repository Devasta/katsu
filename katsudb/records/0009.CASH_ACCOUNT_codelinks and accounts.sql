DO $$
Declare inserted_id integer;
BEGIN

    --
    SELECT internalaccount_create('A', 'INTL', 'CASH', 'Cash','EUR') into inserted_id;
    PERFORM codelink_create('CASH_ACCOUNT_EUR', inserted_id, 'Account for day-to-day deposit/withdrawals');

END
$$ LANGUAGE plpgsql;