"""
Product Service - Serviço de Produtos (SOA)
==========================================
Serviço independente que se comunica via ESB
"""

from flask import Flask, jsonify, request
import sys
import os

# Adicionar path do ESB
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from esb.message_bus import esb

app = Flask(__name__)

# Dados simulados
products_db = {
    1: {
        'id': 1,
        'name': 'Smartphone Galaxy',
        'price': 1299.99,
        'stock': 50,
        'category': 'Eletrônicos'
    },
    2: {
        'id': 2,
        'name': 'Notebook Dell',
        'price': 2499.99,
        'stock': 25,
        'category': 'Informática'
    },
    3: {
        'id': 3,
        'name': 'Fone Bluetooth',
        'price': 199.99,
        'stock': 100,
        'category': 'Acessórios'
    },
    4: {
        'id': 4,
        'name': 'Smart TV 55"',
        'price': 1899.99,
        'stock': 15,
        'category': 'Eletrônicos'
    }
}


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'service': 'product-service', 'status': 'healthy'})


@app.route('/products', methods=['GET'])
def get_products():
    """Lista todos os produtos"""
    return jsonify(list(products_db.values()))


@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Busca produto por ID"""
    if product_id in products_db:
        return jsonify(products_db[product_id])
    
    return jsonify({'error': 'Produto não encontrado'}), 404


@app.route('/products/<int:product_id>/check-stock', methods=['POST'])
def check_stock(product_id):
    """Verifica estoque do produto"""
    data = request.json
    quantity = data.get('quantity', 1)
    
    if product_id not in products_db:
        return jsonify({'error': 'Produto não encontrado'}), 404
    
    product = products_db[product_id]
    available = product['stock'] >= quantity
    
    return jsonify({
        'product_id': product_id,
        'available': available,
        'stock': product['stock'],
        'requested': quantity
    })


@app.route('/products/<int:product_id>/reserve', methods=['POST'])
def reserve_stock(product_id):
    """Reserva estoque do produto"""
    data = request.json
    quantity = data.get('quantity', 1)
    
    if product_id not in products_db:
        return jsonify({'error': 'Produto não encontrado'}), 404
    
    product = products_db[product_id]
    
    if product['stock'] < quantity:
        return jsonify({
            'error': 'Estoque insuficiente',
            'available': product['stock'],
            'requested': quantity
        }), 400
    
    # Reservar estoque
    products_db[product_id]['stock'] -= quantity
    
    return jsonify({
        'product_id': product_id,
        'reserved': quantity,
        'remaining_stock': products_db[product_id]['stock']
    })


if __name__ == '__main__':
    # Registrar serviço no ESB
    esb.register_service('product-service', 'http://localhost:5011')
    
    print("\n📦 Product Service (SOA)")
    print("Porta: 5011")
    print("Registrado no ESB")
    
    app.run(port=5011, debug=True)
