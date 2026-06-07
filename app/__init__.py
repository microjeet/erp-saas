from flask import Flask
from app.core.config import Config
from app.extensions import db, migrate, jwt

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicialização das extensões do Flask
    db.init_app(app)
    migrate.init_app(app, db)

    # Importação de Modelos (Garante que o ORM reconheça as tabelas para as Migrations)
    from app.modules.tenant.models import Tenant
    from app.modules.finance.models import Transaction, TaxDetail
    from app.modules.inventory.models import Product
    jwt.init_app(app)

    # Registro de Blueprints (Módulos do ERP)
    from app.modules.finance.routes import finance_bp
    from app.modules.auth.routes import auth_bp
    app.register_blueprint(finance_bp, url_prefix='/api/v1/finance')
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')

    # Rota de Health Check da Infraestrutura
    @app.route('/health')
    def health_check():
        return {'status': 'ok', 'system': 'SaaS ERP Core', 'state': 'online'}

    return app
