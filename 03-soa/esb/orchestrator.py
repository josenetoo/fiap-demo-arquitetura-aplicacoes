"""
Orquestrador de Serviços
========================
Coordena fluxos complexos que envolvem múltiplos serviços
Característica importante de SOA
"""

from message_bus import esb
from typing import Dict, Any


class ServiceOrchestrator:
    """
    Orquestrador que coordena chamadas a múltiplos serviços
    Em SOA, orquestrações complexas são gerenciadas centralmente
    """
    
    def __init__(self, esb_instance):
        self.esb = esb_instance
    
    def orchestrate_order_creation(self, user_id: int, items: list) -> Dict[str, Any]:
        """
        Orquestra o processo completo de criação de pedido:
        1. Validar usuário (auth-service)
        2. Validar produtos e estoque (product-service)
        3. Criar pedido (order-service)
        4. Processar pagamento (payment-service)
        5. Atualizar estoque (product-service)
        """
        print("\n🎭 ORQUESTRAÇÃO: Criação de Pedido")
        print("="*50)
        
        # Passo 1: Validar usuário
        print("1️⃣  Validando usuário...")
        user_response = self.esb.send_message(
            from_service='orchestrator',
            to_service='auth-service',
            operation='validate_user',
            payload={'user_id': user_id}
        )
        
        if 'error' in user_response:
            return {'error': 'Usuário inválido', 'step': 'auth'}
        
        # Passo 2: Validar produtos
        print("2️⃣  Validando produtos e estoque...")
        for item in items:
            product_response = self.esb.send_message(
                from_service='orchestrator',
                to_service='product-service',
                operation='check_stock',
                payload={
                    'product_id': item['product_id'],
                    'quantity': item['quantity']
                }
            )
            
            if 'error' in product_response:
                return {'error': f"Produto {item['product_id']} indisponível", 'step': 'products'}
        
        # Passo 3: Criar pedido
        print("3️⃣  Criando pedido...")
        order_response = self.esb.send_message(
            from_service='orchestrator',
            to_service='order-service',
            operation='create_order',
            payload={
                'user_id': user_id,
                'items': items
            }
        )
        
        if 'error' in order_response:
            return {'error': 'Erro ao criar pedido', 'step': 'order'}
        
        order_id = order_response['payload'].get('order_id')
        total = order_response['payload'].get('total')
        
        # Passo 4: Processar pagamento
        print("4️⃣  Processando pagamento...")
        payment_response = self.esb.send_message(
            from_service='orchestrator',
            to_service='payment-service',
            operation='process_payment',
            payload={
                'order_id': order_id,
                'amount': total,
                'payment_method': 'credit_card'
            },
            transform=True  # Aplica transformação de mensagem
        )
        
        if 'error' in payment_response:
            # Compensação: cancelar pedido
            print("❌ Pagamento falhou, cancelando pedido...")
            self.esb.send_message(
                from_service='orchestrator',
                to_service='order-service',
                operation='cancel_order',
                payload={'order_id': order_id}
            )
            return {'error': 'Pagamento recusado', 'step': 'payment'}
        
        # Passo 5: Atualizar estoque
        print("5️⃣  Atualizando estoque...")
        for item in items:
            self.esb.send_message(
                from_service='orchestrator',
                to_service='product-service',
                operation='decrease_stock',
                payload={
                    'product_id': item['product_id'],
                    'quantity': item['quantity']
                }
            )
        
        print("✅ Orquestração concluída com sucesso!")
        print("="*50 + "\n")
        
        return {
            'success': True,
            'order_id': order_id,
            'total': total,
            'status': 'completed'
        }
    
    def orchestrate_order_cancellation(self, order_id: int) -> Dict[str, Any]:
        """
        Orquestra o cancelamento de pedido:
        1. Buscar pedido (order-service)
        2. Processar estorno (payment-service)
        3. Devolver estoque (product-service)
        4. Cancelar pedido (order-service)
        """
        print("\n🎭 ORQUESTRAÇÃO: Cancelamento de Pedido")
        print("="*50)
        
        # Passo 1: Buscar pedido
        print("1️⃣  Buscando pedido...")
        order_response = self.esb.send_message(
            from_service='orchestrator',
            to_service='order-service',
            operation='get_order',
            payload={'order_id': order_id}
        )
        
        if 'error' in order_response:
            return {'error': 'Pedido não encontrado'}
        
        order = order_response['payload']
        
        # Passo 2: Processar estorno
        print("2️⃣  Processando estorno...")
        refund_response = self.esb.send_message(
            from_service='orchestrator',
            to_service='payment-service',
            operation='refund',
            payload={'order_id': order_id}
        )
        
        # Passo 3: Devolver estoque
        print("3️⃣  Devolvendo estoque...")
        for item in order.get('items', []):
            self.esb.send_message(
                from_service='orchestrator',
                to_service='product-service',
                operation='increase_stock',
                payload={
                    'product_id': item['product_id'],
                    'quantity': item['quantity']
                }
            )
        
        # Passo 4: Cancelar pedido
        print("4️⃣  Cancelando pedido...")
        cancel_response = self.esb.send_message(
            from_service='orchestrator',
            to_service='order-service',
            operation='cancel_order',
            payload={'order_id': order_id}
        )
        
        print("✅ Cancelamento concluído!")
        print("="*50 + "\n")
        
        return {
            'success': True,
            'order_id': order_id,
            'status': 'cancelled'
        }


# Instância global do orquestrador
orchestrator = ServiceOrchestrator(esb)


if __name__ == '__main__':
    print("\n🎭 Orquestrador de Serviços SOA")
    print("Coordena fluxos complexos entre múltiplos serviços")
