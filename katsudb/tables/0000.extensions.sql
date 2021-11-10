--For any files we generate that are not just straight SQL, we will generate as
--an XML query which we will transform. Example: SEPA ISO 10022
CREATE EXTENSION IF NOT EXISTS xml2;

