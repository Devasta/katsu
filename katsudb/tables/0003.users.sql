--At some point in future, I would like to have an external portal for members to visit.
--I don't think we need seperate staff and users table, just make it all the one.
--The awaitingverification flag will be used for verifying emails.
--Password resets can just be done by clearing the password field.
--TokenID  is used for session tokens by flask_login, when we reset someones password we should also update that.

CREATE TABLE IF NOT EXISTS users (
    userID   SERIAL PRIMARY KEY,
    email    VARCHAR(100) NOT NULL UNIQUE,
    roleID   INTEGER NOT NULL REFERENCES roles (roleID),
    forename VARCHAR(35) NOT NULL,
    surname  VARCHAR(35) NOT NULL,
    password CHAR(60), --Always Bcrypting!!!
    tokenID  INTEGER UNIQUE NOT NULL,
    memberID INTEGER UNIQUE,
    awaitingverification BOOLEAN DEFAULT TRUE
);
CREATE SEQUENCE IF NOT EXISTS user_tokenid_seq START 1;
ALTER TABLE users ALTER COLUMN tokenID SET DEFAULT nextval('user_tokenid_seq');
