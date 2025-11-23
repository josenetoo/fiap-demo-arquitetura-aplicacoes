"""
Payment Microservice - Serviço de Pagamento
===========================================
Microsserviço stateless de processamento de pagamentos
"""

from flask import Flask, jsonify, request
from datetime import datetime
import random

app = Flask(__name__)

# Simulação de histórico de pagamentos (em produção seria BD)
payments = {}


@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'service': 'payment-service',
        'status': 'healthy'
    })


@app.route('/api/payments/process', methods=['POST'])
def process_payment():
    """
    Processa pagamento
    Simula integração com gateway de pagamento
    """
    data = request.json
    
    if not all(k in data for k in ['order_id', 'amount']):
        return jsonify({'error': 'Dados incompletos'}), 400
    
    order_id = data['order_id']
    amount = data['amount']
    payment_method = data.get('payment_method', 'credit_card')
    
    # Simular processamento (90% de aprovação)
    approved = random.random() < 0.9
    
    payment_id = f"pay-{len(payments) + 1}"
    
    payment = {
        'id': payment_id,
        'order_id': order_id,
        'amount': amount,
        'payment_method': payment_method,
        'status': 'approved' if approved else 'declined',
        'processed_at': datetime.utcnow().isoformat()
    }
    
    payments[payment_id] = payment
    
    if approved:
        return jsonify({
            'success': True,
            'payment_id': payment_id,
            'status': 'approved',
            'message': 'Pagamento aprovado'
        }), 200
    else:
        return jsonify({
            'success': False,
            'payment_id': payment_id,
            'status': 'declined',
            'message': 'Pagamento recusado'
        }), 400


@app.route('/api/payments/<payment_id>', methods=['GET'])
def get_payment(payment_id):
    """Busca informações de um pagamento"""
    if payment_id not in payments:
        return jsonify({'error': 'Pagamento não encontrado'}), 404
    
    return jsonify(payments[payment_id])


@app.route('/api/payments/refund', methods=['POST'])
def refund_payment():
    """Processa estorno"""
    data = request.json
    
    if 'payment_id' not in data:
        return jsonify({'error': 'payment_id não informado'}), 400
    
    payment_id = data['payment_id']
    
    if payment_id not in payments:
        return jsonify({'error': 'Pagamento não encontrado'}), 404
    
    payment = payments[payment_id]
    
    if payment['status'] != 'approved':
        return jsonify({'error': 'Apenas pagamentos aprovados podem ser estornados'}), 400
    
    payment['status'] = 'refunded'
    payment['refunded_at'] = datetime.utcnow().isoformat()
    
    return jsonify({
        'success': True,
        'payment_id': payment_id,
        'status': 'refunded',
        'message': 'Estorno processado'
    })


@app.route('/api/payments/methods', methods=['GET'])
def get_payment_methods():
    """Lista métodos de pagamento disponíveis"""
    return jsonify([
        {'id': 'credit_card', 'name': 'Cartão de Crédito'},
        {'id': 'debit_card', 'name': 'Cartão de Débito'},
        {'id': 'pix', 'name': 'PIX'},
        {'id': 'boleto', 'name': 'Boleto Bancário'}
    ])


if __name__ == '__main__':
    print("\n" + "="*50)
    print("💳 PAYMENT MICROSERVICE")
    print("="*50)
    print("Serviço independente de pagamentos")
    print("Stateless (sem banco de dados)")
    print("Porta: 6004")
    print("="*50 + "\n")
    
    app.run(host='0.0.0.0', port=6004, debug=True)
