from flask import Blueprint, request, jsonify, session
from app import db
from app.models.user import User, RoleEnum
from functools import wraps

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Login required'}), 401
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Login required'}), 401
        user = User.query.get(session['user_id'])
        # Handle role comparison - it might be Enum or string
        role_value = user.role.value if isinstance(user.role, RoleEnum) else str(user.role)
        if not user or role_value != RoleEnum.ADMIN.value:
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function


@auth_bp.route('/login', methods=['POST', 'OPTIONS'])
def login():
    """Login user"""
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Username and password required'}), 400
        
        username = data['username'].strip()
        password = data['password']
        
        # Query user from database
        user = User.query.filter_by(username=username).first()
        
        if not user:
            print(f"[AUTH] User not found: {username}")
            return jsonify({'error': 'Invalid username or password'}), 401
        
        # Check password
        if not user.check_password(password):
            print(f"[AUTH] Invalid password for user: {username}")
            return jsonify({'error': 'Invalid username or password'}), 401
        
        if not user.is_active:
            print(f"[AUTH] User inactive: {username}")
            return jsonify({'error': 'User account is inactive'}), 401
        
        # Create session
        session['user_id'] = user.id
        session['username'] = user.username
        session['role'] = user.role.value if isinstance(user.role, RoleEnum) else str(user.role)
        
        print(f"[AUTH] Login successful: {username} ({session['role']})")
        
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict()
        }), 200
    
    except Exception as e:
        print(f"[AUTH] Login error: {str(e)}")
        return jsonify({'error': f'Login failed: {str(e)}'}), 500


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout user"""
    session.clear()
    return jsonify({'message': 'Logout successful'}), 200


@auth_bp.route('/me', methods=['GET'])
@login_required
def get_current_user():
    """Get current logged-in user"""
    user = User.query.get(session['user_id'])
    
    if not user:
        session.clear()
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200


@auth_bp.route('/check', methods=['GET', 'OPTIONS'])
def check_session():
    """Check if user is logged in"""
    if request.method == 'OPTIONS':
        return '', 204
    
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user and user.is_active:
            return jsonify({
                'logged_in': True,
                'user': user.to_dict()
            }), 200
    
    return jsonify({'logged_in': False}), 200

