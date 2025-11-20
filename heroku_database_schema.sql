-- Rwanda Trade Dashboard Database Schema for Heroku
-- Run this on your ClearDB database

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create datasetx table (if not exists)
CREATE TABLE IF NOT EXISTS datasetx (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item VARCHAR(255) NOT NULL,
    time INT NOT NULL,
    amount DECIMAL(15,2) NOT NULL
);

-- Create export_commodities table (if not exists)
CREATE TABLE IF NOT EXISTS export_commodities (
    period VARCHAR(255) PRIMARY KEY,
    `2020Q1` DECIMAL(15,2),
    `2020Q2` DECIMAL(15,2),
    `2020Q3` DECIMAL(15,2),
    `2020Q4` DECIMAL(15,2),
    `2021Q1` DECIMAL(15,2),
    `2021Q2` DECIMAL(15,2),
    `2021Q3` DECIMAL(15,2),
    `2021Q4` DECIMAL(15,2),
    `2022Q1` DECIMAL(15,2),
    `2022Q2` DECIMAL(15,2),
    `2022Q3` DECIMAL(15,2),
    `2022Q4` DECIMAL(15,2),
    `2023Q1` DECIMAL(15,2),
    `2023Q2` DECIMAL(15,2),
    `2023Q3` DECIMAL(15,2),
    `2023Q4` DECIMAL(15,2),
    `2024Q1` DECIMAL(15,2),
    `2024Q2` DECIMAL(15,2),
    `2025Q1` DECIMAL(15,2),
    `2025Q2` DECIMAL(15,2)
);

-- Create imports_commodities table (if not exists)
CREATE TABLE IF NOT EXISTS imports_commodities (
    period VARCHAR(255) PRIMARY KEY,
    `2020Q1` DECIMAL(15,2),
    `2020Q2` DECIMAL(15,2),
    `2020Q3` DECIMAL(15,2),
    `2020Q4` DECIMAL(15,2),
    `2021Q1` DECIMAL(15,2),
    `2021Q2` DECIMAL(15,2),
    `2021Q3` DECIMAL(15,2),
    `2021Q4` DECIMAL(15,2),
    `2022Q1` DECIMAL(15,2),
    `2022Q2` DECIMAL(15,2),
    `2022Q3` DECIMAL(15,2),
    `2022Q4` DECIMAL(15,2),
    `2023Q1` DECIMAL(15,2),
    `2023Q2` DECIMAL(15,2),
    `2023Q3` DECIMAL(15,2),
    `2023Q4` DECIMAL(15,2),
    `2024Q1` DECIMAL(15,2),
    `2024Q2` DECIMAL(15,2),
    `2025Q1` DECIMAL(15,2),
    `2025Q2` DECIMAL(15,2)
);

-- Create other required tables
CREATE TABLE IF NOT EXISTS exportss (
    period VARCHAR(255) PRIMARY KEY,
    exports DECIMAL(15,2),
    imports DECIMAL(15,2),
    `re-imports` DECIMAL(15,2)
);

CREATE TABLE IF NOT EXISTS exports_share (
    country VARCHAR(255) PRIMARY KEY,
    share DECIMAL(5,2),
    value DECIMAL(15,2),
    change1 DECIMAL(5,2),
    change2 DECIMAL(5,2)
);

CREATE TABLE IF NOT EXISTS imports_share (
    country VARCHAR(255) PRIMARY KEY,
    share DECIMAL(5,2),
    value DECIMAL(15,2),
    change1 DECIMAL(5,2),
    change2 DECIMAL(5,2)
);

-- Insert sample data (you'll need to export your current data)
-- Use: mysqldump -u root -p bigdatahackaton > database_backup.sql
-- Then modify and run on ClearDB