"""
Auth Service - Serviço de Autenticação (SOA)
============================================
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
users_db = {
    1: {'id': 1, 'username': 'joao', 'email': 'joao@fiap.com.br'},
    2: {'id': 2, 'username': 'maria', 'email': 'maria@fiap.com.br'},
    3: {'id': 3, 'username': 'pedro', 'email': 'pedro@fiap.com.br'}
}


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'service': 'auth-service', 'status': 'healthy'})


@app.route('/validate', methods=['POST'])
def validate_user():
    """Valida se usuário existe"""
    data = request.json
    user_id = data.get('user_id')
    
    if user_id in users_db:
        return jsonify({
            'valid': True,
            'user': users_db[user_id]
        })
    
    return jsonify({'valid': False, 'error': 'Usuário não encontrado'}), 404


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Busca usuário por ID"""
    if user_id in users_db:
        return jsonify(users_db[user_id])
    
    return jsonify({'error': 'Usuário não encontrado'}), 404


if __name__ == '__main__':
    # Registrar serviço no ESB
    esb.register_service('auth-service', 'http://localhost:5010')
    
    print("\n🔐 Auth Service (SOA)")
    print("Porta: 5010")
    print("Registrado no ESB")
    
    app.run(port=5010, debug=True)
