CREATE TABLE BEER(
   beer_id SERIAL PRIMARY KEY,
   name TEXT NOT NULL,
   BREWERY_ID        CHAR(50) NOT NULL,
   ALCOHOL
   IBU        CHAR(50),
   SALARY         REAL
);

CREATE TABLE [IF NOT EXISTS] table_name (
   column1 datatype(length) column_contraint,
   column2 datatype(length) column_contraint,
   column3 datatype(length) column_contraint,
   table_constraints
);

CREATE TABLE BREWERY(
   id INT PRIMARY KEY      NOT NULL,
   name           CHAR(50) NOT NULL,
   location        INT      NOT NULL
);