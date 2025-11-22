"""
Python script to add MANAGER role to existing database
Run this script if you already have a database with ADMIN and CASHIER roles

Usage:
    python migrations/add_manager_role.py
"""
import sys
import os

# Add parent directory to path to import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from app import create_app, db
from config import Config

def update_role_enum():
    """Update the role enum in the database to include MANAGER"""
    app = create_app()
    
    with app.app_context():
        print("Updating role enum to include MANAGER...")
        
        try:
            # Use raw SQL to alter the enum column
            # This is necessary because SQLAlchemy doesn't directly support enum modifications
            from sqlalchemy import text
            with db.engine.begin() as connection:
                connection.execute(text("""
                    ALTER TABLE users 
                    MODIFY COLUMN role ENUM('ADMIN', 'MANAGER', 'CASHIER') 
                    NOT NULL DEFAULT 'CASHIER'
                """))
            
            print("✓ Role enum updated successfully!")
            print("  Now supports: ADMIN, MANAGER, CASHIER")
            
        except Exception as e:
            print(f"✗ Error updating role enum: {e}")
            print("\nIf the enum already includes MANAGER, you can ignore this error.")
            print("Alternatively, you can run the SQL script directly:")
            print("  mysql -u root -p coffee_shop_db < migrations/add_manager_role.sql")
            return False
    
    return True

if __name__ == '__main__':
    try:
        update_role_enum()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nPlease check:")
        print("  1. MySQL service is running")
        print("  2. .env file exists and has correct credentials")
        print("  3. Database 'coffee_shop_db' exists")
        sys.exit(1)

