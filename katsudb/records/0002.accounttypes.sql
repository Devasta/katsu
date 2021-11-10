------------------------------------------------------------------------------------------------------------------------
--Populate Static Values, it is unwise to add more values to these.
--Seriously, don't.
INSERT INTO accounttypes
    (accounttype, description, debitincrease)
VALUES
    ('A', 'Asset', True), --Mostly Loans
    ('L', 'Liability', False), --Mostly Savings Accounts
    ('I', 'Income', False),
    ('E', 'Expense', True),
    ('Q', 'Equity', False);