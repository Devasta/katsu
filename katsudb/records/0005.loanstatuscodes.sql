--The process for loans goes:
-- P --> D --> A --> C
-- Only "A" status loans will have interest payments applied.
-- Only "P" status loans can have certain loan details amended.
-- "C" loans get locked for editing.
INSERT INTO loanstatuscodes
    (loanstatusid, description)
VALUES
    ('P', 'Pending Approval'),
    ('D', 'Approved - Pending Drawdown'),
    ('A', 'Active'),
    ('C', 'Closed');