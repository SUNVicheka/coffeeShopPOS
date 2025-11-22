from app import db
from datetime import datetime
from enum import Enum as PyEnum
import random
import string


class OrderTypeEnum(PyEnum):
    DINE_IN = 'DINE_IN'
    TAKEAWAY = 'TAKEAWAY'


class PaymentMethodEnum(PyEnum):
    CASH = 'CASH'
    CARD = 'CARD'
    QR = 'QR'


class OrderStatusEnum(PyEnum):
    PENDING = 'PENDING'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'


class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_number = db.Column(db.String(20), unique=True, nullable=False, index=True)
    order_type = db.Column(db.Enum(OrderTypeEnum), nullable=False, default=OrderTypeEnum.DINE_IN)
    cashier_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    tax = db.Column(db.Numeric(10, 2), nullable=False, default=0.0)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    payment_method = db.Column(db.Enum(PaymentMethodEnum), nullable=True)
    status = db.Column(db.Enum(OrderStatusEnum), default=OrderStatusEnum.COMPLETED, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy='dynamic', cascade='all, delete-orphan')
    
    @staticmethod
    def generate_order_number():
        """Generate unique order number"""
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        random_str = ''.join(random.choices(string.digits, k=4))
        return f'ORD{timestamp}{random_str}'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'order_number': self.order_number,
            'order_type': self.order_type.value if self.order_type else None,
            'cashier_id': self.cashier_id,
            'cashier_name': self.cashier.full_name if self.cashier else None,
            'subtotal': float(self.subtotal) if self.subtotal else 0.0,
            'tax': float(self.tax) if self.tax else 0.0,
            'total': float(self.total) if self.total else 0.0,
            'payment_method': self.payment_method.value if self.payment_method else None,
            'status': self.status.value if self.status else None,
            'notes': self.notes,
            'items': [item.to_dict() for item in self.items],
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Order {self.order_number}>'


class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'product_name': self.product.name if self.product else None,
            'quantity': self.quantity,
            'unit_price': float(self.unit_price) if self.unit_price else 0.0,
            'total_price': float(self.total_price) if self.total_price else 0.0,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<OrderItem {self.id}>'

