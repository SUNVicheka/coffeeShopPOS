-- Migration script to add MANAGER role to users table
-- Run this script if you already have a database with ADMIN and CASHIER roles
-- Execute: mysql -u root -p coffee_shop_db < migrations/add_manager_role.sql

-- Update the role enum to include MANAGER
ALTER TABLE users MODIFY COLUMN role ENUM('ADMIN', 'MANAGER', 'CASHIER') NOT NULL DEFAULT 'CASHIER';

-- Verify the change
DESCRIBE users;

