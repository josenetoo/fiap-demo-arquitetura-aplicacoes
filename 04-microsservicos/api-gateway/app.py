"""
API Gateway - Microsserviços
============================
Ponto de entrada único que roteia requisições para os microsserviços
"""

from flask import Flask, jsonify, request
import requests
from functools import wraps

app = Flask(__name__)

# URLs dos microsserviços
SERVICES = {
    'auth': 'http://auth-service:6001',
    'products': 'http://product-service:6002',
    'orders': 'http://order-service:6003',
    'payments': 'http://payment-service:6004'
}


# ============================================
# MIDDLEWARE E UTILIDADES
# ============================================

def require_auth(f):
    """Middleware de autenticação"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token não fornecido'}), 401
        
        # Validar token com auth-service
        try:
            response = requests.post(
                f"{SERVICES['auth']}/api/validate",
                json={'token': token},
                timeout=5
            )
            
            if response.status_code != 200:
                return jsonify({'error': 'Token inválido'}), 401
                
        except requests.exceptions.RequestException:
            return jsonify({'error': 'Auth service indisponível'}), 503
        
        return f(*args, **kwargs)
    
    return decorated_function


def proxy_request(service, path, method='GET', **kwargs):
    """Proxy de requisição para um microsserviço"""
    url = f"{SERVICES[service]}{path}"
    
    try:
        if method == 'GET':
            response = requests.get(url, timeout=10, **kwargs)
        elif method == 'POST':
            response = requests.post(url, timeout=10, **kwargs)
        elif method == 'PUT':
            response = requests.put(url, timeout=10, **kwargs)
        elif method == 'DELETE':
            response = requests.delete(url, timeout=10, **kwargs)
        
        return response.json(), response.status_code
        
    except requests.exceptions.Timeout:
        return {'error': f'{service} service timeout'}, 504
    except requests.exceptions.RequestException as e:
        return {'error': f'{service} service indisponível'}, 503


# ============================================
# ROTAS DO GATEWAY
# ============================================

@app.route('/')
def home():
    return jsonify({
        'message': 'API Gateway - Arquitetura de Microsserviços',
        'architecture': 'Microservices',
        'description': 'Gateway que roteia para microsserviços independentes',
        'services': {
            'auth-service': {
                'url': SERVICES['auth'],
                'description': 'Autenticação e usuários',
                'database': 'auth.db (próprio)'
            },
            'product-service': {
                'url': SERVICES['products'],
                'description': 'Gerenciamento de produtos',
                'database': 'products.db (próprio)'
            },
            'order-service': {
                'url': SERVICES['orders'],
                'description': 'Gerenciamento de pedidos',
                'database': 'orders.db (próprio)'
            },
            'payment-service': {
                'url': SERVICES['payments'],
                'description': 'Processamento de pagamentos',
                'database': 'stateless'
            }
        },
        'features': [
            'Serviços independentes',
            'Banco de dados por serviço',
            'Deploy independente',
            'Escalabilidade granular',
            'Comunicação via HTTP/REST'
        ]
    })


@app.route('/health')
def health():
    """Health check de todos os serviços"""
    health_status = {}
    
    for service_name, service_url in SERVICES.items():
        try:
            response = requests.get(f"{service_url}/health", timeout=3)
            health_status[service_name] = {
                'status': 'healthy' if response.status_code == 200 else 'unhealthy',
                'response_time': response.elapsed.total_seconds()
            }
        except requests.exceptions.RequestException:
            health_status[service_name] = {
                'status': 'down',
                'response_time': None
            }
    
    all_healthy = all(s['status'] == 'healthy' for s in health_status.values())
    
    return jsonify({
        'gateway': 'healthy',
        'services': health_status,
        'overall': 'healthy' if all_healthy else 'degraded'
    }), 200 if all_healthy else 503


# === ROTAS DE AUTENTICAÇÃO ===

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Proxy para auth-service"""
    return proxy_request('auth', '/api/register', 'POST', json=request.json)


@app.route('/api/auth/login', methods=['POST'])
def login():
    """Proxy para auth-service"""
    return proxy_request('auth', '/api/login', 'POST', json=request.json)


@app.route('/api/users/<int:user_id>')
def get_user(user_id):
    """Proxy para auth-service"""
    return proxy_request('auth', f'/api/users/{user_id}')


# === ROTAS DE PRODUTOS ===

@app.route('/api/products')
def list_products():
    """Proxy para product-service"""
    return proxy_request('products', '/api/products')


@app.route('/api/products/<int:product_id>')
def get_product(product_id):
    """Proxy para product-service"""
    return proxy_request('products', f'/api/products/{product_id}')


@app.route('/api/products', methods=['POST'])
@require_auth
def create_product():
    """Proxy para product-service (requer autenticação)"""
    return proxy_request('products', '/api/products', 'POST', json=request.json)


# === ROTAS DE PEDIDOS ===

@app.route('/api/orders', methods=['POST'])
@require_auth
def create_order():
    """Proxy para order-service (requer autenticação)"""
    return proxy_request('orders', '/api/orders', 'POST', json=request.json)


@app.route('/api/orders/<int:order_id>')
@require_auth
def get_order(order_id):
    """Proxy para order-service"""
    return proxy_request('orders', f'/api/orders/{order_id}')


@app.route('/api/orders/user/<int:user_id>')
@require_auth
def get_user_orders(user_id):
    """Proxy para order-service"""
    return proxy_request('orders', f'/api/orders/user/{user_id}')


# === ROTAS DE PAGAMENTO ===

@app.route('/api/payments/methods')
def get_payment_methods():
    """Proxy para payment-service"""
    return proxy_request('payments', '/api/payments/methods')


@app.route('/api/payments/process', methods=['POST'])
@require_auth
def process_payment():
    """Proxy para payment-service"""
    return proxy_request('payments', '/api/payments/process', 'POST', json=request.json)


# ============================================
# INICIALIZAÇÃO
# ============================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🌐 API GATEWAY - Arquitetura de Microsserviços")
    print("="*60)
    print("Ponto de entrada único para todos os microsserviços")
    print()
    print("Serviços registrados:")
    for name, url in SERVICES.items():
        print(f"  • {name:15} -> {url}")
    print()
    print("🚀 Gateway: http://localhost:9000")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=9000, debug=True)
