"""
Módulo de Produtos - Models
Responsabilidade: Gerenciar dados de produtos
"""
from shared.database import db
from datetime import datetime


class Product(db.Model):
    """Modelo de Produto"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Converte para dicionário"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'stock': self.stock,
            'created_at': self.created_at.isoformat()
        }
    
    def has_stock(self, quantity):
        """Verifica se há estoque disponível"""
        return self.stock >= quantity
    
    def decrease_stock(self, quantity):
        """Diminui o estoque"""
        if self.has_stock(quantity):
            self.stock -= quantity
            return True
        return False
