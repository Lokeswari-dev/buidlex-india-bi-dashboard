import pandas as pd
import random
from datetime import datetime, timedelta

# Constants for generating dummy data
MATERIALS = {
    'Cement': {'Category': 'Binding', 'Price': (300, 450)},
    'TMT Steel': {'Category': 'Reinforcement', 'Price': (45000, 55000)},
    'Concrete': {'Category': 'Mixture', 'Price': (3500, 5000)},
    'Bricks': {'Category': 'Masonry', 'Price': (6, 12)},
    'Sand': {'Category': 'Aggregates', 'Price': (1500, 2500)}
}
LOCATIONS = ['Hyderabad', 'Bangalore', 'Mumbai', 'Pune', 'Vizag']
DELIVERY_STATUS = ['Delivered', 'In Transit', 'Pending', 'Cancelled']
PAYMENT_STATUS = ['Paid', 'Pending', 'Partial']

def generate_buildex_data(num_rows=1000):
    data = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365) # Last 1 year of data

    for i in range(num_rows):
        # Generate random date
        random_days = random.randint(0, 365)
        order_date = start_date + timedelta(days=random_days)
        
        customer_name = f"BuildCo_{random.randint(100, 999)}"
        
        material = random.choice(list(MATERIALS.keys()))
        category = MATERIALS[material]['Category']
        
        # Adjust quantity logic based on material for realism
        if material == 'Bricks':
            quantity = random.randint(5000, 25000)
        elif material == 'TMT Steel':
            quantity = random.randint(5, 50) # Tons
        else:
            quantity = random.randint(50, 500)
            
        unit_price = round(random.uniform(*MATERIALS[material]['Price']), 2)
        total_revenue = round(quantity * unit_price, 2)
        
        location = random.choice(LOCATIONS)
        delivery = random.choices(DELIVERY_STATUS, weights=[0.6, 0.2, 0.15, 0.05])[0]
        payment = random.choices(PAYMENT_STATUS, weights=[0.6, 0.3, 0.1])[0]

        data.append([
            order_date.strftime('%Y-%m-%d'),
            customer_name,
            material,
            category,
            quantity,
            unit_price,
            total_revenue,
            location,
            delivery,
            payment
        ])

    df = pd.DataFrame(data, columns=[
        'OrderDate', 'CustomerName', 'MaterialName', 'Category', 
        'Quantity', 'UnitPrice', 'TotalRevenue', 'Location', 
        'DeliveryStatus', 'PaymentStatus'
    ])

    output_file = 'buildex_data.csv'
    df.to_csv(output_file, index=False)
    print(f"Successfully generated {num_rows} rows of dummy data and saved to {output_file}")

if __name__ == '__main__':
    generate_buildex_data()
