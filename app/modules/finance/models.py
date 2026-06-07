from app.extensions import db
from datetime import datetime, timezone

class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), nullable=False, index=True)
    type = db.Column(db.String(10), nullable=False) # 'revenue' (receita) ou 'expense' (despesa)
    gross_amount = db.Column(db.Numeric(15, 4), nullable=False) # Valor bruto exato
    net_amount = db.Column(db.Numeric(15, 4), nullable=False)   # Valor líquido após impostos
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    taxes = db.relationship('TaxDetail', backref='transaction', lazy=True, cascade='all, delete-orphan')

class TaxDetail(db.Model):
    __tablename__ = 'tax_details'
    
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'), nullable=False, index=True)
    tax_name = db.Column(db.String(50), nullable=False) # Ex: 'ICMS', 'ISS'
    rate_percentage = db.Column(db.Numeric(5, 4), nullable=False) # Ex: 0.1800 para 18%
    calculated_amount = db.Column(db.Numeric(15, 4), nullable=False) # Retenção exata
