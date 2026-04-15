import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

class FraudDetectionModel:
    def __init__(self, data_path='online_retail.csv'):
        self.data = pd.read_csv(data_path, encoding='latin1')
        self.model = None
        self.data['TotalPrice'] = self.data['Quantity'] * self.data['UnitPrice']
        
    def prepare_features(self):
        # Create features from real data
        customer_features = self.data.groupby('CustomerID').agg({
            'InvoiceNo': 'nunique',  # order frequency
            'TotalPrice': ['mean', 'sum'],  # spending patterns
            'Quantity': 'mean'  # avg order size
        }).fillna(0)
        
        customer_features.columns = ['order_count', 'avg_order_value', 'total_spent', 'avg_quantity']
        
        # Create synthetic labels (in real world, use actual fraud data)
        customer_features['is_fraud'] = (
            (customer_features['order_count'] == 1) & 
            (customer_features['total_spent'] > 1000)
        ).astype(int)
        
        return customer_features
    
    def train(self):
        features = self.prepare_features()
        X = features[['order_count', 'avg_order_value', 'total_spent', 'avg_quantity']]
        y = features['is_fraud']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        
        self.model = RandomForestClassifier(n_estimators=100)
        self.model.fit(X_train, y_train)
        
        accuracy = self.model.score(X_test, y_test)
        print(f"Model trained. Accuracy: {accuracy:.2f}")
        
        joblib.dump(self.model, 'fraud_model.pkl')
        return self.model
    
    def predict(self, customer_id, amount, quantity):
        if self.model is None:
            self.model = joblib.load('fraud_model.pkl')
        
        # Get customer features
        features = self.prepare_features()
        
        if customer_id in features.index:
            customer_data = features.loc[customer_id]
            order_count = customer_data['order_count']
            avg_order = customer_data['avg_order_value']
            total_spent = customer_data['total_spent']
            avg_qty = customer_data['avg_quantity']
        else:
            # New customer
            order_count, avg_order, total_spent, avg_qty = 0, 0, 0, 0
        
        X_pred = [[order_count, avg_order, total_spent, avg_qty]]
        fraud_prob = self.model.predict_proba(X_pred)[0][1]
        
        return fraud_prob