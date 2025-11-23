"""
Módulo de Autenticação - Routes
Responsabilidade: Endpoints HTTP de autenticação
"""
from flask import Blueprint, request, jsonify
from .services import AuthService

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    """Endpoint de registro de usuário"""
    data = request.json
    
    # Validar dados
    if not all(k in data for k in ['username', 'email', 'password']):
        return jsonify({'error': 'Dados incompletos'}), 400
    
    user, error = AuthService.register_user(
        data['username'],
        data['email'],
        data['password']
    )
    
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify(user.to_dict()), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """Endpoint de login"""
    data = request.json
    
    # Validar dados
    if not all(k in data for k in ['username', 'password']):
        return jsonify({'error': 'Dados incompletos'}), 400
    
    user = AuthService.authenticate(data['username'], data['password'])
    
    if not user:
        return jsonify({'error': 'Credenciais inválidas'}), 401
    
    return jsonify({
        **user.to_dict(),
        'token': f'token-{user.id}'  # Simplificado para demo
    })


@auth_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Endpoint para buscar usuário"""
    user = AuthService.get_user_by_id(user_id)
    
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    return jsonify(user.to_dict())
