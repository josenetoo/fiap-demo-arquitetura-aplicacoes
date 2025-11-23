"""
Módulo de Produtos - Services
Responsabilidade: Lógica de negócio de produtos
"""
from .models import Product
from shared.database import db


class ProductService:
    """Serviço de produtos"""
    
    @staticmethod
    def create_product(name, description, price, stock=0):
        """Cria um novo produto"""
        product = Product(
            name=name,
            description=description,
            price=price,
            stock=stock
        )
        
        db.session.add(product)
        db.session.commit()
        
        return product
    
    @staticmethod
    def get_all_products():
        """Lista todos os produtos"""
        return Product.query.all()
    
    @staticmethod
    def get_product(product_id):
        """Busca produto por ID"""
        return Product.query.get(product_id)
    
    @staticmethod
    def update_product(product_id, **kwargs):
        """Atualiza um produto"""
        product = Product.query.get(product_id)
        
        if not product:
            return None, "Produto não encontrado"
        
        for key, value in kwargs.items():
            if hasattr(product, key):
                setattr(product, key, value)
        
        db.session.commit()
        return product, None
    
    @staticmethod
    def delete_product(product_id):
        """Remove um produto"""
        product = Product.query.get(product_id)
        
        if not product:
            return False
        
        db.session.delete(product)
        db.session.commit()
        return True
    
    @staticmethod
    def check_availability(product_id, quantity):
        """Verifica disponibilidade de estoque"""
        product = Product.query.get(product_id)
        
        if not product:
            return False, "Produto não encontrado"
        
        if not product.has_stock(quantity):
            return False, f"Estoque insuficiente. Disponível: {product.stock}"
        
        return True, None
    
    @staticmethod
    def reserve_stock(product_id, quantity):
        """Reserva estoque de um produto"""
        product = Product.query.get(product_id)
        
        if not product:
            return False, "Produto não encontrado"
        
        if product.decrease_stock(quantity):
            db.session.commit()
            return True, None
        
        return False, "Estoque insuficiente"
