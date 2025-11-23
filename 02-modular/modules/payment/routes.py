"""
Módulo de Pagamento - Routes
Responsabilidade: Endpoints HTTP de pagamento
"""
from flask import Blueprint, request, jsonify
from .services import PaymentService

payment_bp = Blueprint('payment', __name__, url_prefix='/api/payment')


@payment_bp.route('/methods', methods=['GET'])
def get_payment_methods():
    """Lista métodos de pagamento disponíveis"""
    methods = PaymentService.get_payment_methods()
    return jsonify(methods)


@payment_bp.route('/process', methods=['POST'])
def process_payment():
    """Processa um pagamento"""
    data = request.json
    
    # Validar dados
    if 'order_id' not in data or 'payment_method' not in data:
        return jsonify({'error': 'Dados incompletos'}), 400
    
    success, message = PaymentService.process_payment(
        data['order_id'],
        data['payment_method'],
        data.get('payment_data')
    )
    
    if not success:
        return jsonify({'error': message}), 400
    
    return jsonify({
        'success': True,
        'message': message
    })


@payment_bp.route('/refund', methods=['POST'])
def refund_payment():
    """Processa estorno de pagamento"""
    data = request.json
    
    if 'order_id' not in data:
        return jsonify({'error': 'order_id não informado'}), 400
    
    success, message = PaymentService.refund_payment(data['order_id'])
    
    if not success:
        return jsonify({'error': message}), 400
    
    return jsonify({
        'success': True,
        'message': message
    })
