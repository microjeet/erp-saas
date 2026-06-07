from decimal import Decimal, ROUND_HALF_UP

class TaxEngine:
    @staticmethod
    def process_transaction(gross_amount_str: str, tax_rates: dict) -> dict:
        """
        Processa uma transação aplicando múltiplas taxas de impostos.
        Usa strings para instanciar o Decimal, garantindo precisão absoluta.
        """
        gross = Decimal(gross_amount_str)
        total_tax = Decimal('0.0000')
        details = []
        
        for name, rate_str in tax_rates.items():
            rate = Decimal(rate_str)
            # Arredondamento contábil bancário na 4ª casa decimal
            tax_value = (gross * rate).quantize(Decimal('0.0000'), rounding=ROUND_HALF_UP)
            total_tax += tax_value
            details.append({
                'tax_name': name,
                'rate': str(rate),
                'amount': str(tax_value)
            })
            
        net_amount = gross - total_tax
        
        return {
            'gross_amount': str(gross),
            'net_amount': str(net_amount),
            'total_taxes': str(total_tax),
            'details': details
        }
