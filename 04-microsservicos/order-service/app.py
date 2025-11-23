"""
Order Microservice - Serviço de Pedidos
=======================================
Microsserviço que se comunica com outros serviços via HTTP
"""

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# URLs dos outros microsserviços
AUTH_SERVICE_URL = 'http://auth-service:6001'
PRODUCT_SERVICE_URL = 'http://product-service:6002'
PAYMENT_SERVICE_URL = 'http://payment-service:6004'


# ============================================
# MODELOS DE DADOS
# ============================================

class Order(db.Model):
    """Modelo de pedido - BD exclusivo deste serviço"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)  # Referência externa
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self, include_items=False):
        result = {
            'id': self.id,
            'user_id': self.user_id,
            'total': self.total,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }
        
        if include_items:
            result['items'] = [item.to_dict() for item in self.items]
        
        return result


class OrderItem(db.Model):
    """Itens do pedido"""
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)  # Referência externa
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'price': self.price,
            'subtotal': self.quantity * self.price
        }


# ============================================
# API REST
# ============================================

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'service': 'order-service',
        'status': 'healthy',
        'database': 'connected'
    })


@app.route('/api/orders', methods=['POST'])
def create_order():
    """
    Cria pedido - Demonstra comunicação entre microsserviços
    """
    data = request.json
    
    if not all(k in data for k in ['user_id', 'items']):
        return jsonify({'error': 'Dados incompletos'}), 400
    
    user_id = data['user_id']
    items = data['items']
    
    # 1. Validar usuário (chamada ao auth-service)
    try:
        auth_response = requests.get(
            f'{AUTH_SERVICE_URL}/api/users/{user_id}',
            timeout=5
        )
        
        if auth_response.status_code != 200:
            return jsonify({'error': 'Usuário não encontrado'}), 404
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Auth service indisponível'}), 503
    
    # 2. Validar produtos e reservar estoque (chamadas ao product-service)
    total = 0
    order_items = []
    
    for item in items:
        try:
            # Buscar produto
            product_response = requests.get(
                f'{PRODUCT_SERVICE_URL}/api/products/{item["product_id"]}',
                timeout=5
            )
            
            if product_response.status_code != 200:
                return jsonify({'error': f'Produto {item["product_id"]} não encontrado'}), 404
            
            product = product_response.json()
            
            # Reservar estoque
            reserve_response = requests.post(
                f'{PRODUCT_SERVICE_URL}/api/products/{item["product_id"]}/reserve',
                json={'quantity': item['quantity']},
                timeout=5
            )
            
            if reserve_response.status_code != 200:
                # Rollback: liberar estoques já reservados
                for reserved_item in order_items:
                    requests.post(
                        f'{PRODUCT_SERVICE_URL}/api/products/{reserved_item["product_id"]}/release',
                        json={'quantity': reserved_item['quantity']},
                        timeout=5
                    )
                
                return jsonify({'error': 'Estoque insuficiente'}), 400
            
            subtotal = product['price'] * item['quantity']
            total += subtotal
            
            order_items.append({
                'product_id': item['product_id'],
                'quantity': item['quantity'],
                'price': product['price']
            })
            
        except requests.exceptions.RequestException:
            return jsonify({'error': 'Product service indisponível'}), 503
    
    # 3. Criar pedido
    order = Order(user_id=user_id, total=total, status='pending')
    db.session.add(order)
    db.session.flush()
    
    for item_data in order_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item_data['product_id'],
            quantity=item_data['quantity'],
            price=item_data['price']
        )
        db.session.add(order_item)
    
    db.session.commit()
    
    return jsonify(order.to_dict(include_items=True)), 201


@app.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Busca pedido por ID"""
    order = Order.query.get(order_id)
    
    if not order:
        return jsonify({'error': 'Pedido não encontrado'}), 404
    
    return jsonify(order.to_dict(include_items=True))


@app.route('/api/orders/user/<int:user_id>', methods=['GET'])
def get_user_orders(user_id):
    """Lista pedidos de um usuário"""
    orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
    return jsonify([o.to_dict() for o in orders])


@app.route('/api/orders/<int:order_id>/status', methods=['PUT'])
def update_status(order_id):
    """Atualiza status do pedido"""
    order = Order.query.get(order_id)
    
    if not order:
        return jsonify({'error': 'Pedido não encontrado'}), 404
    
    data = request.json
    order.status = data.get('status', order.status)
    db.session.commit()
    
    return jsonify(order.to_dict())


# ============================================
# INICIALIZAÇÃO
# ============================================

def init_db():
    with app.app_context():
        db.create_all()
        print("✅ Banco de dados de pedidos inicializado")


if __name__ == '__main__':
    init_db()
    
    print("\n" + "="*50)
    print("🛒 ORDER MICROSERVICE")
    print("="*50)
    print("Serviço independente de pedidos")
    print("Banco de dados: orders.db (próprio)")
    print("Comunica com: auth-service, product-service")
    print("Porta: 6003")
    print("="*50 + "\n")
    
    app.run(host='0.0.0.0', port=6003, debug=True)
