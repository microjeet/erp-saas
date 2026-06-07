from app.extensions import db
from datetime import datetime, timezone

class Tenant(db.Model):
    __tablename__ = 'tenants'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    document = db.Column(db.String(20), unique=True, nullable=False) # CNPJ
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relações (Cascade: se o tenant for deletado, apaga tudo dele)
    transactions = db.relationship('Transaction', backref='tenant', lazy=True, cascade='all, delete-orphan')
