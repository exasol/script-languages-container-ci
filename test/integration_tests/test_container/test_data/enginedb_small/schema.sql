CREATE SCHEMA TEST;

CREATE TABLE ENGINETABLE (
    INT_INDEX   DECIMAL(18,0),
    DECIMAL1    DECIMAL(8,3),
    DECIMAL2    DECIMAL(8,3),
    SMALLINT1   DECIMAL(9,0),
    SMALLINT2   DECIMAL(9,0),
    INT1        DECIMAL(18,0),
    INT2        DECIMAL(18,0),
    FLOAT1      DOUBLE PRECISION,
    FLOAT2      DOUBLE PRECISION,
    SINGLE_CHAR CHAR(1) UTF8,
    CHAR1       CHAR(30) UTF8,
    CHAR2       CHAR(30) UTF8,
    VARCHAR01   VARCHAR(30) UTF8,
    VARCHAR02   VARCHAR(30) UTF8,
    DATE1       DATE,
    DATE2       DATE
);

CREATE TABLE COMP1 (
    IDX         DECIMAL(18,0),
    CHAR1_1     CHAR(1) UTF8,
    CHAR1_2     CHAR(1) UTF8,
    VARCHAR1_1  VARCHAR(1) UTF8,
    VARCHAR1_2  VARCHAR(1) UTF8,
    CHAR4_1     CHAR(4) UTF8,
    CHAR4_2     CHAR(4) UTF8,
    VARCHAR4_1  VARCHAR(4) UTF8,
    VARCHAR4_2  VARCHAR(4) UTF8,
    CHAR10_1    CHAR(10) UTF8,
    CHAR10_2    CHAR(10) UTF8,
    VARCHAR10_1 VARCHAR(10) UTF8,
    VARCHAR10_2 VARCHAR(10) UTF8
);