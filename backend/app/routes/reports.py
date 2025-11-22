from flask import Blueprint, request, jsonify
from app import db
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.user import User
from app.routes.auth import login_required, admin_required
from datetime import datetime, date, timedelta
from sqlalchemy import func, extract

reports_bp = Blueprint('reports', __name__, url_prefix='/api/reports')


@reports_bp.route('/sales', methods=['GET'])
@login_required
def get_sales_report():
    """Get sales report"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Default to today if no dates provided
    if not start_date:
        start_date = date.today().isoformat()
    if not end_date:
        end_date = date.today().isoformat()
    
    try:
        start = datetime.fromisoformat(start_date).replace(hour=0, minute=0, second=0)
        end = datetime.fromisoformat(end_date).replace(hour=23, minute=59, second=59)
    except (ValueError, AttributeError):
        return jsonify({'error': 'Invalid date format'}), 400
    
    # Get completed orders in date range
    orders = Order.query.filter(
        Order.status == 'COMPLETED',
        Order.created_at >= start,
        Order.created_at <= end
    ).all()
    
    total_orders = len(orders)
    total_revenue = sum(float(order.total) for order in orders)
    total_tax = sum(float(order.tax) for order in orders)
    total_subtotal = sum(float(order.subtotal) for order in orders)
    
    # Group by date
    daily_sales = {}
    for order in orders:
        order_date = order.created_at.date().isoformat()
        if order_date not in daily_sales:
            daily_sales[order_date] = {
                'date': order_date,
                'orders': 0,
                'revenue': 0.0,
                'tax': 0.0,
                'subtotal': 0.0
            }
        daily_sales[order_date]['orders'] += 1
        daily_sales[order_date]['revenue'] += float(order.total)
        daily_sales[order_date]['tax'] += float(order.tax)
        daily_sales[order_date]['subtotal'] += float(order.subtotal)
    
    return jsonify({
        'period': {
            'start_date': start_date,
            'end_date': end_date
        },
        'summary': {
            'total_orders': total_orders,
            'total_revenue': round(total_revenue, 2),
            'total_tax': round(total_tax, 2),
            'total_subtotal': round(total_subtotal, 2)
        },
        'daily_sales': list(daily_sales.values())
    }), 200


@reports_bp.route('/item-sales', methods=['GET'])
@login_required
def get_item_sales_report():
    """Get item-wise sales report"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Default to today if no dates provided
    if not start_date:
        start_date = date.today().isoformat()
    if not end_date:
        end_date = date.today().isoformat()
    
    try:
        start = datetime.fromisoformat(start_date).replace(hour=0, minute=0, second=0)
        end = datetime.fromisoformat(end_date).replace(hour=23, minute=59, second=59)
    except (ValueError, AttributeError):
        return jsonify({'error': 'Invalid date format'}), 400
    
    # Get order items from completed orders in date range
    order_items = db.session.query(
        OrderItem.product_id,
        Product.name.label('product_name'),
        func.sum(OrderItem.quantity).label('total_quantity'),
        func.sum(OrderItem.total_price).label('total_revenue')
    ).join(
        Product, OrderItem.product_id == Product.id
    ).join(
        Order, OrderItem.order_id == Order.id
    ).filter(
        Order.status == 'COMPLETED',
        Order.created_at >= start,
        Order.created_at <= end
    ).group_by(
        OrderItem.product_id,
        Product.name
    ).order_by(
        func.sum(OrderItem.total_price).desc()
    ).all()
    
    items = []
    for item in order_items:
        items.append({
            'product_id': item.product_id,
            'product_name': item.product_name,
            'total_quantity': int(item.total_quantity),
            'total_revenue': round(float(item.total_revenue), 2)
        })
    
    return jsonify({
        'period': {
            'start_date': start_date,
            'end_date': end_date
        },
        'items': items
    }), 200


@reports_bp.route('/cashier', methods=['GET'])
@admin_required
def get_cashier_report():
    """Get cashier performance report"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Default to today if no dates provided
    if not start_date:
        start_date = date.today().isoformat()
    if not end_date:
        end_date = date.today().isoformat()
    
    try:
        start = datetime.fromisoformat(start_date).replace(hour=0, minute=0, second=0)
        end = datetime.fromisoformat(end_date).replace(hour=23, minute=59, second=59)
    except (ValueError, AttributeError):
        return jsonify({'error': 'Invalid date format'}), 400
    
    # Get orders grouped by cashier
    cashier_stats = db.session.query(
        Order.cashier_id,
        User.full_name.label('cashier_name'),
        User.username.label('username'),
        func.count(Order.id).label('total_orders'),
        func.sum(Order.total).label('total_revenue')
    ).join(
        User, Order.cashier_id == User.id
    ).filter(
        Order.status == 'COMPLETED',
        Order.created_at >= start,
        Order.created_at <= end
    ).group_by(
        Order.cashier_id,
        User.full_name,
        User.username
    ).order_by(
        func.sum(Order.total).desc()
    ).all()
    
    cashiers = []
    for stat in cashier_stats:
        cashiers.append({
            'cashier_id': stat.cashier_id,
            'cashier_name': stat.cashier_name,
            'username': stat.username,
            'total_orders': int(stat.total_orders),
            'total_revenue': round(float(stat.total_revenue), 2)
        })
    
    return jsonify({
        'period': {
            'start_date': start_date,
            'end_date': end_date
        },
        'cashiers': cashiers
    }), 200

