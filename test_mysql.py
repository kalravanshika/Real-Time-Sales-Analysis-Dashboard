import mysql.connector

print("🚀 Starting MySQL connection test...")

try:
    print("🔄 Attempting to connect to MySQL with a 5-second timeout...")

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Glitch@142",
        database="sales_dashboard",
        connection_timeout=5  # ✅ Timeout to prevent freezing
    )

    print("✅ Connected to MySQL successfully!")

    cursor = conn.cursor()
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()
    print("✅ Tables in database:", tables)

    cursor.execute("SELECT COUNT(*) FROM sales_data;")
    count = cursor.fetchone()[0]
    print(f"📊 Total records in sales_data: {count}")

    cursor.close()
    conn.close()
    print("✅ MySQL connection closed!")

except mysql.connector.Error as err:
    print(f"❌ MySQL Error: {err}")  # ✅ Print exact MySQL error
except Exception as e:
    print(f"❌ General Error: {e}")  # ✅ Catch any other errors
finally:
    print("🔚 End of script.")