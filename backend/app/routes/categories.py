from flask import Blueprint, request, jsonify
from app import db
from app.models.category import Category
from app.routes.auth import login_required, admin_required, manager_or_admin_required

categories_bp = Blueprint('categories', __name__, url_prefix='/api/categories')


@categories_bp.route('', methods=['GET'])
@login_required
def get_categories():
    """Get all categories"""
    categories = Category.query.order_by(Category.name).all()
    return jsonify([cat.to_dict() for cat in categories]), 200


@categories_bp.route('/<int:category_id>', methods=['GET'])
@login_required
def get_category(category_id):
    """Get single category"""
    category = Category.query.get_or_404(category_id)
    return jsonify(category.to_dict()), 200


@categories_bp.route('', methods=['POST'])
@manager_or_admin_required
def create_category():
    """Create new category"""
    data = request.get_json()
    
    if not data or not data.get('name'):
        return jsonify({'error': 'Category name required'}), 400
    
    name = data['name'].strip()
    
    # Check if category already exists
    existing = Category.query.filter_by(name=name).first()
    if existing:
        return jsonify({'error': 'Category already exists'}), 400
    
    category = Category(
        name=name,
        description=data.get('description', '').strip()
    )
    
    db.session.add(category)
    db.session.commit()
    
    return jsonify({
        'message': 'Category created successfully',
        'category': category.to_dict()
    }), 201


@categories_bp.route('/<int:category_id>', methods=['PUT'])
@manager_or_admin_required
def update_category(category_id):
    """Update category"""
    category = Category.query.get_or_404(category_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    if 'name' in data:
        name = data['name'].strip()
        if name != category.name:
            existing = Category.query.filter_by(name=name).first()
            if existing:
                return jsonify({'error': 'Category name already exists'}), 400
            category.name = name
    
    if 'description' in data:
        category.description = data['description'].strip()
    
    db.session.commit()
    
    return jsonify({
        'message': 'Category updated successfully',
        'category': category.to_dict()
    }), 200


@categories_bp.route('/<int:category_id>', methods=['DELETE'])
@manager_or_admin_required
def delete_category(category_id):
    """Delete category"""
    category = Category.query.get_or_404(category_id)
    
    # Check if category has products
    if category.products.count() > 0:
        return jsonify({'error': 'Cannot delete category with products'}), 400
    
    db.session.delete(category)
    db.session.commit()
    
    return jsonify({'message': 'Category deleted successfully'}), 200

