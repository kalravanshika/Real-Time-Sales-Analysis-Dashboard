from kafka import KafkaConsumer
import json
import mysql.connector

def save_to_mysql(record, cursor, conn):
    sql = """
    INSERT INTO sales_data (
        customer_id, customer_name, customer_age, customer_gender, customer_location,
        product_id, product_name, product_category, product_brand, product_rating,
        transaction_id, quantity, price, discount_applied, total_amount, payment_method,
        order_date, order_time, delivery_time
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    data = (
        record["customer_id"], record["customer_name"], record["customer_age"], record["customer_gender"],
        record["customer_location"], record["product_id"], record["product_name"], record["product_category"],
        record["product_brand"], record["product_rating"], record["transaction_id"], record["quantity"],
        record["price"], record["discount_applied"], record["total_amount"], record["payment_method"],
        record["order_date"], record["order_time"], record["delivery_time"]
    )
    cursor.execute(sql, data)
    conn.commit()

def start_consumer():
    # Set up MySQL connection
    conn = mysql.connector.connect(
        host="localhost",         # change if needed
        user="root",   # replace with your MySQL username
        password="Glitch@142",  # replace with your MySQL password
        database="MajorProject"       # your MySQL database name
    )
    cursor = conn.cursor()

    # Set up Kafka consumer
    consumer = KafkaConsumer(
        'sales-data',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='mysql_saver_group',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    print("Listening to Kafka topic 'sales-data' and saving records to MySQL...")

    for message in consumer:
        record = message.value
        print("Received:", record)
        try:
            save_to_mysql(record, cursor, conn)
            print("Saved to MySQL:", record["transaction_id"])
        except Exception as e:
            print("Error saving to MySQL:", e)

if __name__ == "__main__":
    start_consumer()
