# Manual Setup Instructions

Complete step-by-step manual setup guide for the Coffee Shop Cashier Management System.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Backend Setup](#backend-setup)
3. [Frontend Setup](#frontend-setup)
4. [Database Setup](#database-setup)
5. [Running the Application](#running-the-application)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

1. **Python 3.8+**
   - Download from: https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"
   - Verify: `python --version`

2. **Node.js 16+**
   - Download from: https://nodejs.org/
   - Verify: `node --version` and `npm --version`

3. **MySQL Server 8.0+**
   - See [SETUP_DATABASE.md](SETUP_DATABASE.md) for MySQL installation
   - Verify: MySQL service is running

4. **Git** (optional)
   - Download from: https://git-scm.com/downloads

---

## Backend Setup

### Step 1: Navigate to Backend Directory

```bash
cd coffeeShopPOS/backend
```

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Verify installation:
```bash
pip list
```

You should see Flask, SQLAlchemy, PyMySQL, etc.

### Step 4: Configure Environment Variables

1. Copy the example environment file:
   ```bash
   # Create .env file manually or copy from example
   ```

2. Create `backend/.env` file with the following content:
   ```env
   # Flask Configuration
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=your-secret-key-change-in-production

   # Database Configuration
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD=your_mysql_password
   DB_NAME=coffee_shop_db

   # JWT Configuration
   JWT_SECRET_KEY=jwt-secret-key-change-in-production

   # CORS Configuration
   CORS_ORIGINS=http://localhost:3000,http://localhost:5173

   # Application Settings
   TAX_RATE=0.05
   ```

3. **IMPORTANT:** Replace `your_mysql_password` with your actual MySQL root password!

### Step 5: Set Up MySQL Database

**Before proceeding, ensure MySQL is set up (see SETUP_DATABASE.md):**

1. Create the database:
   ```sql
   CREATE DATABASE coffee_shop_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

2. Verify database exists:
   ```sql
   SHOW DATABASES;
   ```

### Step 6: Initialize Database

```bash
python init_db.py
```

This will:
- Create all database tables
- Insert default categories
- Create default users (admin/cashier)
- Insert sample products

**Expected output:**
```
Creating database tables...
✓ Database tables created

Creating categories...
  ✓ Created category: Hot Coffee
  ✓ Created category: Cold Coffee
  ...

Creating users...
  ✓ Created user: admin (ADMIN)
  ✓ Created user: cashier (CASHIER)

Creating products...
  ✓ Created product: Espresso
  ...

✓ Database initialized successfully!

Default login credentials:
  Admin:   username=admin, password=admin123
  Cashier: username=cashier, password=cashier123
```

### Step 7: Test Backend Server

```bash
python run.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

Open browser: http://localhost:5000

You should see a Flask welcome page or API response.

**Keep this terminal open!**

---

## Frontend Setup

### Step 1: Open New Terminal

Open a **new terminal window** (keep backend running in the first terminal).

### Step 2: Navigate to Frontend Directory

```bash
cd coffeeShopPOS/frontend
```

### Step 3: Install Node Dependencies

```bash
npm install
```

This may take a few minutes. You should see:
```
added XXX packages
```

### Step 4: Verify Installation

Check if all dependencies are installed:
```bash
npm list --depth=0
```

### Step 5: Start Frontend Development Server

```bash
npm start
# or
npm run dev
```

You should see:
```
VITE vX.X.X ready in XXX ms

➜  Local:   http://localhost:3000/
➜  Network: use --host to expose
```

**Keep this terminal open!**

---

## Running the Application

### Starting Both Servers

1. **Terminal 1 - Backend:**
   ```bash
   cd coffeeShopPOS/backend
   venv\Scripts\activate    # Windows
   # source venv/bin/activate  # macOS/Linux
   python run.py
   ```
   Server runs on: http://localhost:5000

2. **Terminal 2 - Frontend:**
   ```bash
   cd coffeeShopPOS/frontend
   npm start
   ```
   Server runs on: http://localhost:3000

### Accessing the Application

1. Open browser: http://localhost:3000
2. Login page should appear
3. Use default credentials:
   - **Admin:** username: `admin`, password: `admin123`
   - **Cashier:** username: `cashier`, password: `cashier123`

### Default Features Available

- **POS Interface** - Create orders, process payments
- **Products** - Manage products (Admin only)
- **Orders** - View order history
- **Reports** - View sales reports
- **Users** - Manage users (Admin only)

---

## First Login Setup

### Change Default Passwords

After first login:

1. Go to **Users** page (Admin only)
2. Edit the admin user
3. Change password to something secure
4. Repeat for cashier user

### Add Your Products

1. Go to **Products** page
2. Click **Add Product**
3. Fill in product details:
   - Name, SKU, Category
   - Price, Cost Price
   - Stock Quantity
4. Click **Create**

---

## Troubleshooting

### Backend Issues

#### "Module not found"
```bash
# Ensure virtual environment is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Reinstall dependencies
pip install -r requirements.txt
```

#### "Can't connect to MySQL"
- Check MySQL service is running
- Verify `.env` file has correct credentials
- Test MySQL connection: `mysql -u root -p`

#### "Database doesn't exist"
```sql
CREATE DATABASE coffee_shop_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### "Port 5000 already in use"
- Change port in `run.py`: `app.run(port=5001)`
- Update frontend API URL accordingly

### Frontend Issues

#### "Module not found"
```bash
# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### "Port 3000 already in use"
- Change port in `vite.config.js`
- Or stop the process using port 3000

#### "Cannot connect to backend"
- Ensure backend is running on http://localhost:5000
- Check CORS settings in backend `.env`
- Verify API URL in `frontend/src/services/api.js`

### Database Issues

#### "Access denied"
- Check MySQL credentials in `.env`
- Verify user has permissions on database

#### "Table doesn't exist"
- Run database initialization: `python init_db.py`

---

## Verification Checklist

- [ ] Python 3.8+ installed and in PATH
- [ ] Node.js 16+ installed
- [ ] MySQL Server installed and running
- [ ] Virtual environment created and activated
- [ ] Python dependencies installed
- [ ] Node dependencies installed
- [ ] Database created in MySQL
- [ ] `.env` file configured with correct credentials
- [ ] Database initialized with `python init_db.py`
- [ ] Backend server running on port 5000
- [ ] Frontend server running on port 3000
- [ ] Can access http://localhost:3000
- [ ] Can login with default credentials

---

## Next Steps

After successful setup:

1. **Change default passwords** (Security)
2. **Add your products** (Products page)
3. **Configure categories** (Products page)
4. **Create additional users** (Users page - Admin only)
5. **Test POS functionality** (POS page)
6. **Generate reports** (Reports page)

---

## Quick Reference Commands

### Backend
```bash
cd backend
venv\Scripts\activate          # Activate venv (Windows)
source venv/bin/activate        # Activate venv (macOS/Linux)
python run.py                   # Start server
python init_db.py               # Initialize database
```

### Frontend
```bash
cd frontend
npm install                     # Install dependencies
npm start                       # Start dev server
npm run build                   # Build for production
```

### Database
```bash
mysql -u root -p                # Login to MySQL
mysql -u root -p coffee_shop_db # Connect to database
mysqldump -u root -p coffee_shop_db > backup.sql  # Backup
```

---

For database-specific setup, see [SETUP_DATABASE.md](SETUP_DATABASE.md)

For API documentation, see [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

