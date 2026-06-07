import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'chave_fallback')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Segurança do JWT para o Multi-tenant
    JWT_SECRET_KEY = os.environ.get('SECRET_KEY', 'jwt_fallback')
