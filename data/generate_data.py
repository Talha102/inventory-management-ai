import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

np.random.seed(42)
random.seed(42)

suppliers_data = {
    'supplier_id': ['S001', 'S002', 'S003', 'S004', 'S005'],
    'supplier_name': ['Ali Farms Lahore', 'Khan Fresh Store', 'Brew Masters Co', 'City Bakery Supply', 'Fresh Valley Pk'],
    'contact_person': ['Ali Hassan', 'Khan Sahab', 'Bilal Ahmed', 'Fatima Khan', 'Usman Ali'],
    'phone': ['0300-1234567', '0321-7654321', '0333-1122334', '0345-9988776', '0311-5544332'],
    'email': ['ali@farms.pk', 'khan@fresh.pk', 'bilal@brew.pk', 'fatima@bakery.pk', 'usman@valley.pk'],
    'city': ['Lahore', 'Karachi', 'Islamabad', 'Lahore', 'Faisalabad'],
    'lead_time_days': [1, 2, 3, 1, 2],
    'reliability_score': [4.8, 4.5, 4.2, 4.9, 4.3]
}

inventory_data = {
    'item_id': ['I001','I002','I003','I004','I005','I006','I007','I008','I009','I010','I011','I012','I013','I014','I015'],
    'item_name': ['Mango','Orange','Lemon','Watermelon','Coffee Beans','Milk','Sugar','Green Tea','Croissant','Sandwich Bread','Cups','Straws','Napkins','Ice','Mint'],
    'category': ['Juice','Juice','Juice','Juice','Coffee','Coffee','Coffee','Tea','Bakery','Bakery','Supplies','Supplies','Supplies','Supplies','Tea'],
    'current_stock': [5, 45, 8, 30, 3, 20, 15, 10, 50, 40, 200, 500, 300, 25, 12],
    'min_stock': [10, 20, 10, 15, 5, 15, 10, 8, 30, 20, 100, 200, 150, 20, 8],
    'max_stock': [50, 80, 40, 60, 20, 50, 40, 30, 100, 80, 500, 1000, 600, 80, 30],
    'unit': ['kg','kg','kg','kg','kg','liter','kg','kg','pcs','pcs','pcs','pcs','pcs','kg','kg'],
    'unit_price': [500, 200, 150, 100, 2500, 180, 120, 800, 150, 80, 5, 2, 3, 50, 300],
    'cost_price': [350, 140, 100, 70, 1800, 130, 90, 600, 100, 55, 3, 1, 2, 35, 200],
    'supplier_id': ['S001','S001','S001','S005','S003','S002','S002','S003','S004','S004','S002','S002','S004','S005','S001'],
    'last_restocked': ['2026-06-01','2026-06-05','2026-06-03','2026-06-04','2026-06-02','2026-06-06','2026-06-05','2026-06-03','2026-06-07','2026-06-06','2026-06-01','2026-06-01','2026-06-02','2026-06-05','2026-06-04'],
    'expiry_days': [3, 5, 7, 4, 180, 2, 365, 365, 2, 3, 730, 730, 730, 1, 7]
}

items = inventory_data['item_name']
price_map = dict(zip(inventory_data['item_name'], inventory_data['unit_price']))
start_date = datetime(2026, 1, 1)
sales_records = []

for day in range(180):
    current_date = start_date + timedelta(days=day)
    is_weekend = current_date.weekday() >= 5
    for item in items:
        base_sales = random.randint(2, 15)
        if is_weekend:
            base_sales = int(base_sales * 1.4)
        if item in ['Mango', 'Watermelon', 'Ice']:
            if current_date.month in [5, 6, 7]:
                base_sales = int(base_sales * 1.6)
        revenue = base_sales * price_map[item]
        sales_records.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'item_name': item,
            'quantity_sold': base_sales,
            'revenue': revenue
        })

os.makedirs('data', exist_ok=True)
pd.DataFrame(suppliers_data).to_csv('data/suppliers.csv', index=False)
pd.DataFrame(inventory_data).to_csv('data/inventory.csv', index=False)
pd.DataFrame(sales_records).to_csv('data/sales_history.csv', index=False)

print("Suppliers data saved!")
print("Inventory data saved!")
print("Sales history saved!")
print(f"Total sales records: {len(sales_records)}")