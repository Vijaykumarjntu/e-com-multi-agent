import pandas as pd
from typing import Dict, Any

class InventoryForecaster:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        items = state['items']
        stock_status = {}
        
        for item in items:
            stock_code = item['StockCode']
            # Check historical sales
            sales = self.data[self.data['StockCode'] == stock_code]['Quantity'].sum()
            stock_status[stock_code] = max(0, 100 - sales)  # Mock stock level
            
        state['inventory_status'] = stock_status
        return state