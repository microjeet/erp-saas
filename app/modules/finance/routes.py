from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app.extensions import db
from app.modules.finance.services import TaxEngine
from app.modules.inventory.models import Product

finance_bp = Blueprint('finance', __name__)

@finance_bp.route('/transaction', methods=['POST'])
@jwt_required()
def create_transaction():
    claims = get_jwt()
    tenant_id = claims.get('tenant_id')
    data = request.json
    
    # 1. Processamento Fiscal
    result = TaxEngine.process_transaction(str(data.get('gross_amount')), data.get('tax_rates', {}))
    
    # 2. Integração: Baixa de Estoque (se SKU for informado)
    sku = data.get('sku')
    qty = data.get('quantity', 1)
    if sku:
        product = Product.query.filter_by(tenant_id=tenant_id, sku=sku).first()
        if product and product.deduct_stock(qty):
            db.session.commit()
            result['stock_status'] = 'Baixa realizada'
        else:
            result['stock_status'] = 'Erro: Produto não encontrado ou saldo insuficiente'
    
    result['tenant_id'] = tenant_id
    return jsonify(result), 201