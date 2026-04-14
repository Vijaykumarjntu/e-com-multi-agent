from typing import Dict, Any

class SupportRefundAgent:
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        amount = state['total_amount']
        
        # Auto-refund for small amounts
        if amount < 50:
            state['refund_eligible'] = True
            state['human_approval_needed'] = False
        elif amount > 200:
            state['refund_eligible'] = True
            state['human_approval_needed'] = True
        else:
            state['refund_eligible'] = False
            
        return state