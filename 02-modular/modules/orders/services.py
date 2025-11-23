"""
Módulo de Pedidos - Services
Responsabilidade: Lógica de negócio de pedidos
"""
from .models import Order, OrderItem
from modules.products.services import ProductService
from modules.auth.services import AuthService
from shared.database import db


class OrderService:
    """Serviço de pedidos"""
    
    @staticmethod
    def create_order(user_id, items):
        """
        Cria um novo pedido
        
        Args:
            user_id: ID do usuário
            items: Lista de dicts [{'product_id': 1, 'quantity': 2}, ...]
        
        Returns:
            tuple: (Order, error_message)
        """
        # Validar usuário
        user = AuthService.get_user_by_id(user_id)
        if not user:
            return None, "Usuário não encontrado"
        
        # Validar items
        if not items or len(items) == 0:
            return None, "Pedido deve conter ao menos um item"
        
        total = 0
        order_items = []
        
        # Validar produtos e calcular total
        for item in items:
            product = ProductService.get_product(item['product_id'])
            
            if not product:
                return None, f"Produto {item['product_id']} não encontrado"
            
            quantity = item['quantity']
            
            # Verificar estoque
            available, error = ProductService.check_availability(product.id, quantity)
            if not available:
                return None, error
            
            # Calcular subtotal
            subtotal = product.price * quantity
            total += subtotal
            
            order_items.append({
                'product': product,
                'quantity': quantity,
                'price': product.price
            })
        
        # Criar pedido
        order = Order(user_id=user_id, total=total, status='pending')
        db.session.add(order)
        db.session.flush()  # Para obter o ID do pedido
        
        # Adicionar itens e reservar estoque
        for item_data in order_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item_data['product'].id,
                quantity=item_data['quantity'],
                price=item_data['price']
            )
            db.session.add(order_item)
            
            # Reservar estoque
            success, error = ProductService.reserve_stock(
                item_data['product'].id,
                item_data['quantity']
            )
            
            if not success:
                db.session.rollback()
                return None, error
        
        db.session.commit()
        return order, None
    
    @staticmethod
    def get_order(order_id):
        """Busca pedido por ID"""
        return Order.query.get(order_id)
    
    @staticmethod
    def get_user_orders(user_id):
        """Lista pedidos de um usuário"""
        return Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
    
    @staticmethod
    def update_order_status(order_id, status):
        """Atualiza status do pedido"""
        valid_statuses = ['pending', 'paid', 'processing', 'shipped', 'delivered', 'cancelled']
        
        if status not in valid_statuses:
            return None, f"Status inválido. Use: {', '.join(valid_statuses)}"
        
        order = Order.query.get(order_id)
        
        if not order:
            return None, "Pedido não encontrado"
        
        order.status = status
        db.session.commit()
        
        return order, None
    
    @staticmethod
    def cancel_order(order_id):
        """Cancela um pedido e devolve estoque"""
        order = Order.query.get(order_id)
        
        if not order:
            return False, "Pedido não encontrado"
        
        if order.status in ['shipped', 'delivered']:
            return False, "Não é possível cancelar pedido já enviado"
        
        # Devolver estoque
        for item in order.items:
            product = ProductService.get_product(item.product_id)
            if product:
                product.stock += item.quantity
        
        order.status = 'cancelled'
        db.session.commit()
        
        return True, None
