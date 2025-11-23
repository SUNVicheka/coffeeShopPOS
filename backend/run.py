import os
from dotenv import load_dotenv
from app import create_app, db
from app.models.user import User, RoleEnum
from app.models.category import Category
from app.models.product import Product

load_dotenv()

app = create_app(os.getenv('FLASK_ENV', 'development'))

# Configure session
app.config['SESSION_COOKIE_SECURE'] = False  # Allow over HTTP for development
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour


@app.shell_context_processor
def make_shell_context():
    """Create shell context for Flask CLI"""
    return {
        'db': db,
        'User': User,
        'Category': Category,
        'Product': Product
    }


@app.cli.command()
def init_db():
    """Initialize database with demo data"""
    print("Creating database tables...")
    db.create_all()
    print("✓ Database tables created")
    
    # Create default categories
    categories_data = [
        {'name': 'Hot Coffee', 'description': 'Hot coffee drinks'},
        {'name': 'Cold Coffee', 'description': 'Cold coffee drinks'},
        {'name': 'Tea', 'description': 'Tea drinks'},
        {'name': 'Pastries', 'description': 'Bakery items'},
        {'name': 'Sandwiches', 'description': 'Sandwich items'}
    ]
    
    print("\nCreating categories...")
    for cat_data in categories_data:
        if not Category.query.filter_by(name=cat_data['name']).first():
            category = Category(**cat_data)
            db.session.add(category)
            print(f"  ✓ Created category: {cat_data['name']}")
    db.session.commit()
    
    # Create default users
    users_data = [
        {
            'username': 'admin',
            'password': 'admin123',
            'full_name': 'Administrator',
            'email': 'admin@coffeeshop.com',
            'role': RoleEnum.ADMIN
        },
        {
            'username': 'cashier',
            'password': 'cashier123',
            'full_name': 'Cashier User',
            'email': 'cashier@coffeeshop.com',
            'role': RoleEnum.CASHIER
        }
    ]
    
    print("\nCreating users...")
    for user_data in users_data:
        if not User.query.filter_by(username=user_data['username']).first():
            user = User(
                username=user_data['username'],
                full_name=user_data['full_name'],
                email=user_data['email'],
                role=user_data['role']
            )
            user.set_password(user_data['password'])
            db.session.add(user)
            print(f"  ✓ Created user: {user_data['username']} ({user_data['role'].value})")
    db.session.commit()
    
    # Create sample products
    products_data = [
        {
            'name': 'Espresso',
            'sku': 'COFFEE-001',
            'category_name': 'Hot Coffee',
            'description': 'Rich and bold espresso',
            'price': 2.50,
            'cost_price': 0.50,
            'stock_qty': 100,
            'image_url': 'https://images.unsplash.com/photo-1514432324607-2e467f4af445?w=400&h=300&fit=crop'
        },
        {
            'name': 'Cappuccino',
            'sku': 'COFFEE-002',
            'category_name': 'Hot Coffee',
            'description': 'Espresso with steamed milk foam',
            'price': 3.50,
            'cost_price': 0.80,
            'stock_qty': 100,
            'image_url': 'https://images.unsplash.com/photo-1541183402695-c87eccf24f25?w=400&h=300&fit=crop'
        },
        {
            'name': 'Latte',
            'sku': 'COFFEE-003',
            'category_name': 'Hot Coffee',
            'description': 'Espresso with steamed milk',
            'price': 3.75,
            'cost_price': 0.90,
            'stock_qty': 100,
            'image_url': 'https://images.unsplash.com/photo-1488477181946-85a2a11eba04?w=400&h=300&fit=crop'
        },
        {
            'name': 'Iced Coffee',
            'sku': 'COFFEE-004',
            'category_name': 'Cold Coffee',
            'description': 'Cold brewed coffee',
            'price': 3.00,
            'cost_price': 0.70,
            'stock_qty': 100,
            'image_url': 'https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=400&h=300&fit=crop'
        },
        {
            'name': 'Green Tea',
            'sku': 'TEA-001',
            'category_name': 'Tea',
            'description': 'Refreshing green tea',
            'price': 2.00,
            'cost_price': 0.30,
            'stock_qty': 100,
            'image_url': 'https://images.unsplash.com/photo-1597318972223-e0a85be9f2a7?w=400&h=300&fit=crop'
        },
        {
            'name': 'Croissant',
            'sku': 'PAST-001',
            'category_name': 'Pastries',
            'description': 'Buttery French croissant',
            'price': 2.50,
            'cost_price': 0.60,
            'stock_qty': 50,
            'image_url': 'https://images.unsplash.com/photo-1585518419759-67c33ef3c0df?w=400&h=300&fit=crop'
        },
        {
            'name': 'Ham Sandwich',
            'sku': 'SAND-001',
            'category_name': 'Sandwiches',
            'description': 'Ham and cheese sandwich',
            'price': 5.50,
            'cost_price': 2.00,
            'stock_qty': 30,
            'image_url': 'https://images.unsplash.com/photo-1553979459-d2229ba7433b?w=400&h=300&fit=crop'
        }
    ]
    
    print("\nCreating products...")
    for prod_data in products_data:
        if not Product.query.filter_by(name=prod_data['name']).first():
            category = Category.query.filter_by(name=prod_data['category_name']).first()
            product = Product(
                name=prod_data['name'],
                sku=prod_data['sku'],
                category_id=category.id if category else None,
                description=prod_data['description'],
                price=prod_data['price'],
                cost_price=prod_data['cost_price'],
                stock_qty=prod_data['stock_qty'],
                image_url=prod_data.get('image_url'),
                is_available=True
            )
            db.session.add(product)
            print(f"  ✓ Created product: {prod_data['name']}")
    db.session.commit()
    
    print("\n✓ Database initialized successfully!")
    print("\nDefault login credentials:")
    print("  Admin:   username=admin, password=admin123")
    print("  Cashier: username=cashier, password=cashier123")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

