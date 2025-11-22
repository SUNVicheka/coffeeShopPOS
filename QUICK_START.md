# Quick Start Guide

Get your Coffee Shop POS system running in 10 minutes!

## 🎯 Prerequisites Check

First, verify you have everything installed:

```bash
python --version    # Should show 3.8 or higher
node --version      # Should show 16 or higher
npm --version       # Should show 8 or higher
mysql --version     # Should show 8.0 or higher
```

---

## ⚡ Fast Setup (3 Steps)

### Step 1: Create MySQL Database (2 minutes)

Open MySQL Command Line or MySQL Workbench:

```sql
CREATE DATABASE coffee_shop_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

**That's it!** The database is ready.

---

### Step 2: Configure Backend (3 minutes)

1. **Navigate to backend folder:**
   ```bash
   cd coffeeShopPOS/backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   
   # Activate it:
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file:**
   - Copy `env_template.txt` and rename to `.env`
   - Open `.env` in a text editor
   - Change `DB_PASSWORD=your_mysql_password` to your actual MySQL password
   - Save the file

5. **Initialize database:**
   ```bash
   python init_db.py
   ```

   You should see:
   ```
   ✓ Database tables created
   ✓ Created categories...
   ✓ Created users...
   ✓ Created products...
   ✓ Database initialized successfully!
   ```

---

### Step 3: Start Both Servers (2 minutes)

**Open TWO terminal windows:**

#### Terminal 1 - Backend:
```bash
cd coffeeShopPOS/backend
venv\Scripts\activate      # Windows
# source venv/bin/activate  # macOS/Linux
python run.py
```

You should see: `* Running on http://0.0.0.0:5000`

#### Terminal 2 - Frontend:
```bash
cd coffeeShopPOS/frontend
npm install
npm start
```

You should see: `Local: http://localhost:3000/`

---

## 🎉 You're Done!

1. Open browser: **http://localhost:3000**
2. Login with:
   - **Admin:** `admin` / `admin123`
   - **Cashier:** `cashier` / `cashier123`

---

## 🚀 Using Startup Scripts (Even Faster!)

### Windows:

1. Create `.env` file in `backend/` (see Step 2 above)
2. Double-click: `start_backend.bat`
3. Double-click: `start_frontend.bat` (new window)

### macOS/Linux:

1. Create `.env` file in `backend/` (see Step 2 above)
2. Make scripts executable:
   ```bash
   chmod +x start_backend.sh start_frontend.sh
   ```
3. Run:
   ```bash
   ./start_backend.sh    # Terminal 1
   ./start_frontend.sh   # Terminal 2
   ```

---

## ✅ Verify Installation

- [ ] Backend running: http://localhost:5000
- [ ] Frontend running: http://localhost:3000
- [ ] Login page appears
- [ ] Can login with admin/cashier
- [ ] POS page shows products
- [ ] Can add items to cart
- [ ] Can checkout successfully

---

## 🐛 Troubleshooting

### Backend won't start?
- Check MySQL is running
- Verify `.env` file exists and has correct password
- Make sure virtual environment is activated
- Check port 5000 is not in use

### Frontend won't start?
- Make sure Node.js is installed
- Delete `node_modules` and run `npm install` again
- Check port 3000 is not in use

### Can't login?
- Make sure database was initialized (`python init_db.py`)
- Check backend is running on port 5000
- Verify credentials: `admin`/`admin123`

---

## 📚 Need More Help?

- **Detailed Setup:** See `docs/MANUAL_SETUP.md`
- **Database Issues:** See `docs/SETUP_DATABASE.md`
- **Checklist:** See `SETUP_CHECKLIST.md`
- **Project Summary:** See `PROJECT_SUMMARY.md`

---

## 🎯 Next Steps After Setup

1. **Change passwords** (Go to Users page → Edit)
2. **Add your products** (Go to Products page → Add Product)
3. **Test POS** (Go to POS page → Create an order)
4. **Generate reports** (Go to Reports page)

---

**That's it!** Your Coffee Shop POS is ready to use! 🎉

