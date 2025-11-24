"""
Payment Service - Serviço de Pagamento (SOA)
============================================
Serviço independente que se comunica via ESB
"""

from flask import Flask, jsonify, request
import sys
import os
from datetime import datetime
import requests
import random

# Adicionar path do ESB
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from esb.message_bus import esb

app = Flask(__name__)

# Dados simulados
payments_db = {}
payment_counter = 1

# Preços dos produtos (simulado)
product_prices = {
    1: 1299.99,
    2: 2499.99,
    3: 199.99,
    4: 1899.99
}


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'service': 'payment-service', 'status': 'healthy'})


@app.route('/payments', methods=['GET'])
def get_payments():
    """Lista todos os pagamentos"""
    return jsonify(list(payments_db.values()))


@app.route('/payments/<int:payment_id>', methods=['GET'])
def get_payment(payment_id):
    """Busca pagamento por ID"""
    if payment_id in payments_db:
        return jsonify(payments_db[payment_id])
    
    return jsonify({'error': 'Pagamento não encontrado'}), 404


@app.route('/payments/process', methods=['POST'])
def process_payment():
    """Processa um pagamento"""
    global payment_counter
    
    data = request.json
    order_id = data.get('order_id')
    payment_method = data.get('payment_method', 'credit_card')
    
    if not order_id:
        return jsonify({'error': 'order_id é obrigatório'}), 400
    
    # Buscar dados do pedido
    try:
        order_response = requests.get(f'http://localhost:5012/orders/{order_id}', timeout=5)
        if order_response.status_code != 200:
            return jsonify({'error': 'Pedido não encontrado'}), 404
        
        order = order_response.json()
    except:
        return jsonify({'error': 'Erro ao buscar pedido'}), 500
    
    # Calcular total
    product_id = order['product_id']
    quantity = order['quantity']
    unit_price = product_prices.get(product_id, 100.0)
    total = unit_price * quantity
    
    # Simular processamento do pagamento
    # 90% de sucesso, 10% de falha
    success = random.random() > 0.1
    
    payment = {
        'id': payment_counter,
        'order_id': order_id,
        'amount': total,
        'payment_method': payment_method,
        'status': 'approved' if success else 'declined',
        'processed_at': datetime.now().isoformat(),
        'transaction_id': f'TXN_{payment_counter}_{random.randint(1000, 9999)}'
    }
    
    if not success:
        payment['error'] = 'Cartão recusado'
    
    payments_db[payment_counter] = payment
    payment_counter += 1
    
    # Se pagamento aprovado, confirmar pedido
    if success:
        try:
            requests.post(f'http://localhost:5012/orders/{order_id}/confirm', timeout=5)
        except:
            pass  # Log error but don't fail payment
    
    status_code = 200 if success else 400
    return jsonify(payment), status_code


@app.route('/payments/<int:payment_id>/refund', methods=['POST'])
def refund_payment(payment_id):
    """Estorna um pagamento"""
    if payment_id not in payments_db:
        return jsonify({'error': 'Pagamento não encontrado'}), 404
    
    payment = payments_db[payment_id]
    
    if payment['status'] != 'approved':
        return jsonify({'error': 'Apenas pagamentos aprovados podem ser estornados'}), 400
    
    # Simular estorno
    refund = {
        'id': len(payments_db) + 1,
        'original_payment_id': payment_id,
        'amount': payment['amount'],
        'status': 'refunded',
        'refunded_at': datetime.now().isoformat(),
        'refund_id': f'REF_{payment_id}_{random.randint(1000, 9999)}'
    }
    
    # Atualizar pagamento original
    payments_db[payment_id]['status'] = 'refunded'
    payments_db[payment_id]['refunded_at'] = datetime.now().isoformat()
    
    return jsonify(refund)


if __name__ == '__main__':
    # Registrar serviço no ESB
    esb.register_service('payment-service', 'http://localhost:5013')
    
    print("\n💳 Payment Service (SOA)")
    print("Porta: 5013")
    print("Registrado no ESB")
    
    app.run(port=5013, debug=True)
