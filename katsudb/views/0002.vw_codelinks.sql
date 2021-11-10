CREATE OR REPLACE VIEW vw_codelinks AS
    SELECT
        codelinkname,
        accountid,
        description
    FROM codelinks;