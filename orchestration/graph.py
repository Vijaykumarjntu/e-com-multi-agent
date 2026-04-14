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
        
        # Add nodes
        workflow.add_node("inventory", self.inventory.process)
        workflow.add_node("fraud", self.fraud.process)
        workflow.add_node("support", self.support.process)
        workflow.add_node("marketing", self.marketing.process)
        workflow.add_node("human", self._human_approval)
        
        # Add edges
        workflow.set_entry_point("inventory")
        workflow.add_edge("inventory", "fraud")
        workflow.add_edge("fraud", "support")
        workflow.add_edge("support", "marketing")
        
        # Conditional edge
        def needs_approval(state):
            if state.get('human_approval_needed', False):
                return "human"
            return END
            
        workflow.add_conditional_edges("marketing", needs_approval)
        workflow.add_edge("human", END)
        
        return workflow.compile()
    
    def _human_approval(self, state: Dict[str, Any]) -> Dict[str, Any]:
        print(f"\n⚠️ HUMAN APPROVAL NEEDED for Order {state['order_id']}")
        print(f"   Reason: Fraud risk {state['fraud_risk_score']:.2f}")
        decision = input("   Approve? (yes/no): ")
        state['human_decision'] = decision
        return state
    
    def process_order(self, order: Dict[str, Any]) -> Dict[str, Any]:
        return self.graph.invoke(order)