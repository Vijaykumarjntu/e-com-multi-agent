from typing import Dict, Any
import random

class MarketingAgent:
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        customer_id = state['customer_id']
        
        # Simple campaign suggestion
        if state['total_amount'] > 300:
            campaign_id = f"CAMP_{random.randint(1000,9999)}"
            state['marketing_campaign_id'] = campaign_id
        else:
            state['marketing_campaign_id'] = None
            
        return state