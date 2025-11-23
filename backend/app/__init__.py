from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()


def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)
    
    # Load configuration
    from config import config as config_dict
    app.config.from_object(config_dict[config_name])
    
    # Session configuration - MUST be before initializing extensions
    app.config['SESSION_COOKIE_SECURE'] = False
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['PERMANENT_SESSION_LIFETIME'] = 3600
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    
    # Allow all origins for development (temporary)
    CORS(
        app,
        origins="*",
        supports_credentials=True,
        allow_headers=['Content-Type', 'Authorization'],
        methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
        max_age=3600,
        expose_headers=['Content-Type']
    )
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.products import products_bp
    from app.routes.orders import orders_bp
    from app.routes.users import users_bp
    from app.routes.reports import reports_bp
    from app.routes.categories import categories_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(categories_bp)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app

