CREATE TABLE IF NOT EXISTS loanclosecodes(
    closereasonid SERIAL PRIMARY KEY,
    closereason varchar(50) UNIQUE NOT NULL
);
