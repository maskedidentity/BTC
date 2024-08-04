-> made this challenge for mimicking http parameter pollution vulnerability on tier 


-> used HTML, CSS,Flask, MySQL

-> description of the DB and tables used

-> to set up DB

-> systemctl start mysql


-> mysql -u root -h localhost -p 


-> DB name: BTC


-> SQL table name: user2024

CREATE TABLE user2024 (
    name VARCHAR(20) NOT NULL PRIMARY KEY,
    password VARCHAR(255) NOT NULL,
    tier VARCHAR(10) NOT NULL
);
