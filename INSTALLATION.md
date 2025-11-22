# Installation Guide

Quick installation guide for Coffee Shop Cashier Management System.

## Quick Start

### 1. Prerequisites Check

Ensure you have:
- Python 3.8+
- Node.js 16+
- MySQL Server 8.0+

Verify:
```bash
python --version
node --version
npm --version
mysql --version
```

### 2. Clone/Extract Project

If using Git:
```bash
git clone <repository-url>
cd coffeeShopPOS
```

Or extract the project folder to your desired location.

### 3. Database Setup

1. Create MySQL database:
```sql
CREATE DATABASE coffee_shop_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

See [docs/SETUP_DATABASE.md](docs/SETUP_DATABASE.md) for detailed instructions.

### 4. Backend Installation

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (see backend/.env.example)
# Edit .env with your MySQL credentials

# Initialize database
python init_db.py
```

### 5. Frontend Installation

```bash
cd frontend

# Install dependencies
npm install
```

### 6. Start Application

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate    # Windows
python run.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

### 7. Access Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

**Default Login:**
- Admin: `admin` / `admin123`
- Cashier: `cashier` / `cashier123`

---

## Detailed Documentation

- [Database Setup](docs/SETUP_DATABASE.md) - MySQL configuration
- [Manual Setup](docs/MANUAL_SETUP.md) - Step-by-step guide
- [README.md](README.md) - Project overview

---

## Troubleshooting

See [docs/MANUAL_SETUP.md](docs/MANUAL_SETUP.md#troubleshooting) for common issues.

---

**Note:** Make sure MySQL is running before starting the backend server!

