"""
Order Service - Serviço de Pedidos (SOA)
========================================
Serviço independente que se comunica via ESB
"""

from flask import Flask, jsonify, request
import sys
import os
from datetime import datetime
import requests

# Adicionar path do ESB
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from esb.message_bus import esb

app = Flask(__name__)

# Dados simulados
orders_db = {}
order_counter = 1


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'service': 'order-service', 'status': 'healthy'})


@app.route('/orders', methods=['GET'])
def get_orders():
    """Lista todos os pedidos"""
    return jsonify(list(orders_db.values()))


@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Busca pedido por ID"""
    if order_id in orders_db:
        return jsonify(orders_db[order_id])
    
    return jsonify({'error': 'Pedido não encontrado'}), 404


@app.route('/orders', methods=['POST'])
def create_order():
    """Cria um novo pedido"""
    global order_counter
    
    data = request.json
    user_id = data.get('user_id')
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    if not user_id or not product_id:
        return jsonify({'error': 'user_id e product_id são obrigatórios'}), 400
    
    # Validar usuário via ESB
    try:
        auth_response = requests.post('http://localhost:5010/validate', 
                                    json={'user_id': user_id}, timeout=5)
        if not auth_response.json().get('valid'):
            return jsonify({'error': 'Usuário inválido'}), 400
    except:
        return jsonify({'error': 'Erro ao validar usuário'}), 500
    
    # Verificar estoque via ESB
    try:
        stock_response = requests.post(f'http://localhost:5011/products/{product_id}/check-stock',
                                     json={'quantity': quantity}, timeout=5)
        if not stock_response.json().get('available'):
            return jsonify({'error': 'Estoque insuficiente'}), 400
    except:
        return jsonify({'error': 'Erro ao verificar estoque'}), 500
    
    # Criar pedido
    order = {
        'id': order_counter,
        'user_id': user_id,
        'product_id': product_id,
        'quantity': quantity,
        'status': 'created',
        'created_at': datetime.now().isoformat(),
        'total': 0  # Será calculado pelo payment service
    }
    
    orders_db[order_counter] = order
    order_counter += 1
    
    return jsonify(order), 201


@app.route('/orders/<int:order_id>/confirm', methods=['POST'])
def confirm_order(order_id):
    """Confirma um pedido após pagamento"""
    if order_id not in orders_db:
        return jsonify({'error': 'Pedido não encontrado'}), 404
    
    # Reservar estoque
    order = orders_db[order_id]
    try:
        reserve_response = requests.post(
            f'http://localhost:5011/products/{order["product_id"]}/reserve',
            json={'quantity': order['quantity']}, timeout=5)
        
        if reserve_response.status_code != 200:
            return jsonify({'error': 'Erro ao reservar estoque'}), 500
    except:
        return jsonify({'error': 'Erro ao comunicar com product service'}), 500
    
    # Atualizar status
    orders_db[order_id]['status'] = 'confirmed'
    orders_db[order_id]['confirmed_at'] = datetime.now().isoformat()
    
    return jsonify(orders_db[order_id])


@app.route('/orders/<int:order_id>/cancel', methods=['POST'])
def cancel_order(order_id):
    """Cancela um pedido"""
    if order_id not in orders_db:
        return jsonify({'error': 'Pedido não encontrado'}), 404
    
    orders_db[order_id]['status'] = 'cancelled'
    orders_db[order_id]['cancelled_at'] = datetime.now().isoformat()
    
    return jsonify(orders_db[order_id])


if __name__ == '__main__':
    # Registrar serviço no ESB
    esb.register_service('order-service', 'http://localhost:5012')
    
    print("\n📋 Order Service (SOA)")
    print("Porta: 5012")
    print("Registrado no ESB")
    
    app.run(port=5012, debug=True)
