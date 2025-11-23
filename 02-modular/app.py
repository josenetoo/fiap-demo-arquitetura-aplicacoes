"""
ARQUITETURA MODULAR - E-commerce Organizado em Módulos
=======================================================
Mesma aplicação monolítica, mas com separação clara de responsabilidades:
- Cada módulo tem Models, Services e Routes próprios
- Baixo acoplamento entre módulos
- Alta coesão dentro de cada módulo
- Ainda é um monolito (deploy único, BD único)
"""

from flask import Flask, jsonify
from config import config
from shared import init_db

# Importar blueprints dos módulos
from modules.auth import auth_bp
from modules.products import products_bp
from modules.orders import orders_bp
from modules.payment import payment_bp


def create_app(config_name='development'):
    """Factory para criar a aplicação"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Inicializar banco de dados
    init_db(app)
    
    # Registrar blueprints (módulos)
    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(payment_bp)
    
    # Rota principal
    @app.route('/')
    def home():
        return jsonify({
            'message': 'E-commerce Modular - FIAP Demo',
            'architecture': 'Modular Monolith',
            'description': 'Monolito organizado em módulos independentes',
            'modules': {
                'auth': {
                    'description': 'Autenticação e usuários',
                    'endpoints': '/api/auth/*'
                },
                'products': {
                    'description': 'Gerenciamento de produtos',
                    'endpoints': '/api/products/*'
                },
                'orders': {
                    'description': 'Gerenciamento de pedidos',
                    'endpoints': '/api/orders/*'
                },
                'payment': {
                    'description': 'Processamento de pagamentos',
                    'endpoints': '/api/payment/*'
                }
            },
            'benefits': [
                'Código organizado e fácil de navegar',
                'Separação clara de responsabilidades',
                'Baixo acoplamento entre módulos',
                'Alta coesão dentro dos módulos',
                'Base para migração futura'
            ]
        })
    
    @app.route('/health')
    def health():
        return jsonify({'status': 'healthy', 'architecture': 'modular'})
    
    return app


def seed_database(app):
    """Popula o banco com dados de exemplo"""
    with app.app_context():
        from modules.products.services import ProductService
        from modules.products.models import Product
        
        # Verificar se já existem produtos
        if Product.query.count() == 0:
            products = [
                {
                    'name': 'Notebook Dell',
                    'description': 'Core i7, 16GB RAM, 512GB SSD',
                    'price': 3500.00,
                    'stock': 10
                },
                {
                    'name': 'Mouse Logitech MX Master',
                    'description': 'Mouse sem fio ergonômico',
                    'price': 450.00,
                    'stock': 50
                },
                {
                    'name': 'Teclado Mecânico Keychron',
                    'description': 'RGB, switches blue, wireless',
                    'price': 650.00,
                    'stock': 30
                },
                {
                    'name': 'Monitor LG UltraWide 29"',
                    'description': 'Full HD, 75Hz, IPS',
                    'price': 1400.00,
                    'stock': 15
                },
                {
                    'name': 'Webcam Logitech C920',
                    'description': '1080p, microfone integrado',
                    'price': 450.00,
                    'stock': 25
                },
                {
                    'name': 'Headset HyperX Cloud',
                    'description': '7.1 surround, microfone removível',
                    'price': 350.00,
                    'stock': 40
                }
            ]
            
            for product_data in products:
                ProductService.create_product(**product_data)
            
            print("✅ Banco de dados populado com produtos de exemplo")


if __name__ == '__main__':
    app = create_app('development')
    seed_database(app)
    
    print("\n" + "="*60)
    print("🏗️  ARQUITETURA MODULAR - E-commerce")
    print("="*60)
    print("📦 Módulos independentes:")
    print("   • Auth     - Autenticação e usuários")
    print("   • Products - Gerenciamento de produtos")
    print("   • Orders   - Gerenciamento de pedidos")
    print("   • Payment  - Processamento de pagamentos")
    print()
    print("✨ Características:")
    print("   • Baixo acoplamento entre módulos")
    print("   • Alta coesão dentro dos módulos")
    print("   • Código organizado e manutenível")
    print("   • Ainda é um monolito (deploy único)")
    print()
    print("🚀 Servidor: http://localhost:5001")
    print("="*60 + "\n")
    
    app.run(debug=True, port=5001)
