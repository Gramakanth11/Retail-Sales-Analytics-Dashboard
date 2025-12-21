-- Create database
CREATE DATABASE IF NOT EXISTS retail_sales;
USE retail_sales;

-- Drop table if already exists
DROP TABLE IF EXISTS sales_cleaned;

-- Create table
CREATE TABLE sales_cleaned (
    `Order ID`        VARCHAR(50),
    `Order Date`      DATE,
    `Customer ID`     VARCHAR(50),
    `Customer Name`   VARCHAR(255),
    `Segment`         VARCHAR(100),
    `Region`          VARCHAR(100),
    `Product ID`      VARCHAR(50),
    `Product Name`    VARCHAR(255),
    `Category`        VARCHAR(100),
    `Sub-Category`    VARCHAR(100),
    `Quantity`        INT,
    `Unit Price`      DECIMAL(10, 2),
    `Discount`        DECIMAL(5, 2),
    `Total Sales`     DECIMAL(12, 2),
    `Profit`          DECIMAL(12, 2),
    `Profit Margin`   DECIMAL(7, 4)
);

SHOW DATABASES;

USE retail_sales;
SHOW TABLES;

SELECT COUNT(*) FROM retail_sales.sales_cleaned;
