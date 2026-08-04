from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# Instancia o banco de dados
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configuração da string de conexão com o PostgreSQL
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicia o banco de dados com o app
    db.init_app(app)

    from app.routes.cidadao import cidadao_bp
    app.register_blueprint(cidadao_bp, url_prefix='/api/cidadao')

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    from app.routes.corporativo import corporativo_bp
    app.register_blueprint(corporativo_bp, url_prefix='/api/corporativo')
    
    return app