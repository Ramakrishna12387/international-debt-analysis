CREATE DATABASE IF NOT EXISTS international_debt_db;

USE international_debt_db;

CREATE TABLE countries (
    country_code VARCHAR(10) PRIMARY KEY,
    country_name VARCHAR(150) NOT NULL
);

CREATE TABLE indicators (
    indicator_code VARCHAR(50) PRIMARY KEY,
    indicator_name VARCHAR(255) NOT NULL
);

CREATE TABLE debt_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    country_code VARCHAR(10) NOT NULL,
    indicator_code VARCHAR(50) NOT NULL,
    year SMALLINT NOT NULL,
    debt DECIMAL(20, 6),
    FOREIGN KEY (country_code)
        REFERENCES countries(country_code),
    FOREIGN KEY (indicator_code)
        REFERENCES indicators(indicator_code),
    UNIQUE KEY unique_debt_record
        (country_code, indicator_code, year)
);