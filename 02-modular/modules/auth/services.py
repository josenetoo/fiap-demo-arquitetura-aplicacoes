"""
Módulo de Autenticação - Services
Responsabilidade: Lógica de negócio de autenticação
"""
from .models import User
from shared.database import db


class AuthService:
    """Serviço de autenticação"""
    
    @staticmethod
    def register_user(username, email, password):
        """
        Registra um novo usuário
        
        Returns:
            tuple: (User, error_message)
        """
        # Validar se usuário já existe
        if User.query.filter_by(username=username).first():
            return None, "Usuário já existe"
        
        if User.query.filter_by(email=email).first():
            return None, "Email já cadastrado"
        
        # Criar novo usuário
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return user, None
    
    @staticmethod
    def authenticate(username, password):
        """
        Autentica um usuário
        
        Returns:
            User or None
        """
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            return user
        
        return None
    
    @staticmethod
    def get_user_by_id(user_id):
        """Busca usuário por ID"""
        return User.query.get(user_id)
    
    @staticmethod
    def get_user_by_username(username):
        """Busca usuário por username"""
        return User.query.filter_by(username=username).first()
