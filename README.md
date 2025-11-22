# Coffee Shop Cashier Management System

A complete Cashier Management System for a coffee shop built with React + Bootstrap frontend and Python Flask backend with MySQL database.

## 🚀 Features

- ✅ **User Authentication** - Login/Logout with role-based access
- ✅ **Product Management** - Add, Edit, Delete, Search products with categories
- ✅ **Inventory Management** - Stock tracking and management
- ✅ **Order Processing** - Create orders, add items, calculate totals
- ✅ **Billing & Receipt** - Generate bills with on-screen receipt display
- ✅ **Sales Reports** - Daily sales, item-wise reports, cashier performance
- ✅ **User Management** - Manage users with different roles (Admin, Cashier)
- ✅ **Payment Methods** - Cash, Card, QR payment support
- ✅ **Product Categories** - Organize products by categories

## 🏗️ Technology Stack

### Frontend
- React 18.3
- Bootstrap 5
- JavaScript/TypeScript
- React Router
- Axios for API calls

### Backend
- Python 3.8+
- Flask 3.0
- SQLAlchemy ORM
- MySQL Database
- Flask-CORS
- Flask-JWT-Extended (for authentication)

### Database
- MySQL 8.0+

## 📋 Prerequisites

Before starting, ensure you have:

1. **Python 3.8+** installed
2. **Node.js 16+** installed
3. **MySQL Server** installed and running
4. **Git** (optional, for version control)

## 🚀 Quick Start

### Option 1: Automated Scripts (Recommended)

**Windows:**
1. Create MySQL database (see below)
2. Configure `.env` file in `backend/` directory
3. Double-click `start_backend.bat` (Terminal 1)
4. Double-click `start_frontend.bat` (Terminal 2)

**macOS/Linux:**
1. Create MySQL database (see below)
2. Configure `.env` file in `backend/` directory
3. Make scripts executable: `chmod +x start_backend.sh start_frontend.sh`
4. Run `./start_backend.sh` (Terminal 1)
5. Run `./start_frontend.sh` (Terminal 2)

### Option 2: Manual Setup

### 1. Database Setup

First, create the MySQL database:

```sql
CREATE DATABASE coffee_shop_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

See `docs/SETUP_DATABASE.md` for detailed database setup instructions.

### 2. Backend Setup

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt

# Create .env file (copy env_template.txt to .env and edit)
# Then initialize database
python init_db.py

# Run the server
python run.py
```

Backend will run on `http://localhost:5000`

### 3. Frontend Setup

```bash
cd frontend
npm install
npm start
```

Frontend will run on `http://localhost:3000`

### 4. Login

- Open browser: http://localhost:3000
- **Admin:** username=`admin`, password=`admin123`
- **Cashier:** username=`cashier`, password=`cashier123`

## 📁 Project Structure

```
coffeeShopPOS/
├── backend/              # Flask Backend
│   ├── app/
│   │   ├── models/      # Database models
│   │   ├── routes/      # API routes
│   │   └── utils/       # Utility functions
│   ├── config.py        # Configuration
│   ├── run.py           # Application entry point
│   ├── init_db.py       # Database initialization
│   └── requirements.txt # Python dependencies
│
├── frontend/            # React Frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── pages/       # Page components
│   │   ├── services/    # API services
│   │   └── contexts/    # React contexts
│   ├── public/          # Static files
│   └── package.json     # Node dependencies
│
└── docs/                # Documentation
    ├── SETUP_DATABASE.md
    ├── API_DOCUMENTATION.md
    └── MANUAL_SETUP.md
```

## 🔑 Default Login Credentials

After database initialization:

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |
| Cashier | cashier | cashier123 |

**⚠️ Important:** Change these passwords after first login!

## 📚 Documentation

- **[SETUP_DATABASE.md](docs/SETUP_DATABASE.md)** - MySQL database setup guide
- **[MANUAL_SETUP.md](docs/MANUAL_SETUP.md)** - Manual setup instructions
- **[API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md)** - API endpoints reference

## 🛠️ Development

### Backend Development
```bash
cd backend
python run.py  # Runs on http://localhost:5000
```

### Frontend Development
```bash
cd frontend
npm start  # Runs on http://localhost:3000
```

## 📝 Features in Detail

### Authentication
- Simple username/password login
- Session-based authentication
- Role-based access control (Admin, Cashier)

### Product Management
- CRUD operations for products
- Category management
- Stock quantity tracking
- Search and filter functionality

### Order Processing
- Add items to cart
- Modify quantities
- Calculate subtotal, tax, total
- Multiple payment methods
- Order history

### Receipt Generation
- On-screen receipt display
- Print-friendly format
- Order details and totals

### Reports
- Daily sales reports
- Item-wise sales analytics
- Cashier performance metrics

## 🔒 Security Features

- Password hashing (Werkzeug)
- SQL injection prevention (SQLAlchemy ORM)
- CORS configuration
- Input validation
- Role-based access control

## 📄 License

This project is for educational purposes.

---

For detailed setup instructions, see the [docs](docs/) folder.

