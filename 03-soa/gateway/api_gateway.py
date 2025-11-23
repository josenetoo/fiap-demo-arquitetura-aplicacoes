"""
API Gateway - Ponto de entrada único para arquitetura SOA
=========================================================
Recebe requisições HTTP e as roteia através do ESB
"""

from flask import Flask, jsonify, request
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from esb.message_bus import esb
from esb.orchestrator import orchestrator

app = Flask(__name__)


@app.route('/')
def home():
    return jsonify({
        'message': 'SOA E-commerce - API Gateway',
        'architecture': 'Service-Oriented Architecture (SOA)',
        'description': 'Serviços se comunicam através do ESB',
        'components': {
            'esb': 'Enterprise Service Bus - Barramento central',
            'orchestrator': 'Orquestrador de fluxos complexos',
            'services': [
                'auth-service (5010)',
                'product-service (5011)',
                'order-service (5012)',
                'payment-service (5013)'
            ]
        },
        'endpoints': {
            'esb_status': '/esb/status',
            'create_order': 'POST /orders',
            'cancel_order': 'POST /orders/<id>/cancel'
        }
    })


@app.route('/esb/status')
def esb_status():
    """Status do ESB"""
    return jsonify(esb.get_service_status())


@app.route('/esb/messages')
def esb_messages():
    """Log de mensagens do ESB"""
    return jsonify({
        'messages': esb.get_message_log(limit=20)
    })


@app.route('/orders', methods=['POST'])
def create_order():
    """
    Cria pedido através do orquestrador
    Demonstra orquestração de múltiplos serviços via ESB
    """
    data = request.json
    
    result = orchestrator.orchestrate_order_creation(
        user_id=data.get('user_id'),
        items=data.get('items', [])
    )
    
    if 'error' in result:
        return jsonify(result), 400
    
    return jsonify(result), 201


@app.route('/orders/<int:order_id>/cancel', methods=['POST'])
def cancel_order(order_id):
    """
    Cancela pedido através do orquestrador
    Demonstra compensação e transações distribuídas
    """
    result = orchestrator.orchestrate_order_cancellation(order_id)
    
    if 'error' in result:
        return jsonify(result), 400
    
    return jsonify(result)


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Busca usuário via ESB"""
    response = esb.send_message(
        from_service='api-gateway',
        to_service='auth-service',
        operation='get_user',
        payload={'user_id': user_id}
    )
    
    return jsonify(response)


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🌐 API GATEWAY - Arquitetura SOA")
    print("="*60)
    print("Ponto de entrada único para todos os serviços")
    print("Roteia requisições através do ESB")
    print()
    print("🚀 Servidor: http://localhost:8000")
    print("="*60 + "\n")
    
    app.run(port=8000, debug=True)
