from flask import Blueprint, request, jsonify, session
from app import db
from app.models.product import Product
from app.models.category import Category
from app.models.stock_log import StockLog, StockChangeTypeEnum
from app.routes.auth import login_required, admin_required
from sqlalchemy import or_

products_bp = Blueprint('products', __name__, url_prefix='/api/products')


@products_bp.route('', methods=['GET'])
@login_required
def get_products():
    """Get all products with optional filtering"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    category_id = request.args.get('category_id', type=int)
    search = request.args.get('search', '').strip()
    available_only = request.args.get('available_only', 'false').lower() == 'true'
    
    query = Product.query
    
    # Filter by category
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    # Search by name or SKU
    if search:
        query = query.filter(
            or_(
                Product.name.ilike(f'%{search}%'),
                Product.sku.ilike(f'%{search}%')
            )
        )
    
    # Filter available products
    if available_only:
        query = query.filter_by(is_available=True)
    
    # Order by name
    query = query.order_by(Product.name)
    
    # Pagination
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'items': [product.to_dict() for product in pagination.items],
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages
    }), 200


@products_bp.route('/<int:product_id>', methods=['GET'])
@login_required
def get_product(product_id):
    """Get single product"""
    product = Product.query.get_or_404(product_id)
    return jsonify(product.to_dict()), 200


@products_bp.route('', methods=['POST'])
@admin_required
def create_product():
    """Create new product"""
    data = request.get_json()
    
    if not data or not data.get('name'):
        return jsonify({'error': 'Product name required'}), 400
    
    # Validate category
    category_id = data.get('category_id')
    if category_id:
        category = Category.query.get(category_id)
        if not category:
            return jsonify({'error': 'Invalid category'}), 400
    
    # Validate price
    try:
        price = float(data.get('price', 0))
        cost_price = float(data.get('cost_price', 0))
        if price < 0 or cost_price < 0:
            return jsonify({'error': 'Price must be positive'}), 400
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid price format'}), 400
    
    product = Product(
        name=data['name'].strip(),
        sku=data.get('sku', '').strip() or None,
        category_id=category_id,
        description=data.get('description', '').strip() or None,
        price=price,
        cost_price=cost_price,
        stock_qty=int(data.get('stock_qty', 0)),
        is_available=data.get('is_available', True),
        image_url=data.get('image_url', '').strip() or None
    )
    
    db.session.add(product)
    db.session.commit()
    
    return jsonify({
        'message': 'Product created successfully',
        'product': product.to_dict()
    }), 201


@products_bp.route('/<int:product_id>', methods=['PUT'])
@admin_required
def update_product(product_id):
    """Update product"""
    product = Product.query.get_or_404(product_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Update fields
    if 'name' in data:
        product.name = data['name'].strip()
    
    if 'sku' in data:
        sku = data['sku'].strip() or None
        if sku and sku != product.sku:
            existing = Product.query.filter_by(sku=sku).first()
            if existing:
                return jsonify({'error': 'SKU already exists'}), 400
        product.sku = sku
    
    if 'category_id' in data:
        category_id = data['category_id']
        if category_id:
            category = Category.query.get(category_id)
            if not category:
                return jsonify({'error': 'Invalid category'}), 400
        product.category_id = category_id
    
    if 'description' in data:
        product.description = data['description'].strip() or None
    
    if 'price' in data:
        try:
            price = float(data['price'])
            if price < 0:
                return jsonify({'error': 'Price must be positive'}), 400
            product.price = price
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid price format'}), 400
    
    if 'cost_price' in data:
        try:
            cost_price = float(data['cost_price'])
            if cost_price < 0:
                return jsonify({'error': 'Cost price must be positive'}), 400
            product.cost_price = cost_price
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid cost price format'}), 400
    
    if 'stock_qty' in data:
        product.stock_qty = int(data['stock_qty'])
    
    if 'is_available' in data:
        product.is_available = bool(data['is_available'])
    
    if 'image_url' in data:
        product.image_url = data['image_url'].strip() or None
    
    db.session.commit()
    
    return jsonify({
        'message': 'Product updated successfully',
        'product': product.to_dict()
    }), 200


@products_bp.route('/<int:product_id>', methods=['DELETE'])
@admin_required
def delete_product(product_id):
    """Delete product"""
    product = Product.query.get_or_404(product_id)
    
    # Check if product has orders
    if product.order_items.count() > 0:
        return jsonify({'error': 'Cannot delete product with existing orders'}), 400
    
    db.session.delete(product)
    db.session.commit()
    
    return jsonify({'message': 'Product deleted successfully'}), 200


@products_bp.route('/<int:product_id>/stock', methods=['POST'])
@admin_required
def update_stock(product_id):
    """Update product stock quantity"""
    product = Product.query.get_or_404(product_id)
    data = request.get_json()
    
    if not data or 'quantity' not in data:
        return jsonify({'error': 'Quantity required'}), 400
    
    try:
        quantity = int(data['quantity'])
        change_type = data.get('change_type', 'ADJUSTMENT')
        reason = data.get('reason', '').strip()
        actor_id = session.get('user_id')
        
        previous_qty = product.stock_qty
        product.stock_qty = quantity
        quantity_change = quantity - previous_qty
        
        # Create stock log
        stock_log = StockLog(
            product_id=product.id,
            change_type=StockChangeTypeEnum[change_type],
            quantity_change=quantity_change,
            previous_qty=previous_qty,
            new_qty=quantity,
            reason=reason or None,
            actor_id=actor_id
        )
        
        db.session.add(stock_log)
        db.session.commit()
        
        return jsonify({
            'message': 'Stock updated successfully',
            'product': product.to_dict()
        }), 200
    
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid quantity format'}), 400

