"""
Módulo de Produtos - Routes
Responsabilidade: Endpoints HTTP de produtos
"""
from flask import Blueprint, request, jsonify
from .services import ProductService

products_bp = Blueprint('products', __name__, url_prefix='/api/products')


@products_bp.route('', methods=['GET'])
def get_products():
    """Lista todos os produtos"""
    products = ProductService.get_all_products()
    return jsonify([p.to_dict() for p in products])


@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Busca um produto específico"""
    product = ProductService.get_product(product_id)
    
    if not product:
        return jsonify({'error': 'Produto não encontrado'}), 404
    
    return jsonify(product.to_dict())


@products_bp.route('', methods=['POST'])
def create_product():
    """Cria um novo produto"""
    data = request.json
    
    # Validar dados
    required_fields = ['name', 'price']
    if not all(k in data for k in required_fields):
        return jsonify({'error': 'Dados incompletos'}), 400
    
    product = ProductService.create_product(
        name=data['name'],
        description=data.get('description', ''),
        price=data['price'],
        stock=data.get('stock', 0)
    )
    
    return jsonify(product.to_dict()), 201


@products_bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Atualiza um produto"""
    data = request.json
    
    product, error = ProductService.update_product(product_id, **data)
    
    if error:
        return jsonify({'error': error}), 404
    
    return jsonify(product.to_dict())


@products_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Remove um produto"""
    success = ProductService.delete_product(product_id)
    
    if not success:
        return jsonify({'error': 'Produto não encontrado'}), 404
    
    return jsonify({'message': 'Produto removido com sucesso'}), 200


@products_bp.route('/<int:product_id>/availability', methods=['POST'])
def check_availability(product_id):
    """Verifica disponibilidade de estoque"""
    data = request.json
    quantity = data.get('quantity', 1)
    
    available, error = ProductService.check_availability(product_id, quantity)
    
    if not available:
        return jsonify({'available': False, 'error': error}), 400
    
    return jsonify({'available': True})
