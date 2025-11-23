"""
Product Microservice - Serviço de Produtos
==========================================
Microsserviço independente de gerenciamento de produtos
"""

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ============================================
# MODELO DE DADOS
# ============================================

class Product(db.Model):
    """Modelo de produto - BD exclusivo deste serviço"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'stock': self.stock,
            'created_at': self.created_at.isoformat()
        }


# ============================================
# API REST
# ============================================

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'service': 'product-service',
        'status': 'healthy',
        'database': 'connected'
    })


@app.route('/api/products', methods=['GET'])
def list_products():
    """Lista todos os produtos"""
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])


@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Busca produto por ID"""
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({'error': 'Produto não encontrado'}), 404
    
    return jsonify(product.to_dict())


@app.route('/api/products', methods=['POST'])
def create_product():
    """Cria novo produto"""
    data = request.json
    
    if not all(k in data for k in ['name', 'price']):
        return jsonify({'error': 'Dados incompletos'}), 400
    
    product = Product(
        name=data['name'],
        description=data.get('description', ''),
        price=data['price'],
        stock=data.get('stock', 0)
    )
    
    db.session.add(product)
    db.session.commit()
    
    return jsonify(product.to_dict()), 201


@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Atualiza produto"""
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({'error': 'Produto não encontrado'}), 404
    
    data = request.json
    
    if 'name' in data:
        product.name = data['name']
    if 'description' in data:
        product.description = data['description']
    if 'price' in data:
        product.price = data['price']
    if 'stock' in data:
        product.stock = data['stock']
    
    db.session.commit()
    
    return jsonify(product.to_dict())


@app.route('/api/products/<int:product_id>/stock', methods=['POST'])
def check_stock(product_id):
    """Verifica disponibilidade de estoque"""
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({'error': 'Produto não encontrado'}), 404
    
    data = request.json
    quantity = data.get('quantity', 1)
    
    available = product.stock >= quantity
    
    return jsonify({
        'product_id': product_id,
        'available': available,
        'stock': product.stock,
        'requested': quantity
    })


@app.route('/api/products/<int:product_id>/reserve', methods=['POST'])
def reserve_stock(product_id):
    """Reserva estoque (usado por order-service)"""
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({'error': 'Produto não encontrado'}), 404
    
    data = request.json
    quantity = data.get('quantity', 1)
    
    if product.stock < quantity:
        return jsonify({
            'success': False,
            'error': 'Estoque insuficiente',
            'available': product.stock
        }), 400
    
    product.stock -= quantity
    db.session.commit()
    
    return jsonify({
        'success': True,
        'product_id': product_id,
        'reserved': quantity,
        'remaining': product.stock
    })


@app.route('/api/products/<int:product_id>/release', methods=['POST'])
def release_stock(product_id):
    """Libera estoque (cancelamento de pedido)"""
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({'error': 'Produto não encontrado'}), 404
    
    data = request.json
    quantity = data.get('quantity', 1)
    
    product.stock += quantity
    db.session.commit()
    
    return jsonify({
        'success': True,
        'product_id': product_id,
        'released': quantity,
        'total_stock': product.stock
    })


# ============================================
# INICIALIZAÇÃO
# ============================================

def init_db():
    with app.app_context():
        db.create_all()
        
        if Product.query.count() == 0:
            products = [
                Product(name='Notebook Dell', description='Core i7, 16GB', price=3500.00, stock=10),
                Product(name='Mouse Logitech', description='Sem fio', price=150.00, stock=50),
                Product(name='Teclado Mecânico', description='RGB', price=450.00, stock=30),
                Product(name='Monitor LG 27"', description='Full HD', price=1200.00, stock=15),
                Product(name='Webcam HD', description='1080p', price=300.00, stock=25),
            ]
            
            for product in products:
                db.session.add(product)
            
            db.session.commit()
            print("✅ Produtos de exemplo criados")


if __name__ == '__main__':
    init_db()
    
    print("\n" + "="*50)
    print("📦 PRODUCT MICROSERVICE")
    print("="*50)
    print("Serviço independente de produtos")
    print("Banco de dados: products.db (próprio)")
    print("Porta: 6002")
    print("="*50 + "\n")
    
    app.run(host='0.0.0.0', port=6002, debug=True)
