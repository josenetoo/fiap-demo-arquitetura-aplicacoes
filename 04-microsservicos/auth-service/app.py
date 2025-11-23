"""
Auth Microservice - Serviço de Autenticação
===========================================
Microsserviço independente com:
- Banco de dados próprio
- API REST
- Deploy independente
"""

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auth.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ============================================
# MODELO DE DADOS (Banco próprio do serviço)
# ============================================

class User(db.Model):
    """Modelo de usuário - BD exclusivo deste serviço"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }


# ============================================
# API REST DO MICROSSERVIÇO
# ============================================

@app.route('/health', methods=['GET'])
def health():
    """Health check do serviço"""
    return jsonify({
        'service': 'auth-service',
        'status': 'healthy',
        'database': 'connected'
    })


@app.route('/api/register', methods=['POST'])
def register():
    """Registra novo usuário"""
    data = request.json
    
    # Validar dados
    if not all(k in data for k in ['username', 'email', 'password']):
        return jsonify({'error': 'Dados incompletos'}), 400
    
    # Verificar se usuário já existe
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Usuário já existe'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email já cadastrado'}), 400
    
    # Criar usuário
    user = User(
        username=data['username'],
        email=data['email'],
        password_hash=generate_password_hash(data['password'])
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify(user.to_dict()), 201


@app.route('/api/login', methods=['POST'])
def login():
    """Autentica usuário"""
    data = request.json
    
    if not all(k in data for k in ['username', 'password']):
        return jsonify({'error': 'Dados incompletos'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': 'Credenciais inválidas'}), 401
    
    return jsonify({
        **user.to_dict(),
        'token': f'jwt-token-{user.id}'  # Simplificado
    })


@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Busca usuário por ID"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    return jsonify(user.to_dict())


@app.route('/api/users', methods=['GET'])
def list_users():
    """Lista todos os usuários"""
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])


@app.route('/api/validate', methods=['POST'])
def validate_token():
    """Valida token de autenticação (usado por outros serviços)"""
    data = request.json
    token = data.get('token')
    
    # Simplificado: extrair user_id do token
    if token and token.startswith('jwt-token-'):
        user_id = int(token.split('-')[-1])
        user = User.query.get(user_id)
        
        if user:
            return jsonify({
                'valid': True,
                'user': user.to_dict()
            })
    
    return jsonify({'valid': False}), 401


# ============================================
# INICIALIZAÇÃO
# ============================================

def init_db():
    """Inicializa banco de dados"""
    with app.app_context():
        db.create_all()
        
        # Criar usuários de exemplo
        if User.query.count() == 0:
            users = [
                User(username='joao', email='joao@fiap.com.br', 
                     password_hash=generate_password_hash('123456')),
                User(username='maria', email='maria@fiap.com.br',
                     password_hash=generate_password_hash('123456')),
                User(username='pedro', email='pedro@fiap.com.br',
                     password_hash=generate_password_hash('123456'))
            ]
            
            for user in users:
                db.session.add(user)
            
            db.session.commit()
            print("✅ Usuários de exemplo criados")


if __name__ == '__main__':
    init_db()
    
    print("\n" + "="*50)
    print("🔐 AUTH MICROSERVICE")
    print("="*50)
    print("Serviço independente de autenticação")
    print("Banco de dados: auth.db (próprio)")
    print("Porta: 6001")
    print("="*50 + "\n")
    
    app.run(host='0.0.0.0', port=6001, debug=True)
