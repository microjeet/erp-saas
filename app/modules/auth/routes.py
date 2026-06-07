from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json or {}
    tenant_id = data.get('tenant_id', 1)
    
    # Injetando a identidade do Tenant de forma irreversível no Token
    access_token = create_access_token(
        identity='operador_admin', 
        additional_claims={'tenant_id': tenant_id}
    )
    return jsonify(access_token=access_token)
