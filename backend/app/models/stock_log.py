from app import db
from datetime import datetime
from enum import Enum as PyEnum


class StockChangeTypeEnum(PyEnum):
    IN = 'IN'
    OUT = 'OUT'
    ADJUSTMENT = 'ADJUSTMENT'


class StockLog(db.Model):
    __tablename__ = 'stock_logs'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    change_type = db.Column(db.Enum(StockChangeTypeEnum), nullable=False)
    quantity_change = db.Column(db.Integer, nullable=False)
    previous_qty = db.Column(db.Integer, nullable=False)
    new_qty = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(200), nullable=True)
    actor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_name': self.product.name if self.product else None,
            'change_type': self.change_type.value if self.change_type else None,
            'quantity_change': self.quantity_change,
            'previous_qty': self.previous_qty,
            'new_qty': self.new_qty,
            'reason': self.reason,
            'actor_id': self.actor_id,
            'actor_name': self.actor.full_name if self.actor else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<StockLog {self.id}>'

