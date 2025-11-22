# Setup Checklist

Follow this checklist to ensure everything is set up correctly.

## Prerequisites

- [ ] Python 3.8+ installed
  - Verify: `python --version`
- [ ] Node.js 16+ installed
  - Verify: `node --version`
  - Verify: `npm --version`
- [ ] MySQL Server 8.0+ installed and running
  - Verify: MySQL service is running
  - Verify: `mysql --version`

## Step 1: MySQL Database Setup

- [ ] MySQL Server is running
- [ ] Created database: `coffee_shop_db`
  ```sql
  CREATE DATABASE coffee_shop_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
  ```
- [ ] Verified database exists:
  ```sql
  SHOW DATABASES;
  ```
- [ ] Know your MySQL root password

## Step 2: Backend Setup

- [ ] Navigate to `backend/` directory
- [ ] Created virtual environment:
  ```bash
  python -m venv venv
  ```
- [ ] Activated virtual environment:
  - Windows: `venv\Scripts\activate`
  - macOS/Linux: `source venv/bin/activate`
- [ ] Installed Python dependencies:
  ```bash
  pip install -r requirements.txt
  ```
- [ ] Created `.env` file in `backend/` directory
- [ ] Configured `.env` with MySQL credentials:
  - `DB_HOST=localhost`
  - `DB_PORT=3306`
  - `DB_USER=root` (or your MySQL user)
  - `DB_PASSWORD=your_mysql_password` ⚠️ **IMPORTANT: Replace with your actual password**
  - `DB_NAME=coffee_shop_db`
- [ ] Initialized database:
  ```bash
  python init_db.py
  ```
- [ ] Database initialized successfully (saw success messages)
- [ ] Tested backend server starts:
  ```bash
  python run.py
  ```
- [ ] Backend running on http://localhost:5000

## Step 3: Frontend Setup

- [ ] Open a NEW terminal window (keep backend running)
- [ ] Navigate to `frontend/` directory
- [ ] Installed Node dependencies:
  ```bash
  npm install
  ```
- [ ] Verified dependencies installed (no errors)
- [ ] Started frontend server:
  ```bash
  npm start
  ```
- [ ] Frontend running on http://localhost:3000

## Step 4: Application Testing

- [ ] Opened browser to http://localhost:3000
- [ ] Login page appears
- [ ] Can login with admin credentials:
  - Username: `admin`
  - Password: `admin123`
- [ ] Dashboard/POS page loads after login
- [ ] Navigation menu visible
- [ ] Can see products in POS page
- [ ] Can add products to cart
- [ ] Can checkout and create order
- [ ] Receipt displays after order

## Step 5: Post-Installation Security

- [ ] Changed admin password
  - Go to Users page (Admin only)
  - Edit admin user
  - Change password to something secure
- [ ] Changed cashier password
  - Edit cashier user
  - Change password to something secure
- [ ] Reviewed .env file security
  - Secret keys changed from defaults
  - MySQL password is secure

## Step 6: Data Setup (Optional)

- [ ] Added your products
  - Go to Products page
  - Click "Add Product"
  - Fill in product details
- [ ] Organized products into categories
  - Created categories if needed
  - Assigned products to categories
- [ ] Set stock quantities for products
- [ ] Verified products appear in POS

## Troubleshooting

### If backend won't start:
- [ ] MySQL service is running
- [ ] `.env` file exists and is configured correctly
- [ ] Virtual environment is activated
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Database exists and is accessible
- [ ] Port 5000 is not in use

### If frontend won't start:
- [ ] Node.js is installed correctly
- [ ] Dependencies installed (`npm install`)
- [ ] Port 3000 is not in use
- [ ] Backend is running on port 5000

### If can't login:
- [ ] Database was initialized (`python init_db.py`)
- [ ] Default users were created
- [ ] Using correct credentials:
  - Admin: `admin` / `admin123`
  - Cashier: `cashier` / `cashier123`
- [ ] Backend server is running

### If products don't load:
- [ ] Database was initialized with sample products
- [ ] Backend API is accessible
- [ ] Check browser console for errors
- [ ] Verify API URL in `frontend/src/services/api.js`

---

## Quick Verification Commands

### Test MySQL Connection
```bash
mysql -u root -p -e "USE coffee_shop_db; SHOW TABLES;"
```

### Test Backend API
```bash
curl http://localhost:5000/api/auth/check
```

### Test Frontend
Open browser: http://localhost:3000

---

## Success Indicators

✅ Both terminals running without errors  
✅ Backend accessible at http://localhost:5000  
✅ Frontend accessible at http://localhost:3000  
✅ Can login successfully  
✅ POS page displays products  
✅ Can create and view orders  
✅ Reports generate correctly  

---

## Next Steps After Setup

1. **Change default passwords** (Security priority)
2. **Add your actual products** (Replace sample data)
3. **Configure your categories** (Customize for your shop)
4. **Train users** (Show them how to use the system)
5. **Set up backups** (Regular database backups)
6. **Monitor performance** (Check logs if issues arise)

---

## Need Help?

- Check `docs/MANUAL_SETUP.md` for detailed instructions
- Check `docs/SETUP_DATABASE.md` for MySQL issues
- Review error messages in terminal windows
- Check browser console (F12) for frontend errors

---

**Status:** ☐ Setup Complete

