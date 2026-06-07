from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app.extensions import db
from app.modules.inventory.models import Product

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/product', methods=['POST'])
@jwt_required()
def create_product():
    tenant_id = get_jwt().get('tenant_id')
    data = request.json
    
    new_product = Product(
        tenant_id=tenant_id,
        name=data.get('name'),
        sku=data.get('sku'),
        price=data.get('price'),
        stock_quantity=data.get('stock_quantity', 0)
    )
    
    db.session.add(new_product)
    db.session.commit()
    
    return jsonify({
        'message': 'Product created successfully',
        'product': {
            'id': new_product.id,
            'name': new_product.name,
            'sku': new_product.sku,
            'price': str(new_product.price),
            'stock': new_product.stock_quantity
        }
    }), 201

@inventory_bp.route('/products', methods=['GET'])
@jwt_required()
def list_products():
    tenant_id = get_jwt().get('tenant_id')
    products = Product.query.filter_by(tenant_id=tenant_id).all()
    
    result = [{
        'id': p.id,
        'name': p.name,
        'sku': p.sku,
        'price': str(p.price),
        'stock': p.stock_quantity
    } for p in products]
    
    return jsonify(result), 200
