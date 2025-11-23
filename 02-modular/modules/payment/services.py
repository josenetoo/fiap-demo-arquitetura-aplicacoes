"""
Módulo de Pagamento - Services
Responsabilidade: Lógica de negócio de pagamentos
"""
from modules.orders.services import OrderService


class PaymentService:
    """Serviço de pagamento"""
    
    VALID_METHODS = ['credit_card', 'debit_card', 'pix', 'boleto']
    
    @staticmethod
    def process_payment(order_id, payment_method, payment_data=None):
        """
        Processa um pagamento
        
        Args:
            order_id: ID do pedido
            payment_method: Método de pagamento
            payment_data: Dados adicionais do pagamento
        
        Returns:
            tuple: (success, message)
        """
        # Validar método de pagamento
        if payment_method not in PaymentService.VALID_METHODS:
            return False, f"Método inválido. Use: {', '.join(PaymentService.VALID_METHODS)}"
        
        # Buscar pedido
        order = OrderService.get_order(order_id)
        
        if not order:
            return False, "Pedido não encontrado"
        
        if order.status == 'paid':
            return False, "Pedido já foi pago"
        
        if order.status == 'cancelled':
            return False, "Pedido foi cancelado"
        
        # Simular processamento de pagamento
        success = PaymentService._simulate_payment(payment_method, order.total, payment_data)
        
        if success:
            # Atualizar status do pedido
            OrderService.update_order_status(order_id, 'paid')
            return True, f"Pagamento aprovado via {payment_method}"
        else:
            return False, "Pagamento recusado"
    
    @staticmethod
    def _simulate_payment(method, amount, data):
        """
        Simula processamento de pagamento
        Em produção, aqui seria integração com gateway de pagamento
        """
        # Simulação simples: sempre aprova
        # Em produção: integração com Stripe, PagSeguro, etc.
        
        if method == 'credit_card':
            # Validar dados do cartão
            if data and 'card_number' in data and 'cvv' in data:
                return True
            return False
        
        elif method == 'debit_card':
            # Validar dados do cartão
            if data and 'card_number' in data and 'cvv' in data:
                return True
            return False
        
        elif method == 'pix':
            # PIX sempre aprovado na simulação
            return True
        
        elif method == 'boleto':
            # Boleto sempre gera (em produção, geraria o boleto)
            return True
        
        return False
    
    @staticmethod
    def get_payment_methods():
        """Retorna métodos de pagamento disponíveis"""
        return [
            {
                'id': 'credit_card',
                'name': 'Cartão de Crédito',
                'requires_data': True
            },
            {
                'id': 'debit_card',
                'name': 'Cartão de Débito',
                'requires_data': True
            },
            {
                'id': 'pix',
                'name': 'PIX',
                'requires_data': False
            },
            {
                'id': 'boleto',
                'name': 'Boleto Bancário',
                'requires_data': False
            }
        ]
    
    @staticmethod
    def refund_payment(order_id):
        """
        Processa estorno de pagamento
        
        Returns:
            tuple: (success, message)
        """
        order = OrderService.get_order(order_id)
        
        if not order:
            return False, "Pedido não encontrado"
        
        if order.status != 'paid':
            return False, "Apenas pedidos pagos podem ser estornados"
        
        # Simular estorno
        # Em produção: integração com gateway
        
        # Cancelar pedido e devolver estoque
        success, error = OrderService.cancel_order(order_id)
        
        if success:
            return True, "Estorno processado com sucesso"
        
        return False, error or "Erro ao processar estorno"
