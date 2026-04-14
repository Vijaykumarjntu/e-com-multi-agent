import pandas as pd
from dotenv import load_dotenv
import os

from agents.inventory_agent import InventoryForecaster
from agents.fraud_agent import PaymentsFraudAgent
from agents.support_agent import SupportRefundAgent
from agents.marketing_agent import MarketingAgent
from orchestration.graph import ECommerceOrchestrator

load_dotenv()

def main():
    # Load your CSV data
    # data_path = os.getenv('DATA_PATH', './data/online_retail.csv')
    # df = pd.read_csv('./data/online_retail.csv')
    # df = pd.read_csv('online_retail.csv', encoding='latin1')
    # Try different encodings
    encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
    df = None
    
    for encoding in encodings:
        try:
            df = pd.read_csv('./online_retail.csv', encoding='latin1')
            print(f"✅ Successfully loaded with {encoding} encoding")
            print(df[:10])
            break
        except UnicodeDecodeError:
            continue
    print(f"✅ Loaded {len(df)} transactions")
    print(f"✅ Unique customers: {df['CustomerID'].nunique()}")
    
    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
    # Initialize agents
    inventory_agent = InventoryForecaster(df)
    fraud_agent = PaymentsFraudAgent(df)
    support_agent = SupportRefundAgent()
    marketing_agent = MarketingAgent()
    
    # Create orchestrator
    orchestrator = ECommerceOrchestrator(
        inventory_agent, fraud_agent, support_agent, marketing_agent
    )
    
    # Test order (using real customer from your data)
    sample_customer = df[df['CustomerID'].notna()]['CustomerID'].iloc[0]
    sample_items = df[df['CustomerID'] == sample_customer].head(2)[['StockCode', 'Quantity', 'UnitPrice']].to_dict('records')
    
    test_order = {
        'order_id': 'TEST_001',
        'customer_id': int(sample_customer),
        'items': sample_items,
        'total_amount': sum(i['Quantity'] * i['UnitPrice'] for i in sample_items),
        'country': 'UK',
        'human_approval_needed': False
    }
    
    print("\n" + "="*50)
    print("Processing Test Order...")
    print("="*50)
    
    result = orchestrator.process_order(test_order)
    
    print("\n" + "="*50)
    print("FINAL RESULT:")
    print(f"Order ID: {result['order_id']}")
    print(f"Fraud Risk: {result.get('fraud_risk_score', 'N/A')}")
    print(f"Human Approved: {result.get('human_decision', 'Auto-approved')}")
    print(f"Marketing Campaign: {result.get('marketing_campaign_id', 'None')}")

if __name__ == "__main__":
    main()