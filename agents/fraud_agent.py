import pandas as pd
from typing import Dict, Any
import random

class PaymentsFraudAgent:
    def __init__(self, data, fraud_threshold=0.7):
        self.data = data
        self.fraud_threshold = fraud_threshold
        
    def process(self, state):
        customer_id = state['customer_id']
        amount = state['total_amount']
        
        risk = 0.1
        if amount > 500:
            risk += 0.3
        if customer_id not in self.data['CustomerID'].values:
            risk += 0.2
            
        state['fraud_risk_score'] = min(risk, 1.0)
        
        if risk > self.fraud_threshold:
            state['human_approval_needed'] = True
            state['approval_reason'] = f"Fraud risk {risk:.2f} exceeds threshold"
        else:
            state['human_approval_needed'] = False
            
        return state