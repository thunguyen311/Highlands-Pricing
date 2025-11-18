"""
Sample data for Highlands Coffee pricing analysis
"""
import pandas as pd
import numpy as np

def get_product_data():
    """Return sample product pricing data for Highlands Coffee"""
    products = {
        'Product': [
            'Phin Cà Phê Sữa Đá', 'Phin Cà Phê Đen Đá', 'Bạc Xỉu',
            'Freeze Trà Xanh', 'Freeze Socola', 'Freeze Caramel',
            'Trà Sen Vàng', 'Trà Thạch Đào', 'Hồng Trà Macchiato',
            'Bánh Mì Thịt', 'Bánh Mì Chay', 'Bánh Croissant',
            'Bánh Mousse', 'Cookies', 'Muffin'
        ],
        'Category': [
            'Coffee', 'Coffee', 'Coffee',
            'Freeze', 'Freeze', 'Freeze',
            'Tea', 'Tea', 'Tea',
            'Food', 'Food', 'Food',
            'Dessert', 'Dessert', 'Dessert'
        ],
        'Size': [
            'M', 'M', 'M',
            'M', 'M', 'M',
            'M', 'M', 'M',
            'Regular', 'Regular', 'Regular',
            'Regular', 'Regular', 'Regular'
        ],
        'Price (VND)': [
            45000, 39000, 45000,
            59000, 59000, 59000,
            49000, 49000, 55000,
            35000, 32000, 29000,
            42000, 25000, 28000
        ],
        'Cost (VND)': [
            20000, 18000, 20000,
            25000, 26000, 25000,
            22000, 23000, 25000,
            18000, 16000, 15000,
            20000, 12000, 14000
        ]
    }
    
    df = pd.DataFrame(products)
    df['Profit (VND)'] = df['Price (VND)'] - df['Cost (VND)']
    df['Margin (%)'] = (df['Profit (VND)'] / df['Price (VND)'] * 100).round(2)
    
    return df

def get_sales_data():
    """Return sample sales data by product"""
    np.random.seed(42)
    
    products = [
        'Phin Cà Phê Sữa Đá', 'Phin Cà Phê Đen Đá', 'Bạc Xỉu',
        'Freeze Trà Xanh', 'Freeze Socola', 'Freeze Caramel',
        'Trà Sen Vàng', 'Trà Thạch Đào', 'Hồng Trà Macchiato',
        'Bánh Mì Thịt', 'Bánh Mì Chay', 'Bánh Croissant',
        'Bánh Mousse', 'Cookies', 'Muffin'
    ]
    
    # Generate 30 days of sales data
    dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
    
    data = []
    for date in dates:
        for product in products:
            # Random daily sales with some variation
            if 'Coffee' in product or 'Bạc Xỉu' in product:
                base_qty = np.random.randint(50, 120)
            elif 'Freeze' in product:
                base_qty = np.random.randint(30, 80)
            elif 'Trà' in product or 'Tea' in product:
                base_qty = np.random.randint(25, 70)
            else:
                base_qty = np.random.randint(15, 50)
            
            data.append({
                'Date': date,
                'Product': product,
                'Quantity': base_qty
            })
    
    return pd.DataFrame(data)

def get_store_comparison_data():
    """Return sample data for store comparison"""
    stores = ['Nguyễn Huệ', 'Lê Lợi', 'Hai Bà Trưng', 'Đồng Khởi', 'Pasteur']
    
    data = []
    for store in stores:
        data.append({
            'Store': store,
            'Daily Revenue (VND)': np.random.randint(15000000, 35000000),
            'Daily Customers': np.random.randint(300, 700),
            'Avg Transaction (VND)': np.random.randint(50000, 80000),
            'Staff': np.random.randint(5, 12)
        })
    
    return pd.DataFrame(data)
