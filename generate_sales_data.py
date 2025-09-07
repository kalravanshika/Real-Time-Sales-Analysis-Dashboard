import random
import datetime
import time

# Product and customer attributes
products = ['Smartphone', 'Laptop', 'Headphones', 'Smartwatch', 'TV', 'Refrigerator', 'Washing Machine']
categories = ['Electronics', 'Home Appliances', 'Wearables']
brands = ['Samsung', 'Apple', 'Xiaomi', 'LG', 'Sony', 'Boat', 'OnePlus']
regions = ['North India', 'South India', 'East India', 'West India']
payment_methods = ['UPI', 'Credit/Debit Card', 'Cash', 'Net Banking']
genders = ['Male', 'Female']

# Price ranges for each product type
product_prices = {
    'Smartphone': (8000, 150000),
    'Laptop': (25000, 200000),
    'Headphones': (500, 30000),
    'Smartwatch': (2000, 50000),
    'TV': (10000, 300000),
    'Refrigerator': (15000, 100000),
    'Washing Machine': (12000, 80000)
}

# Function to generate a single record
def generate_sales_record():
    customer_id = random.randint(1000, 9999)
    customer_name = f"Customer_{customer_id}"
    customer_age = random.randint(18, 60)
    customer_gender = random.choice(genders)
    customer_location = random.choice(regions)

    product_name = random.choice(products)
    product_id = random.randint(1, 100)
    product_category = random.choice(categories)
    product_brand = random.choice(brands)
    product_rating = round(random.uniform(3.5, 5.0), 1)

    min_price, max_price = product_prices[product_name]
    price = round(random.uniform(min_price, max_price), 2)

    transaction_id = random.randint(100000, 999999)
    quantity = random.randint(1, 5)
    discount_applied = round(random.uniform(0, 0.3), 2)
    total_amount = round(quantity * price * (1 - discount_applied), 2)
    payment_method = random.choice(payment_methods)

    order_date = datetime.datetime.now().strftime('%Y-%m-%d')
    order_time = datetime.datetime.now().strftime('%H:%M:%S')
    delivery_time = (datetime.datetime.now() + datetime.timedelta(days=random.randint(1, 7))).strftime('%Y-%m-%d %H:%M:%S')

    return [
        customer_id, customer_name, customer_age, customer_gender, customer_location,
        product_id, product_name, product_category, product_brand, product_rating,
        transaction_id, quantity, price, discount_applied, total_amount, payment_method,
        order_date, order_time, delivery_time
    ]

# Function to continuously append records to a CSV file
def generate_real_time_data(file_path, interval=5):
    columns = [
        'customer_id', 'customer_name', 'customer_age', 'customer_gender', 'customer_location',
        'product_id', 'product_name', 'product_category', 'product_brand', 'product_rating',
        'transaction_id', 'quantity', 'price', 'discount_applied', 'total_amount', 'payment_method',
        'order_date', 'order_time', 'delivery_time'
    ]

    # Write headers
    with open(file_path, 'w') as file:
        file.write(','.join(columns) + '\n')

    while True:
        record = generate_sales_record()
        with open(file_path, 'a') as file:
            file.write(','.join(map(str, record)) + '\n')
        print(f"New record added: {record}")
        time.sleep(interval)

# Run this only when executing the script directly
if __name__ == "__main__":
    generate_real_time_data('sales_data_india.csv', interval=5)
