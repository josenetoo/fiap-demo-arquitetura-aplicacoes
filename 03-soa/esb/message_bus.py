"""
Enterprise Service Bus (ESB) - Barramento de Mensagens
======================================================
Componente central da arquitetura SOA que:
- Roteia mensagens entre serviços
- Transforma formatos de mensagens
- Implementa padrões de integração
- Monitora e registra comunicações
"""

import json
from datetime import datetime
from typing import Dict, Any, Callable, Optional
import threading


class MessageBus:
    """
    Barramento de mensagens centralizado (ESB)
    Todos os serviços se comunicam através deste barramento
    """
    
    def __init__(self):
        self.services = {}  # Registro de serviços
        self.message_log = []  # Log de mensagens
        self.transformers = {}  # Transformadores de mensagens
        self.lock = threading.Lock()
    
    def register_service(self, service_name: str, endpoint: str):
        """Registra um serviço no ESB"""
        with self.lock:
            self.services[service_name] = {
                'endpoint': endpoint,
                'status': 'active',
                'registered_at': datetime.utcnow().isoformat()
            }
            print(f"✅ Serviço registrado: {service_name} -> {endpoint}")
    
    def unregister_service(self, service_name: str):
        """Remove um serviço do ESB"""
        with self.lock:
            if service_name in self.services:
                del self.services[service_name]
                print(f"❌ Serviço removido: {service_name}")
    
    def send_message(self, 
                    from_service: str,
                    to_service: str,
                    operation: str,
                    payload: Dict[Any, Any],
                    transform: bool = True) -> Dict[Any, Any]:
        """
        Envia mensagem de um serviço para outro através do ESB
        
        Args:
            from_service: Serviço origem
            to_service: Serviço destino
            operation: Operação a ser executada
            payload: Dados da mensagem
            transform: Se deve aplicar transformações
        
        Returns:
            Resposta do serviço destino
        """
        message_id = f"msg-{len(self.message_log) + 1}"
        
        # Criar envelope da mensagem
        message = {
            'id': message_id,
            'from': from_service,
            'to': to_service,
            'operation': operation,
            'payload': payload,
            'timestamp': datetime.utcnow().isoformat(),
            'status': 'routing'
        }
        
        # Registrar mensagem
        self._log_message(message)
        
        print(f"\n📨 ESB: Roteando mensagem {message_id}")
        print(f"   De: {from_service} -> Para: {to_service}")
        print(f"   Operação: {operation}")
        
        # Verificar se serviço destino existe
        if to_service not in self.services:
            error_msg = f"Serviço {to_service} não encontrado no ESB"
            message['status'] = 'error'
            message['error'] = error_msg
            self._log_message(message)
            return {'error': error_msg}
        
        # Aplicar transformações se necessário
        if transform and f"{from_service}->{to_service}" in self.transformers:
            print(f"   🔄 Aplicando transformação de mensagem")
            transformer = self.transformers[f"{from_service}->{to_service}"]
            payload = transformer(payload)
        
        # Simular envio para o serviço (em produção seria HTTP/SOAP/etc)
        message['status'] = 'delivered'
        self._log_message(message)
        
        return {
            'message_id': message_id,
            'status': 'delivered',
            'payload': payload
        }
    
    def register_transformer(self, 
                           from_service: str,
                           to_service: str,
                           transformer: Callable):
        """
        Registra um transformador de mensagens entre dois serviços
        Característica importante do ESB
        """
        key = f"{from_service}->{to_service}"
        self.transformers[key] = transformer
        print(f"🔄 Transformador registrado: {key}")
    
    def _log_message(self, message: Dict[Any, Any]):
        """Registra mensagem no log (auditoria)"""
        with self.lock:
            self.message_log.append(message.copy())
    
    def get_message_log(self, limit: int = 50) -> list:
        """Retorna log de mensagens (monitoramento)"""
        with self.lock:
            return self.message_log[-limit:]
    
    def get_service_status(self) -> Dict[str, Any]:
        """Retorna status de todos os serviços"""
        with self.lock:
            return {
                'services': self.services.copy(),
                'total_messages': len(self.message_log),
                'transformers': list(self.transformers.keys())
            }
    
    def health_check(self) -> Dict[str, Any]:
        """Verifica saúde do ESB"""
        return {
            'status': 'healthy',
            'services_count': len(self.services),
            'messages_processed': len(self.message_log),
            'uptime': 'active'
        }


# Instância global do ESB (singleton)
esb = MessageBus()


# Exemplo de transformadores
def transform_user_to_customer(payload: Dict) -> Dict:
    """Transforma formato de usuário para cliente"""
    return {
        'customer_id': payload.get('user_id'),
        'customer_name': payload.get('username'),
        'customer_email': payload.get('email')
    }


def transform_order_to_payment(payload: Dict) -> Dict:
    """Transforma formato de pedido para pagamento"""
    return {
        'transaction_id': payload.get('order_id'),
        'amount': payload.get('total'),
        'currency': 'BRL'
    }


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚌 ENTERPRISE SERVICE BUS (ESB)")
    print("="*60)
    print("Barramento central de comunicação SOA")
    print("Todos os serviços se comunicam através do ESB")
    print("="*60 + "\n")
    
    # Exemplo de uso
    esb.register_service('auth-service', 'http://localhost:5010')
    esb.register_service('product-service', 'http://localhost:5011')
    esb.register_service('order-service', 'http://localhost:5012')
    esb.register_service('payment-service', 'http://localhost:5013')
    
    # Registrar transformadores
    esb.register_transformer('auth-service', 'order-service', transform_user_to_customer)
    esb.register_transformer('order-service', 'payment-service', transform_order_to_payment)
    
    print("\n✅ ESB inicializado e pronto para rotear mensagens")
    print(f"📊 Status: {esb.health_check()}")
