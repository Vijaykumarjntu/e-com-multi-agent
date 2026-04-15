import pandas as pd
from typing import Dict, Any
import random
from models.fraud_model import FraudDetectionModel

class PaymentsFraudAgent:
    def __init__(self, data, fraud_threshold=0.7):
        self.data = data
        self.fraud_threshold = fraud_threshold
        self.model = FraudDetectionModel()

        # Train or load model
        try:
            self.model.model = joblib.load('fraud_model.pkl')
        except:
            self.model.train()
        
    def process(self, state):
        customer_id = state['customer_id']
        amount = state['total_amount']
        quantity = sum(item['Quantity'] for item in state['items'])
        
        # Use ML for fraud detection
        fraud_prob = self.model.predict(customer_id, amount, quantity)
        
        state['fraud_risk_score'] = fraud_prob
        
        
        if fraud_prob > self.fraud_threshold:
            state['human_approval_needed'] = True
            state['approval_reason'] = f"ML fraud probability: {fraud_prob:.2f}"
        else:
            state['human_approval_needed'] = False
            
        return state