"""
Módulo de Pedidos - Models
Responsabilidade: Gerenciar dados de pedidos
"""
from shared.database import db
from datetime import datetime


class Order(db.Model):
    """Modelo de Pedido"""
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self, include_items=False):
        """Converte para dicionário"""
        result = {
            'id': self.id,
            'user_id': self.user_id,
            'total': self.total,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'items_count': len(self.items)
        }
        
        if include_items:
            result['items'] = [item.to_dict() for item in self.items]
        
        return result


class OrderItem(db.Model):
    """Itens do Pedido"""
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    
    product = db.relationship('Product', foreign_keys=[product_id])
    
    def to_dict(self):
        """Converte para dicionário"""
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_name': self.product.name if self.product else 'N/A',
            'quantity': self.quantity,
            'price': self.price,
            'subtotal': self.quantity * self.price
        }
