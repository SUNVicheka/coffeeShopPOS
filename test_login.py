#!/usr/bin/env python
"""Test script to verify database and users"""
import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from dotenv import load_dotenv
load_dotenv()

from app import create_app, db
from app.models.user import User, RoleEnum

app = create_app('development')

with app.app_context():
    # Check if users exist
    print("\n=== Checking Database ===\n")
    
    admin = User.query.filter_by(username='admin').first()
    cashier = User.query.filter_by(username='cashier').first()
    
    print(f"Admin user exists: {admin is not None}")
    if admin:
        print(f"  - Username: {admin.username}")
        print(f"  - Role: {admin.role.value if admin.role else 'N/A'}")
        print(f"  - Active: {admin.is_active}")
        print(f"  - Password check (admin123): {admin.check_password('admin123')}")
    
    print(f"\nCashier user exists: {cashier is not None}")
    if cashier:
        print(f"  - Username: {cashier.username}")
        print(f"  - Role: {cashier.role.value if cashier.role else 'N/A'}")
        print(f"  - Active: {cashier.is_active}")
        print(f"  - Password check (cashier123): {cashier.check_password('cashier123')}")
    
    # If users don't exist, create them
    if not admin or not cashier:
        print("\n=== Creating Users ===\n")
        
        if not admin:
            admin = User(
                username='admin',
                full_name='Administrator',
                email='admin@coffeeshop.com',
                role=RoleEnum.ADMIN
            )
            admin.set_password('admin123')
            db.session.add(admin)
            print("✓ Created admin user")
        
        if not cashier:
            cashier = User(
                username='cashier',
                full_name='Cashier User',
                email='cashier@coffeeshop.com',
                role=RoleEnum.CASHIER
            )
            cashier.set_password('cashier123')
            db.session.add(cashier)
            print("✓ Created cashier user")
        
        db.session.commit()
        print("\n✓ Users created successfully!")
    
    print("\n=== Login Credentials ===")
    print("Admin:   username=admin, password=admin123")
    print("Cashier: username=cashier, password=cashier123")
    print()
