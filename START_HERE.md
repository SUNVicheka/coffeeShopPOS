# 🎉 Welcome to Coffee Shop POS!

**Your complete Cashier Management System is ready!**

---

## 📍 Where to Start

### New to the Project?
👉 Read: **[FIRST_TIME_SETUP.txt](FIRST_TIME_SETUP.txt)** - Step-by-step instructions

### Want Quick Setup?
👉 Read: **[QUICK_START.md](QUICK_START.md)** - Get running in 10 minutes

### Need Detailed Guide?
👉 Read: **[docs/MANUAL_SETUP.md](docs/MANUAL_SETUP.md)** - Complete manual setup

### Having Issues?
👉 Check: **[SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)** - Troubleshooting checklist

---

## 🚀 Fastest Way to Get Started

### 1️⃣ Create MySQL Database (2 minutes)
```sql
CREATE DATABASE coffee_shop_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2️⃣ Configure Backend (3 minutes)
```bash
cd backend
python -m venv venv
venv\Scripts\activate    # Windows
pip install -r requirements.txt

# Create .env file (copy env_template.txt to .env)
# Edit .env with your MySQL password

python init_db.py
```

### 3️⃣ Start Servers (2 minutes)

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate
python run.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm start
```

### 4️⃣ Login
- Open: http://localhost:3000
- Admin: `admin` / `admin123`
- Cashier: `cashier` / `cashier123`

**That's it!** 🎊

---

## ⚡ Even Faster: Use Startup Scripts

After initial setup (Steps 1-2 above):

**Windows:**
- Double-click `start_backend.bat`
- Double-click `start_frontend.bat` (new window)

**macOS/Linux:**
```bash
chmod +x start_backend.sh start_frontend.sh
./start_backend.sh      # Terminal 1
./start_frontend.sh     # Terminal 2
```

---

## 📚 Complete Documentation

| File | Purpose |
|------|---------|
| **[FIRST_TIME_SETUP.txt](FIRST_TIME_SETUP.txt)** | Complete setup instructions |
| **[QUICK_START.md](QUICK_START.md)** | 10-minute quick setup |
| **[SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)** | Verification checklist |
| **[docs/MANUAL_SETUP.md](docs/MANUAL_SETUP.md)** | Detailed manual setup |
| **[docs/SETUP_DATABASE.md](docs/SETUP_DATABASE.md)** | MySQL database setup |
| **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** | Project overview |
| **[README.md](README.md)** | Main project documentation |

---

## ✅ What's Included

### Features
- ✅ User Authentication (Admin/Cashier roles)
- ✅ Product Management
- ✅ Order Processing (POS)
- ✅ Receipt Generation (On-screen)
- ✅ Sales Reports
- ✅ User Management
- ✅ Inventory Tracking

### Technology
- ✅ **Backend:** Python Flask + MySQL
- ✅ **Frontend:** React + Bootstrap 5
- ✅ **Database:** MySQL 8.0+

---

## 🔑 Default Login Credentials

**After database initialization:**

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |
| Cashier | `cashier` | `cashier123` |

⚠️ **IMPORTANT:** Change these passwords after first login!

---

## 🆘 Need Help?

### Common Issues

**Can't connect to MySQL?**
- See: `docs/SETUP_DATABASE.md`

**Backend won't start?**
- Check `.env` file exists and has correct MySQL password
- Verify MySQL service is running

**Frontend won't start?**
- Run: `npm install`
- Check Node.js is installed

**Can't login?**
- Make sure database was initialized: `python init_db.py`
- Check backend is running on port 5000

### More Help
- Check: `SETUP_CHECKLIST.md` for troubleshooting
- Review: `docs/MANUAL_SETUP.md` for detailed steps

---

## 📝 Next Steps After Setup

1. **Change Default Passwords** (Security priority)
   - Go to Users page → Edit users → Change passwords

2. **Add Your Products**
   - Go to Products page → Add Product
   - Fill in product details

3. **Configure Categories**
   - Products page → Manage categories

4. **Test POS System**
   - Go to POS page
   - Create a test order

5. **Generate Reports**
   - Go to Reports page
   - View sales analytics

---

## 🎯 Quick Commands Reference

### Backend
```bash
cd backend
venv\Scripts\activate      # Activate venv (Windows)
python init_db.py          # Initialize database
python run.py              # Start server
```

### Frontend
```bash
cd frontend
npm install                # Install dependencies
npm start                  # Start server
```

### Database
```bash
mysql -u root -p           # Login to MySQL
```

---

## 📞 Support

If you encounter issues:
1. Check the troubleshooting sections in documentation
2. Review error messages in terminal windows
3. Verify all prerequisites are installed
4. Check MySQL service is running
5. Ensure `.env` file is configured correctly

---

**Ready to start? Begin with [FIRST_TIME_SETUP.txt](FIRST_TIME_SETUP.txt)!** 🚀

---

*Project Version: 1.0.0*  
*Last Updated: December 2024*

