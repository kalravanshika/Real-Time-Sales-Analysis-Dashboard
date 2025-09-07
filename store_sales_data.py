from pyspark.sql import SparkSession
import pandas as pd
import mysql.connector

# ✅ Step 1: Create Spark Session
spark = SparkSession.builder \
    .appName("SalesDataProcessing") \
    .config("spark.driver.memory", "2g") \
    .getOrCreate()

# ✅ Step 2: Load CSV File into Spark DataFrame
try:
    df = spark.read.csv("sales_data.csv", header=True, inferSchema=True)
    print("✅ Successfully loaded sales_data.csv into Spark")
except Exception as e:
    print(f"❌ Error loading CSV file: {e}")
    exit()

# ✅ Step 3: Show First Few Rows of Spark DataFrame
df.show(5)

# ✅ Step 4: Convert Spark DataFrame to Pandas DataFrame
sales_df = df.toPandas()

# ✅ Step 5: Debug - Print First Few Rows Before Inserting into MySQL
print("✅ Sample Data Before Inserting into MySQL:")
print(sales_df.head())

# ✅ Stop Execution if DataFrame is Empty
if sales_df.empty:
    print("❌ No data found! Exiting script.")
    exit()


    
# ✅ Step 6: Connect to MySQL Database
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",  # Replace with your username
        password="Glitch@142",  # Replace with your password
        database="sales_dashboard"
    )
    cursor = conn.cursor()
    print("✅ Connected to MySQL successfully!")  # ✅ This should print
except Exception as e:
    print(f"❌ Error connecting to MySQL: {e}")
    exit()

# ✅ Step 7: Prepare SQL Query for Batch Insert
sql = """INSERT INTO sales_data (timestamp, product, region, quantity, price, payment_method, customer_type, discount)
         VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

# ✅ Debug: Print the SQL Query and Sample Row
print("✅ Sample SQL Insert Query:")
print(sql)
print("✅ First Row Being Inserted:")
print(tuple(sales_df.iloc[0].values))

# ✅ Step 8: Convert Pandas DataFrame to List of Tuples for Fast Insertion
data_tuples = [tuple(x) for x in sales_df.to_numpy()]

# ✅ Step 9: Insert into MySQL (Catch Errors)
try:
    cursor.executemany(sql, data_tuples)
    conn.commit()
    print("✅ Data successfully stored in MySQL!")
except Exception as e:
    print(f"❌ Error inserting data into MySQL: {e}")
    exit()

# ✅ Step 10: Close MySQL Connection
cursor.close()
conn.close()
print("✅ MySQL Connection Closed!")
