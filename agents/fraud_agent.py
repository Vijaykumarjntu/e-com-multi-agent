import pandas as pd
from typing import Dict, Any
import random

class PaymentsFraudAgent:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        customer_id = state['customer_id']
        amount = state['total_amount']
        
        # Simple fraud detection
        risk = 0.1
        if amount > 500:
            risk += 0.3
        if customer_id not in self.data['CustomerID'].values:
            risk += 0.2
            
        state['fraud_risk_score'] = min(risk, 1.0)
        state['human_approval_needed'] = risk > 0.7
        
        return state