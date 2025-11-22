from flask import Blueprint, request, jsonify, session
from app import db
from app.models.user import User, RoleEnum
from app.routes.auth import login_required, admin_required

users_bp = Blueprint('users', __name__, url_prefix='/api/users')


@users_bp.route('', methods=['GET'])
@admin_required
def get_users():
    """Get all users"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    role = request.args.get('role')
    search = request.args.get('search', '').strip()
    
    query = User.query
    
    # Filter by role
    if role:
        try:
            role_enum = RoleEnum[role.upper()]
            query = query.filter_by(role=role_enum)
        except (KeyError, AttributeError):
            pass
    
    # Search by username or full_name
    if search:
        query = query.filter(
            db.or_(
                User.username.ilike(f'%{search}%'),
                User.full_name.ilike(f'%{search}%')
            )
        )
    
    query = query.order_by(User.username)
    
    # Pagination
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'items': [user.to_dict() for user in pagination.items],
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages
    }), 200


@users_bp.route('/<int:user_id>', methods=['GET'])
@admin_required
def get_user(user_id):
    """Get single user"""
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict()), 200


@users_bp.route('', methods=['POST'])
@admin_required
def create_user():
    """Create new user"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password required'}), 400
    
    username = data['username'].strip()
    password = data['password']
    
    # Check if username exists
    existing = User.query.filter_by(username=username).first()
    if existing:
        return jsonify({'error': 'Username already exists'}), 400
    
    # Validate role
    try:
        role = RoleEnum[data.get('role', 'CASHIER').upper()]
    except KeyError:
        return jsonify({'error': 'Invalid role'}), 400
    
    user = User(
        username=username,
        full_name=data.get('full_name', username).strip(),
        email=data.get('email', '').strip() or None,
        role=role,
        is_active=data.get('is_active', True)
    )
    user.set_password(password)
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': 'User created successfully',
        'user': user.to_dict()
    }), 201


@users_bp.route('/<int:user_id>', methods=['PUT'])
@admin_required
def update_user(user_id):
    """Update user"""
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Update fields
    if 'username' in data:
        username = data['username'].strip()
        if username != user.username:
            existing = User.query.filter_by(username=username).first()
            if existing:
                return jsonify({'error': 'Username already exists'}), 400
            user.username = username
    
    if 'full_name' in data:
        user.full_name = data['full_name'].strip()
    
    if 'email' in data:
        email = data['email'].strip() or None
        if email and email != user.email:
            existing = User.query.filter_by(email=email).first()
            if existing:
                return jsonify({'error': 'Email already exists'}), 400
        user.email = email
    
    if 'role' in data:
        try:
            user.role = RoleEnum[data['role'].upper()]
        except KeyError:
            return jsonify({'error': 'Invalid role'}), 400
    
    if 'password' in data and data['password']:
        user.set_password(data['password'])
    
    if 'is_active' in data:
        user.is_active = bool(data['is_active'])
    
    db.session.commit()
    
    return jsonify({
        'message': 'User updated successfully',
        'user': user.to_dict()
    }), 200


@users_bp.route('/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    """Delete user"""
    user = User.query.get_or_404(user_id)
    
    # Prevent deleting own account
    if user.id == session.get('user_id'):
        return jsonify({'error': 'Cannot delete your own account'}), 400
    
    # Check if user has orders
    if user.orders.count() > 0:
        return jsonify({'error': 'Cannot delete user with existing orders'}), 400
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'message': 'User deleted successfully'}), 200

