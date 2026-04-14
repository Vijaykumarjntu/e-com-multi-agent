import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from agents.fraud_agent import PaymentsFraudAgent
from agents.inventory_agent import InventoryForecaster
from agents.support_agent import SupportRefundAgent
from agents.marketing_agent import MarketingAgent
from orchestration.graph import ECommerceOrchestrator

# Load data
df = pd.read_csv('online_retail.csv', encoding='latin1')

# Create order that WILL trigger human approval (high amount = high fraud risk)
test_order_high_risk = {
    'order_id': 'HIGH_RISK_001',
    'customer_id': 99999,  # Non-existent customer = high risk
    'items': [{'StockCode': 'TEST', 'quantity': 1, 'unit_price': 600}],
    'total_amount': 600,  # >500 adds more risk
    'country': 'Unknown',
    'human_approval_needed': False
}

# Create order that WON'T trigger human approval
test_order_low_risk = {
    'order_id': 'LOW_RISK_001',
    'customer_id': 17850,  # Real customer from your data
    'items': [{'StockCode': 'TEST', 'quantity': 1, 'unit_price': 20}],
    'total_amount': 20,
    'country': 'UK',
    'human_approval_needed': False
}

# Initialize agents
inventory_agent = InventoryForecaster(df)
fraud_agent = PaymentsFraudAgent(df, fraud_threshold=0.7)
# support_agent = SupportRefundAgent(100)
support_agent = SupportRefundAgent()
marketing_agent = MarketingAgent()

orchestrator = ECommerceOrchestrator(
    inventory_agent, fraud_agent, support_agent, marketing_agent
)

print("="*60)
print("TEST 1: HIGH RISK ORDER (Should trigger human approval)")
print("="*60)
result1 = orchestrator.process_order(test_order_high_risk)
print(f"\nFinal Status: {result1.get('human_decision', 'No approval needed')}")

print("\n" + "="*60)
print("TEST 2: LOW RISK ORDER (Should auto-approve)")
print("="*60)
result2 = orchestrator.process_order(test_order_low_risk)
print(f"\nFinal Status: {result2.get('human_decision', 'Auto-approved')}")