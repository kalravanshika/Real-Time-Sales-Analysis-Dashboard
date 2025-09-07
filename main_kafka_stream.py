import threading
from kafka_producer import start_producer
from kafka_consumer import start_consumer

if __name__ == "__main__":
    producer_thread = threading.Thread(target=start_producer)
    consumer_thread = threading.Thread(target=start_consumer)

    # Start consumer first to avoid missing messages
    consumer_thread.start()
    producer_thread.start()

    consumer_thread.join()
    producer_thread.join()
