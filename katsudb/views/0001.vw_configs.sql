--These views may seem sort of redundant, but I will probably need to update the DB schema at some stage.
--Best keep structure stuff here where possible.
CREATE OR REPLACE VIEW vw_configs AS
    SELECT
        configname,
        configvalue,
        description
    FROM configvalues;
