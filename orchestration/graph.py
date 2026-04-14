from langgraph.graph import StateGraph, END
from typing import Dict, Any

class ECommerceOrchestrator:
    def __init__(self, inventory_agent, fraud_agent, support_agent, marketing_agent):
        self.inventory = inventory_agent
        self.fraud = fraud_agent
        self.support = support_agent
        self.marketing = marketing_agent
        self.graph = self._build_graph()
        
    def _build_graph(self):
        workflow = StateGraph(dict)
        
        workflow.add_node("inventory", self.inventory.process)
        workflow.add_node("fraud", self.fraud.process)
        workflow.add_node("support", self.support.process)
        workflow.add_node("marketing", self.marketing.process)
        workflow.add_node("human_approval", self._human_approval)
        
        workflow.set_entry_point("inventory")
        workflow.add_edge("inventory", "fraud")
        workflow.add_edge("fraud", "support")
        workflow.add_edge("support", "marketing")
        
        def check_approval(state):
            if state.get('human_approval_needed', False):
                return "human_approval"
            return END
            
        workflow.add_conditional_edges("marketing", check_approval)
        workflow.add_edge("human_approval", END)
        
        return workflow.compile()
    
    def _human_approval(self, state):
        print(f"\n🔴 HUMAN APPROVAL REQUIRED")
        print(f"Order: {state['order_id']}")
        print(f"Amount: ${state['total_amount']}")
        print(f"Fraud Risk: {state.get('fraud_risk_score', 0)}")
        print(f"Reason: {state.get('approval_reason', 'High fraud risk')}")
        
        decision = input("Approve order? (yes/no): ").lower()
        
        if decision == 'yes':
            state['human_decision'] = 'APPROVED'
            print("✅ Order approved")
        else:
            state['human_decision'] = 'REJECTED'
            print("❌ Order rejected")
            
        return state
    
    def process_order(self, order):
        return self.graph.invoke(order)