import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class InventoryForecastModel:
    def __init__(self, data_path='online_retail.csv'):
        self.data = pd.read_csv(data_path, encoding='latin1')
        self.data['InvoiceDate'] = pd.to_datetime(self.data['InvoiceDate'])
        
    def forecast_stock(self, stock_code, days_ahead=7):
        # Get historical sales for this product
        product_sales = self.data[self.data['StockCode'] == stock_code]
        
        if len(product_sales) == 0:
            return {'stock_code': stock_code, 'forecast': 0, 'confidence': 'low'}
        
        # Calculate daily average sales
        daily_avg = product_sales.groupby(product_sales['InvoiceDate'].dt.date)['Quantity'].sum().mean()
        
        # Forecast next N days
        forecast = daily_avg * days_ahead
        
        # Current stock (mock - in real system from database)
        current_stock = np.random.randint(0, 100)
        
        return {
            'stock_code': stock_code,
            'current_stock': current_stock,
            'forecast_7d': round(forecast, 0),
            'will_stockout': forecast > current_stock,
            'reorder_needed': current_stock < 20
        }