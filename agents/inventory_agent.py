import pandas as pd
from typing import Dict, Any

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.inventory_model import InventoryForecastModel

class InventoryForecaster:
    def __init__(self, data):
        self.data = data
        self.forecast_model = InventoryForecastModel()
        
    def process(self, state):
        items = state['items']
        alerts = []
        
        for item in items:
            StockCode = item['StockCode']
            forecast = self.forecast_model.forecast_stock(StockCode)
            
            if forecast['reorder_needed']:
                alerts.append(f"⚠️ {StockCode}: Only {forecast['current_stock']} left, reorder needed")
            elif forecast['will_stockout']:
                alerts.append(f"📦 {StockCode}: Will sell out in 7 days")
        
        if alerts:
            print("\n🔮 INVENTORY ALERTS:")
            for alert in alerts:
                print(f"  {alert}")
        
        state['inventory_alerts'] = alerts
        return state