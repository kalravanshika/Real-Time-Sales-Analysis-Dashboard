from kafka import KafkaProducer
import json
import time
from generate_sales_data import generate_sales_record  # your function

def start_producer():
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )
    print("Producer started...")

    while True:
        record = generate_sales_record()
        data = dict(zip([
            "customer_id", "customer_name", "customer_age", "customer_gender", "customer_location",
            "product_id", "product_name", "product_category", "product_brand", "product_rating",
            "transaction_id", "quantity", "price", "discount_applied", "total_amount", "payment_method",
            "order_date", "order_time", "delivery_time"
        ], record))

        producer.send('sales-data', value=data)
        producer.flush()  # force sending the message immediately
        print("Sent:", data)
        time.sleep(1)  # send every second

if __name__ == "__main__":
    start_producer()
