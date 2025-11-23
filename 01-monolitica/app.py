"""
ARQUITETURA MONOLÍTICA - E-commerce Simples
============================================
Todas as funcionalidades em uma única aplicação:
- Autenticação
- Produtos
- Carrinho
- Pedidos
- Pagamento
"""

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

# ============================================
# CONFIGURAÇÃO DA APLICAÇÃO MONOLÍTICA
# ============================================
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'chave-secreta-monolito'

db = SQLAlchemy(app)


# ============================================
# MODELOS DE DADOS (Todos no mesmo arquivo)
# ============================================

class User(db.Model):
    """Modelo de Usuário"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    orders = db.relationship('Order', backref='user', lazy=True)


class Product(db.Model):
    """Modelo de Produto"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Order(db.Model):
    """Modelo de Pedido"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    items = db.relationship('OrderItem', backref='order', lazy=True)


class OrderItem(db.Model):
    """Itens do Pedido"""
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    
    product = db.relationship('Product')


# ============================================
# LÓGICA DE NEGÓCIO (Tudo no mesmo arquivo)
# ============================================

class AuthService:
    """Serviço de Autenticação"""
    
    @staticmethod
    def register_user(username, email, password):
        if User.query.filter_by(username=username).first():
            return None, "Usuário já existe"
        
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        return user, None
    
    @staticmethod
    def authenticate(username, password):
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            return user
        return None


class ProductService:
    """Serviço de Produtos"""
    
    @staticmethod
    def create_product(name, description, price, stock):
        product = Product(
            name=name,
            description=description,
            price=price,
            stock=stock
        )
        db.session.add(product)
        db.session.commit()
        return product
    
    @staticmethod
    def get_all_products():
        return Product.query.all()
    
    @staticmethod
    def get_product(product_id):
        return Product.query.get(product_id)
    
    @staticmethod
    def update_stock(product_id, quantity):
        product = Product.query.get(product_id)
        if product and product.stock >= quantity:
            product.stock -= quantity
            db.session.commit()
            return True
        return False


class OrderService:
    """Serviço de Pedidos"""
    
    @staticmethod
    def create_order(user_id, items):
        """
        items: [{'product_id': 1, 'quantity': 2}, ...]
        """
        total = 0
        order_items = []
        
        # Validar produtos e calcular total
        for item in items:
            product = Product.query.get(item['product_id'])
            if not product or product.stock < item['quantity']:
                return None, "Produto indisponível"
            
            total += product.price * item['quantity']
            order_items.append({
                'product': product,
                'quantity': item['quantity'],
                'price': product.price
            })
        
        # Criar pedido
        order = Order(user_id=user_id, total=total)
        db.session.add(order)
        db.session.flush()
        
        # Adicionar itens e atualizar estoque
        for item in order_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item['product'].id,
                quantity=item['quantity'],
                price=item['price']
            )
            db.session.add(order_item)
            
            # Atualizar estoque
            item['product'].stock -= item['quantity']
        
        db.session.commit()
        return order, None
    
    @staticmethod
    def get_user_orders(user_id):
        return Order.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def update_order_status(order_id, status):
        order = Order.query.get(order_id)
        if order:
            order.status = status
            db.session.commit()
            return True
        return False


class PaymentService:
    """Serviço de Pagamento (Simulado)"""
    
    @staticmethod
    def process_payment(order_id, payment_method):
        """Simula processamento de pagamento"""
        order = Order.query.get(order_id)
        if not order:
            return False, "Pedido não encontrado"
        
        # Simular processamento
        if payment_method in ['credit_card', 'debit_card', 'pix']:
            order.status = 'paid'
            db.session.commit()
            return True, "Pagamento aprovado"
        
        return False, "Método de pagamento inválido"


# ============================================
# ROTAS DA API (Todas no mesmo arquivo)
# ============================================

@app.route('/')
def home():
    return jsonify({
        'message': 'E-commerce Monolítico - FIAP Demo',
        'architecture': 'Monolithic',
        'endpoints': {
            'auth': '/api/auth/*',
            'products': '/api/products/*',
            'orders': '/api/orders/*',
            'payment': '/api/payment/*'
        }
    })


# === ROTAS DE AUTENTICAÇÃO ===

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json
    user, error = AuthService.register_user(
        data['username'],
        data['email'],
        data['password']
    )
    
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email
    }), 201


@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    user = AuthService.authenticate(data['username'], data['password'])
    
    if not user:
        return jsonify({'error': 'Credenciais inválidas'}), 401
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'token': f'token-{user.id}'  # Simplificado
    })


# === ROTAS DE PRODUTOS ===

@app.route('/api/products', methods=['GET'])
def get_products():
    products = ProductService.get_all_products()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'description': p.description,
        'price': p.price,
        'stock': p.stock
    } for p in products])


@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.json
    product = ProductService.create_product(
        data['name'],
        data.get('description', ''),
        data['price'],
        data.get('stock', 0)
    )
    
    return jsonify({
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'stock': product.stock
    }), 201


@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = ProductService.get_product(product_id)
    if not product:
        return jsonify({'error': 'Produto não encontrado'}), 404
    
    return jsonify({
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'stock': product.stock
    })


# === ROTAS DE PEDIDOS ===

@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.json
    order, error = OrderService.create_order(
        data['user_id'],
        data['items']
    )
    
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify({
        'id': order.id,
        'total': order.total,
        'status': order.status,
        'created_at': order.created_at.isoformat()
    }), 201


@app.route('/api/orders/user/<int:user_id>', methods=['GET'])
def get_user_orders(user_id):
    orders = OrderService.get_user_orders(user_id)
    return jsonify([{
        'id': o.id,
        'total': o.total,
        'status': o.status,
        'created_at': o.created_at.isoformat(),
        'items_count': len(o.items)
    } for o in orders])


@app.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': 'Pedido não encontrado'}), 404
    
    return jsonify({
        'id': order.id,
        'total': order.total,
        'status': order.status,
        'created_at': order.created_at.isoformat(),
        'items': [{
            'product_name': item.product.name,
            'quantity': item.quantity,
            'price': item.price
        } for item in order.items]
    })


# === ROTAS DE PAGAMENTO ===

@app.route('/api/payment/process', methods=['POST'])
def process_payment():
    data = request.json
    success, message = PaymentService.process_payment(
        data['order_id'],
        data['payment_method']
    )
    
    if not success:
        return jsonify({'error': message}), 400
    
    return jsonify({'message': message, 'status': 'paid'})


# ============================================
# INICIALIZAÇÃO
# ============================================

def init_db():
    """Inicializa o banco de dados com dados de exemplo"""
    with app.app_context():
        db.create_all()
        
        # Verificar se já existem dados
        if Product.query.count() == 0:
            # Criar produtos de exemplo
            products = [
                Product(name='Notebook Dell', description='Core i7, 16GB RAM', price=3500.00, stock=10),
                Product(name='Mouse Logitech', description='Mouse sem fio', price=150.00, stock=50),
                Product(name='Teclado Mecânico', description='RGB, switches blue', price=450.00, stock=30),
                Product(name='Monitor LG 27"', description='Full HD, 75Hz', price=1200.00, stock=15),
                Product(name='Webcam HD', description='1080p, microfone integrado', price=300.00, stock=25),
            ]
            
            for product in products:
                db.session.add(product)
            
            db.session.commit()
            print("✅ Banco de dados inicializado com produtos de exemplo")


if __name__ == '__main__':
    init_db()
    print("\n" + "="*50)
    print("🏢 ARQUITETURA MONOLÍTICA - E-commerce")
    print("="*50)
    print("📦 Tudo em uma única aplicação")
    print("🗄️  Banco de dados único")
    print("🚀 Servidor: http://localhost:5000")
    print("="*50 + "\n")
    
    app.run(debug=True, port=5000)
