"""
Módulo de Pedidos - Routes
Responsabilidade: Endpoints HTTP de pedidos
"""
from flask import Blueprint, request, jsonify
from .services import OrderService

orders_bp = Blueprint('orders', __name__, url_prefix='/api/orders')


@orders_bp.route('', methods=['POST'])
def create_order():
    """Cria um novo pedido"""
    data = request.json
    
    # Validar dados
    if 'user_id' not in data or 'items' not in data:
        return jsonify({'error': 'Dados incompletos'}), 400
    
    order, error = OrderService.create_order(
        data['user_id'],
        data['items']
    )
    
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify(order.to_dict(include_items=True)), 201


@orders_bp.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Busca um pedido específico"""
    order = OrderService.get_order(order_id)
    
    if not order:
        return jsonify({'error': 'Pedido não encontrado'}), 404
    
    return jsonify(order.to_dict(include_items=True))


@orders_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_orders(user_id):
    """Lista pedidos de um usuário"""
    orders = OrderService.get_user_orders(user_id)
    return jsonify([o.to_dict() for o in orders])


@orders_bp.route('/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    """Atualiza status do pedido"""
    data = request.json
    
    if 'status' not in data:
        return jsonify({'error': 'Status não informado'}), 400
    
    order, error = OrderService.update_order_status(order_id, data['status'])
    
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify(order.to_dict())


@orders_bp.route('/<int:order_id>/cancel', methods=['POST'])
def cancel_order(order_id):
    """Cancela um pedido"""
    success, error = OrderService.cancel_order(order_id)
    
    if not success:
        return jsonify({'error': error}), 400
    
    return jsonify({'message': 'Pedido cancelado com sucesso'})
