# Coffee Shop POS - Manager Role Documentation

## 🎯 Project Overview

This is a complete **Coffee Shop Cashier Management System** built with:
- **Backend:** Python Flask + MySQL (SQLAlchemy ORM)
- **Frontend:** React 18.3 + Bootstrap 5
- **Database:** MySQL 8.0+

The system includes **three user roles**: **ADMIN**, **MANAGER**, and **CASHIER**

---

## 📊 System Architecture

### Tech Stack Summary

| Component | Technology | Version |
|-----------|-----------|---------|
| Backend | Flask | 3.0 |
| Frontend | React | 18.3 |
| Database | MySQL | 8.0+ |
| ORM | SQLAlchemy | 2.0 |
| UI Framework | Bootstrap | 5.3 |
| State Management | React Context | - |
| HTTP Client | Axios | - |
| HTTP Runner | Vite | - |

### Project Directory Structure

```
coffeeShopPOS/
├── backend/                    # Flask Backend (Python)
│   ├── app/
│   │   ├── models/            # Database models
│   │   │   ├── user.py        # User model with RoleEnum (ADMIN, MANAGER, CASHIER)
│   │   │   ├── product.py     # Product model
│   │   │   ├── category.py    # Category model
│   │   │   ├── order.py       # Order & OrderItem models
│   │   │   └── stock_log.py   # Stock audit trail
│   │   ├── routes/            # API endpoints
│   │   │   ├── auth.py        # Authentication & role-based decorators
│   │   │   ├── products.py    # Product CRUD (Manager/Admin required)
│   │   │   ├── categories.py  # Category management
│   │   │   ├── orders.py      # Order processing
│   │   │   ├── users.py       # User management (Admin only)
│   │   │   └── reports.py     # Sales reports (Cashier, Manager/Admin)
│   │   └── __init__.py        # App factory
│   ├── config.py              # Configuration & environment
│   ├── run.py                 # Entry point (http://localhost:5000)
│   ├── init_db.py             # Database initialization script
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # Environment variables (create this)
│
├── frontend/                   # React Frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   │   └── Layout.jsx     # Main layout with navigation
│   │   ├── pages/             # Page components
│   │   │   ├── Login.jsx      # Login page
│   │   │   ├── POS.jsx        # POS interface (Cashiers)
│   │   │   ├── Products.jsx   # Product management (Manager/Admin)
│   │   │   ├── Orders.jsx     # Order history (All roles)
│   │   │   ├── Reports.jsx    # Sales reports (All roles, Cashier report=Manager/Admin)
│   │   │   └── Users.jsx      # User management (Admin only)
│   │   ├── contexts/          # React contexts
│   │   │   └── AuthContext.jsx # Authentication context with role helpers
│   │   ├── services/          # API services
│   │   │   └── api.js         # Axios instance & API calls
│   │   ├── App.jsx            # Main app component
│   │   └── main.jsx           # Entry point
│   ├── package.json           # Node.js dependencies
│   └── vite.config.js         # Vite configuration
│
├── docs/                       # Documentation
│   ├── SETUP_DATABASE.md      # MySQL setup guide
│   └── MANUAL_SETUP.md        # Complete setup guide
│
├── migrations/                 # Database migrations
│   ├── add_manager_role.py    # Python migration script
│   └── add_manager_role.sql   # SQL migration script
│
├── README.md                   # Main project documentation
├── QUICK_START.md             # Quick setup guide
├── PROJECT_SUMMARY.md         # Project summary
└── START_HERE.md              # Getting started guide
```

---

## 🔐 MANAGER ROLE - Complete Details

### 1. Backend Implementation

#### A. Database Model (`backend/app/models/user.py`)

```python
class RoleEnum(PyEnum):
    ADMIN = 'ADMIN'
    MANAGER = 'MANAGER'
    CASHIER = 'CASHIER'

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=True)
    role = db.Column(db.Enum(RoleEnum), nullable=False, default=RoleEnum.CASHIER)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
```

**Default Manager Credentials (from init_db.py):**
- Username: `manager`
- Password: `manager123`
- Full Name: `Manager User`
- Email: `manager@coffeeshop.com`
- Role: `MANAGER`

#### B. Authentication Decorators (`backend/app/routes/auth.py`)

The system includes three role-based decorators:

```python
@login_required                    # Requires any logged-in user
@admin_required                    # Requires ADMIN role
@manager_or_admin_required        # Requires MANAGER or ADMIN role
```

#### C. API Endpoints by Permission

**📍 MANAGER PERMISSIONS:**

| Endpoint | Method | Description | Permission |
|----------|--------|-------------|-----------|
| `/api/products` | GET | View all products | `login_required` |
| `/api/products` | POST | Create product | `manager_or_admin_required` |
| `/api/products/<id>` | PUT | Update product | `manager_or_admin_required` |
| `/api/products/<id>` | DELETE | Delete product | `manager_or_admin_required` |
| `/api/products/<id>/stock` | POST | Adjust stock | `manager_or_admin_required` |
| `/api/categories` | GET | View categories | `login_required` |
| `/api/categories` | POST | Create category | `manager_or_admin_required` |
| `/api/categories/<id>` | PUT | Update category | `manager_or_admin_required` |
| `/api/categories/<id>` | DELETE | Delete category | `manager_or_admin_required` |
| `/api/orders` | GET | View all orders | `login_required` |
| `/api/orders/<id>` | GET | View order details | `login_required` |
| `/api/orders` | POST | Create order | `login_required` |
| `/api/orders/<id>` | DELETE | Cancel order | `admin_required` |
| `/api/reports/sales` | GET | Sales report | `login_required` |
| `/api/reports/item-sales` | GET | Item-wise report | `login_required` |
| `/api/reports/cashier` | GET | Cashier performance | `manager_or_admin_required` ✓ |
| `/api/users` | GET | List users | `admin_required` |
| `/api/users` | POST | Create user | `admin_required` |
| `/api/users/<id>` | PUT | Update user | `admin_required` |
| `/api/users/<id>` | DELETE | Delete user | `admin_required` |

**✓ = Manager-specific access**

#### D. Routes Implementation Details

##### Product Management (`backend/app/routes/products.py`)

Managers can:
- ✅ View all products
- ✅ Create new products
- ✅ Update product details
- ✅ Delete products
- ✅ Adjust stock levels
- ✅ Manage categories

```python
@products_bp.route('', methods=['POST'])
@manager_or_admin_required
def create_product():
    """Create new product (Manager/Admin only)"""
    # Full implementation...
```

##### Reporting (`backend/app/routes/reports.py`)

Managers have exclusive access to **cashier performance reports**:

```python
@reports_bp.route('/cashier', methods=['GET'])
@manager_or_admin_required
def get_cashier_report():
    """Get cashier performance report (Manager/Admin only)"""
    # Returns:
    # - Cashier ID, Name, Username
    # - Total orders processed
    # - Total revenue generated
    # - Date range filtering
```

This report shows metrics for all cashiers, helping managers monitor performance and sales.

### 2. Database Schema

#### User Table (SQL)

```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    role ENUM('ADMIN', 'MANAGER', 'CASHIER') NOT NULL DEFAULT 'CASHIER',
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX(username)
);
```

#### Migration Scripts

If you need to add MANAGER role to an existing database:

**Option 1: Python Migration** (`backend/migrations/add_manager_role.py`)
```bash
python backend/migrations/add_manager_role.py
```

**Option 2: Direct SQL** (`backend/migrations/add_manager_role.sql`)
```bash
mysql -u root -p coffee_shop_db < backend/migrations/add_manager_role.sql
```

Both scripts execute:
```sql
ALTER TABLE users MODIFY COLUMN role ENUM('ADMIN', 'MANAGER', 'CASHIER') NOT NULL DEFAULT 'CASHIER';
```

### 3. Frontend Implementation

#### A. Authentication Context (`frontend/src/contexts/AuthContext.jsx`)

Manager role helper functions:

```javascript
const isManager = () => {
    return user?.role === 'MANAGER';
};

const isManagerOrAdmin = () => {
    return user?.role === 'ADMIN' || user?.role === 'MANAGER';
};
```

These are exported in the context and used throughout the app:

```javascript
const { isManager, isManagerOrAdmin } = useAuth();
```

#### B. Navigation/Layout (`frontend/src/components/Layout.jsx`)

Manager is displayed in the navbar:
```jsx
{isManager() && <span className="badge bg-info ms-2">Manager</span>}
```

Navigation menu items available to managers:
- ✅ Dashboard/POS (view only)
- ✅ Products (full CRUD)
- ✅ Orders (view & cancel)
- ✅ Reports (all reports including cashier performance)

#### C. Manager Features by Page

##### **Products Page** (`frontend/src/pages/Products.jsx`)

**Manager Can:**
- ✅ View all products
- ✅ Search & filter products
- ✅ Create new products
- ✅ Edit product details (name, price, cost, stock, category)
- ✅ Delete products
- ✅ Adjust stock quantities
- ✅ Manage categories (create, edit, delete)

**Conditional Rendering:**
```jsx
{isManagerOrAdmin() && (
    <button className="btn btn-primary">Add Product</button>
)}
```

##### **Reports Page** (`frontend/src/pages/Reports.jsx`)

**All Users Can See:**
- 📊 Daily Sales Summary
- 📊 Item-wise Sales Analytics

**Manager/Admin Can Also See:**
- 👥 Cashier Performance Report
  - Cashier names & usernames
  - Number of orders processed
  - Total revenue generated
  - Sortable by revenue

**Implementation:**
```jsx
{isManagerOrAdmin() && (
    <Tab eventKey="cashier" title="Cashier Performance">
        {/* Cashier performance table */}
    </Tab>
)}
```

##### **Users Page** (`frontend/src/pages/Users.jsx`)

**Admin Only Can:**
- 👤 Create users
- 👤 Edit users
- 👤 Delete users
- 👤 Assign roles (ADMIN, MANAGER, CASHIER)

**UI Display:**
```jsx
user.role === 'MANAGER' ? 'info' : 
```

Managers are displayed with `info` badge color in the users list.

---

## 👥 Role Comparison Matrix

| Feature | Admin | Manager | Cashier |
|---------|-------|---------|---------|
| **Login** | ✅ | ✅ | ✅ |
| **POS (Create Orders)** | ✅ | ✅ | ✅ |
| **View Orders** | ✅ | ✅ | ✅ |
| **Cancel Orders** | ✅ | ❌ | ❌ |
| **Manage Products** | ✅ | ✅ | ❌ |
| **Manage Categories** | ✅ | ✅ | ❌ |
| **Adjust Stock** | ✅ | ✅ | ❌ |
| **View Sales Reports** | ✅ | ✅ | ✅ |
| **View Item Reports** | ✅ | ✅ | ✅ |
| **View Cashier Reports** | ✅ | ✅ | ❌ |
| **Manage Users** | ✅ | ❌ | ❌ |
| **Delete Users** | ✅ | ❌ | ❌ |

---

## 🚀 Default Credentials After Database Initialization

```bash
python backend/init_db.py
```

Creates three users:

| Role | Username | Password | Email |
|------|----------|----------|-------|
| Admin | `admin` | `admin123` | admin@coffeeshop.com |
| **Manager** | **manager** | **manager123** | manager@coffeeshop.com |
| Cashier | `cashier` | `cashier123` | cashier@coffeeshop.com |

⚠️ **IMPORTANT:** Change these passwords after first login!

---

## 📝 Key Manager Use Cases

### Use Case 1: Add New Product
1. Login as Manager (username: `manager`, password: `manager123`)
2. Navigate to Products
3. Click "Add Product" button
4. Fill in:
   - Product Name
   - SKU (optional)
   - Category
   - Description
   - Selling Price
   - Cost Price
   - Initial Stock
5. Click Save
6. Product is added and available for POS

### Use Case 2: Monitor Cashier Performance
1. Login as Manager
2. Navigate to Reports
3. Click on "Cashier Performance" tab
4. Select date range
5. View:
   - Total orders processed by each cashier
   - Total revenue per cashier
   - Performance comparison

### Use Case 3: Adjust Stock Levels
1. Login as Manager
2. Navigate to Products
3. Click on product row
4. Click "Adjust Stock" button
5. Enter new quantity
6. Add reason for adjustment
7. Submit - stock is updated and logged

### Use Case 4: Manage Categories
1. Login as Manager
2. Navigate to Products
3. Click "Manage Categories"
4. Can Create, Edit, Delete categories
5. Assign products to categories

---

## 🔗 Code File References

### Backend Files

**Model Definition:**
- `backend/app/models/user.py` - User model with RoleEnum

**Authentication:**
- `backend/app/routes/auth.py` - Auth endpoints & decorators
  - `@login_required` - Any logged-in user
  - `@admin_required` - Admin only
  - `@manager_or_admin_required` - Manager or Admin

**Manager-Specific Routes:**
- `backend/app/routes/products.py` - Product management (Manager/Admin)
- `backend/app/routes/categories.py` - Category management (Manager/Admin)
- `backend/app/routes/reports.py` - Cashier report (Manager/Admin)

**Database:**
- `backend/init_db.py` - Creates manager user with credentials
- `backend/migrations/add_manager_role.py` - Migration script
- `backend/migrations/add_manager_role.sql` - Direct SQL migration

### Frontend Files

**Authentication Context:**
- `frontend/src/contexts/AuthContext.jsx`
  - `isManager()` function
  - `isManagerOrAdmin()` function

**Manager Features:**
- `frontend/src/pages/Products.jsx` - Product CRUD (uses `isManagerOrAdmin()`)
- `frontend/src/pages/Reports.jsx` - Cashier report tab (uses `isManagerOrAdmin()`)
- `frontend/src/components/Layout.jsx` - Navigation showing manager badge

---

## 🔧 Configuration

### Backend Environment (`.env` file)

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=coffee_shop_db
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
TAX_RATE=0.05
```

### Database Setup

```sql
CREATE DATABASE coffee_shop_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Then run:
```bash
cd backend
python init_db.py  # Creates tables and seed data including manager user
```

---

## 🧪 Testing the Manager Role

### Step 1: Start Both Servers

**Backend (Terminal 1):**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python run.py  # Runs on http://localhost:5000
```

**Frontend (Terminal 2):**
```bash
cd frontend
npm install
npm start  # Runs on http://localhost:3000
```

### Step 2: Login as Manager

- URL: http://localhost:3000
- Username: `manager`
- Password: `manager123`

### Step 3: Test Manager Features

✅ **Test Product Management:**
1. Go to Products page
2. Click "Add Product"
3. Create a test product
4. Edit the product
5. Adjust stock

✅ **Test Cashier Report:**
1. Go to Reports
2. Select "Cashier Performance" tab
3. Select date range
4. View cashier metrics

✅ **Test Restrictions:**
1. Try accessing Users page (should be forbidden)
2. Try creating/editing users (should be forbidden)

---

## 📦 Dependencies

### Backend (`requirements.txt`)

Key packages for manager role:
- **Flask 3.0** - Web framework
- **SQLAlchemy 2.0** - ORM for database models
- **PyMySQL** - MySQL database driver
- **Flask-CORS** - Cross-origin requests
- **Werkzeug** - Password hashing
- **python-dotenv** - Environment configuration

### Frontend (`package.json`)

Key packages:
- **React 18.3** - UI framework
- **React Router** - Navigation
- **Axios** - HTTP client
- **React Bootstrap** - UI components
- **React Icons** - Icons

---

## 🛡️ Security Considerations

### Authentication Flow

1. **Manager logs in** with username/password
2. **Backend validates** credentials against password hash
3. **Session created** with user_id and role
4. **Role-based decorators** enforce permission checks on each API call
5. **Frontend checks role** before rendering manager-specific UI

### Password Security

- Passwords are **hashed using Werkzeug** `generate_password_hash()`
- Never stored as plain text
- Verified using `check_password_hash()` on login

### API Authorization

Every manager endpoint is protected:

```python
@manager_or_admin_required  # Decorator checks role before executing
def create_product():
    # Only executes if user role is MANAGER or ADMIN
```

### Session Management

Sessions stored server-side with:
- `user_id`
- `username`
- `role` (for quick checks)

---

## 📞 Troubleshooting

### Issue: Can't login as manager after database init
**Solution:**
- Verify `python init_db.py` ran successfully
- Check database: `SELECT * FROM users;`
- Ensure user with username 'manager' exists with role 'MANAGER'

### Issue: Manager can't access product management
**Solution:**
- Check user role in database: `SELECT role FROM users WHERE username='manager';`
- Should show: `MANAGER`
- Restart backend server

### Issue: Cashier report not showing for manager
**Solution:**
- Verify endpoint: `/api/reports/cashier`
- Check backend logs for permission errors
- Ensure manager is logged in (check session in browser DevTools)

### Issue: Can't modify existing database to add MANAGER role
**Solution:**
- Run migration: `python backend/migrations/add_manager_role.py`
- Or execute SQL: `mysql -u root -p coffee_shop_db < backend/migrations/add_manager_role.sql`
- Verify: `DESCRIBE users;` should show role enum with ADMIN, MANAGER, CASHIER

---

## ✨ Manager Role Features Summary

| Feature | Status | Location |
|---------|--------|----------|
| Manager login | ✅ Complete | Backend & Frontend auth |
| Product CRUD | ✅ Complete | Products page & API |
| Category management | ✅ Complete | Products page & API |
| Stock adjustment | ✅ Complete | Products page & API |
| View all reports | ✅ Complete | Reports page |
| Cashier performance report | ✅ Complete | Reports page - Cashier tab |
| View orders | ✅ Complete | Orders page |
| Create orders (POS) | ✅ Complete | POS page |
| Database role enum | ✅ Complete | users table |
| Migration scripts | ✅ Complete | migrations folder |
| Role-based decorators | ✅ Complete | auth.py |
| Frontend role checks | ✅ Complete | AuthContext.jsx |

---

## 📚 Additional Resources

- **Database Setup:** See `docs/SETUP_DATABASE.md`
- **Manual Setup:** See `docs/MANUAL_SETUP.md`
- **Quick Start:** See `QUICK_START.md`
- **Project Summary:** See `PROJECT_SUMMARY.md`

---

**Project Status:** ✅ Manager role fully implemented and ready for use!

*Documentation created: November 22, 2025*
*Version: 1.0.0*
