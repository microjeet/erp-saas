from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app.modules.finance.models import Transaction
from app.modules.inventory.models import Product
from sqlalchemy import func

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard():
    tenant_id = get_jwt().get('tenant_id')
    
    # Agregando valor total de vendas
    total_sales = db.session.query(func.sum(Transaction.gross_amount)).filter_by(tenant_id=tenant_id).scalar() or 0
    
    # Contagem de produtos e valor total em estoque
    total_products = Product.query.filter_by(tenant_id=tenant_id).count()
    inventory_value = db.session.query(func.sum(Product.price * Product.stock_quantity)).filter_by(tenant_id=tenant_id).scalar() or 0
    
    return jsonify({
        'tenant_id': tenant_id,
        'resumo_financeiro': {'total_vendas': float(total_sales)},
        'resumo_estoque': {
            'total_produtos_cadastrados': total_products,
            'valor_total_estoque': float(inventory_value)
        }
    })
