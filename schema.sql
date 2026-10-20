CREATE DATABASE IF NOT EXISTS international_debt_db;
USE international_debt_db;

-- 1. Countries Dimension Table
DROP TABLE IF EXISTS debt_data;
DROP TABLE IF EXISTS indicators;
DROP TABLE IF EXISTS countries;

CREATE TABLE countries (
    country_code VARCHAR(10) PRIMARY KEY,
    country_name VARCHAR(150) NOT NULL
);

-- 2. Indicators Dimension Table
CREATE TABLE indicators (
    indicator_code VARCHAR(50) PRIMARY KEY,
    indicator_name VARCHAR(255) NOT NULL
);

-- 3. Debt Facts Table
CREATE TABLE debt_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    country_code VARCHAR(10) NOT NULL,
    indicator_code VARCHAR(50) NOT NULL,
    debt DECIMAL(20, 2) NOT NULL,
    FOREIGN KEY (country_code) REFERENCES countries(country_code) ON DELETE CASCADE,
    FOREIGN KEY (indicator_code) REFERENCES indicators(indicator_code) ON DELETE CASCADE
);