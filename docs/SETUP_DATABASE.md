# MySQL Database Setup Guide

This guide will help you set up the MySQL database for the Coffee Shop Cashier Management System.

## Prerequisites

- MySQL Server 8.0+ installed and running
- MySQL root access or a database user with CREATE DATABASE privileges

## Step 1: Install MySQL Server (if not installed)

### Windows:
1. Download MySQL Installer from: https://dev.mysql.com/downloads/installer/
2. Run the installer and follow the installation wizard
3. Set root password during installation (remember this password!)

### macOS (Homebrew):
```bash
brew install mysql
brew services start mysql
```

### Linux (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install mysql-server
sudo systemctl start mysql
sudo systemctl enable mysql
```

## Step 2: Create Database

### Option A: Using MySQL Command Line

1. Open MySQL Command Line Client (or terminal)

2. Login as root:
```bash
mysql -u root -p
```
Enter your MySQL root password when prompted.

3. Create the database:
```sql
CREATE DATABASE coffee_shop_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

4. Verify database creation:
```sql
SHOW DATABASES;
```

You should see `coffee_shop_db` in the list.

5. Exit MySQL:
```sql
EXIT;
```

### Option B: Using MySQL Workbench

1. Open MySQL Workbench
2. Connect to your MySQL server (localhost)
3. Click on "Schemas" tab
4. Right-click in the schemas panel → "Create Schema"
5. Schema name: `coffee_shop_db`
6. Collation: `utf8mb4_unicode_ci`
7. Click "Apply"

## Step 3: Create Database User (Optional but Recommended)

For production use, it's better to create a dedicated database user instead of using root:

1. Login to MySQL as root:
```bash
mysql -u root -p
```

2. Create a new user:
```sql
CREATE USER 'coffeeshop_user'@'localhost' IDENTIFIED BY 'your_secure_password';
```

3. Grant privileges:
```sql
GRANT ALL PRIVILEGES ON coffee_shop_db.* TO 'coffeeshop_user'@'localhost';
FLUSH PRIVILEGES;
```

4. Verify user creation:
```sql
    SELECT User, Host FROM mysql.user WHERE User = 'coffeeshop_user';
```

5. Exit MySQL:
```sql
EXIT;
```

**Note:** If you create a new user, update your `.env` file with the new credentials:
```
DB_USER=coffeeshop_user
DB_PASSWORD=your_secure_password
```

## Step 4: Verify MySQL is Running

### Windows:
Check MySQL service in Services app or run:
```bash
sc query MySQL80
```

### macOS/Linux:
```bash
sudo systemctl status mysql
# or
brew services list
```

## Step 5: Test Database Connection

You can test the connection using MySQL command line:

```bash
mysql -u root -p -e "USE coffee_shop_db; SHOW TABLES;"
```

Or if using a dedicated user:
```bash
mysql -u coffeeshop_user -p -e "USE coffee_shop_db; SHOW TABLES;"
```

## Common Issues & Solutions

### Issue 1: "Access denied for user"

**Solution:** 
- Check username and password in `.env` file
- Verify MySQL service is running
- Try resetting MySQL root password

### Issue 2: "Can't connect to MySQL server"

**Solution:**
- Ensure MySQL service is running
- Check if MySQL is running on default port 3306
- Verify firewall settings allow MySQL connections

### Issue 3: "Unknown database 'coffee_shop_db'"

**Solution:**
- Ensure database was created successfully
- Check database name spelling in `.env` file
- Verify you have permissions to access the database

### Issue 4: "Character set issues"

**Solution:**
- Ensure database uses `utf8mb4` character set
- Verify collation is `utf8mb4_unicode_ci`
- Recreate database with correct charset if needed

## Next Steps

After setting up the database:

1. Configure `.env` file in `backend/` directory (see `.env.example`)
2. Install Python dependencies: `pip install -r requirements.txt`
3. Initialize database: `python init_db.py`
4. Start backend server: `python run.py`

## Database Configuration in .env

Update your `backend/.env` file with the following:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_USER=root              # or 'coffeeshop_user' if you created a user
DB_PASSWORD=your_password # Your MySQL root password
DB_NAME=coffee_shop_db
```

## Database Backup (Recommended)

After initialization, create a backup:

```bash
mysqldump -u root -p coffee_shop_db > backup.sql
```

To restore:
```bash
mysql -u root -p coffee_shop_db < backup.sql
```

## Additional Resources

- MySQL Official Documentation: https://dev.mysql.com/doc/
- MySQL Workbench: https://dev.mysql.com/downloads/workbench/
- MySQL Connector for Python: https://dev.mysql.com/doc/connector-python/en/

---

If you encounter any issues, please check the error logs and ensure all prerequisites are met.

