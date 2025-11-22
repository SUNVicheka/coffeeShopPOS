from flask import Blueprint, request, jsonify, session
from app import db
from app.models.order import Order, OrderItem, OrderTypeEnum, PaymentMethodEnum, OrderStatusEnum
from app.models.product import Product
from app.models.stock_log import StockLog, StockChangeTypeEnum
from app.routes.auth import login_required, admin_required
from datetime import datetime, date

orders_bp = Blueprint('orders', __name__, url_prefix='/api/orders')


@orders_bp.route('', methods=['GET'])
@login_required
def get_orders():
    """Get all orders with optional filtering"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = Order.query
    
    # Filter by status
    if status:
        try:
            status_enum = OrderStatusEnum[status.upper()]
            query = query.filter_by(status=status_enum)
        except (KeyError, AttributeError):
            pass
    
    # Filter by date range
    if start_date:
        try:
            start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            query = query.filter(Order.created_at >= start)
        except (ValueError, AttributeError):
            pass
    
    if end_date:
        try:
            end = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            query = query.filter(Order.created_at <= end)
        except (ValueError, AttributeError):
            pass
    
    # Order by created_at descending
    query = query.order_by(Order.created_at.desc())
    
    # Pagination
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'items': [order.to_dict() for order in pagination.items],
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages
    }), 200


@orders_bp.route('/<int:order_id>', methods=['GET'])
@login_required
def get_order(order_id):
    """Get single order"""
    order = Order.query.get_or_404(order_id)
    return jsonify(order.to_dict()), 200


@orders_bp.route('', methods=['POST'])
@login_required
def create_order():
    """Create new order"""
    data = request.get_json()
    cashier_id = session.get('user_id')
    
    if not cashier_id:
        return jsonify({'error': 'User not logged in'}), 401
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    items = data.get('items', [])
    if not items or not isinstance(items, list):
        return jsonify({'error': 'Order items required'}), 400
    
    try:
        order_type = OrderTypeEnum[data.get('order_type', 'DINE_IN').upper()]
    except KeyError:
        return jsonify({'error': 'Invalid order type'}), 400
    
    try:
        payment_method = PaymentMethodEnum[data.get('payment_method', 'CASH').upper()]
    except KeyError:
        return jsonify({'error': 'Invalid payment method'}), 400
    
    # Calculate totals
    subtotal = 0.0
    order_items_data = []
    
    for item_data in items:
        product_id = item_data.get('product_id')
        quantity = int(item_data.get('quantity', 1))
        
        if quantity <= 0:
            continue
        
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': f'Product {product_id} not found'}), 400
        
        if not product.is_available:
            return jsonify({'error': f'Product {product.name} is not available'}), 400
        
        if product.stock_qty < quantity:
            return jsonify({'error': f'Insufficient stock for {product.name}'}), 400
        
        unit_price = float(product.price)
        total_price = unit_price * quantity
        
        order_items_data.append({
            'product': product,
            'quantity': quantity,
            'unit_price': unit_price,
            'total_price': total_price
        })
        
        subtotal += total_price
    
    if subtotal <= 0:
        return jsonify({'error': 'Order total must be greater than 0'}), 400
    
    # Calculate tax (5% default)
    from config import Config
    tax_rate = getattr(Config, 'TAX_RATE', 0.05)
    tax = subtotal * tax_rate
    total = subtotal + tax
    
    # Create order
    order = Order(
        order_number=Order.generate_order_number(),
        order_type=order_type,
        cashier_id=cashier_id,
        subtotal=subtotal,
        tax=tax,
        total=total,
        payment_method=payment_method,
        status=OrderStatusEnum.COMPLETED,
        notes=data.get('notes', '').strip() or None
    )
    
    db.session.add(order)
    db.session.flush()  # Get order ID
    
    # Create order items and update stock
    for item_data in order_items_data:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item_data['product'].id,
            quantity=item_data['quantity'],
            unit_price=item_data['unit_price'],
            total_price=item_data['total_price']
        )
        db.session.add(order_item)
        
        # Update product stock
        product = item_data['product']
        previous_qty = product.stock_qty
        product.stock_qty -= item_data['quantity']
        new_qty = product.stock_qty
        
        # Create stock log
        stock_log = StockLog(
            product_id=product.id,
            change_type=StockChangeTypeEnum.OUT,
            quantity_change=-item_data['quantity'],
            previous_qty=previous_qty,
            new_qty=new_qty,
            reason=f'Order {order.order_number}',
            actor_id=cashier_id
        )
        db.session.add(stock_log)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Order created successfully',
        'order': order.to_dict()
    }), 201


@orders_bp.route('/<int:order_id>', methods=['DELETE'])
@admin_required
def cancel_order(order_id):
    """Cancel order and restore stock"""
    order = Order.query.get_or_404(order_id)
    
    if order.status == OrderStatusEnum.CANCELLED:
        return jsonify({'error': 'Order already cancelled'}), 400
    
    actor_id = session.get('user_id')
    
    # Restore stock for each item
    for item in order.items:
        product = item.product
        previous_qty = product.stock_qty
        product.stock_qty += item.quantity
        new_qty = product.stock_qty
        
        # Create stock log
        stock_log = StockLog(
            product_id=product.id,
            change_type=StockChangeTypeEnum.IN,
            quantity_change=item.quantity,
            previous_qty=previous_qty,
            new_qty=new_qty,
            reason=f'Order {order.order_number} cancelled',
            actor_id=actor_id
        )
        db.session.add(stock_log)
    
    order.status = OrderStatusEnum.CANCELLED
    db.session.commit()
    
    return jsonify({
        'message': 'Order cancelled successfully',
        'order': order.to_dict()
    }), 200

