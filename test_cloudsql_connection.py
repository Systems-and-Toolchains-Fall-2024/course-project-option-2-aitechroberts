from pyspark.sql import SparkSession

# Initialize Spark session
spark = SparkSession.builder \
    .appName("CloudSQLProxyTest") \
    .getOrCreate()

# JDBC connection properties
jdbc_url = "jdbc:postgresql://104.196.99.150:5432/projectdb"
connection_properties = {
    "user": "postgres",
    "password": "postgres_pw",
    "driver": "org.postgresql.Driver"
}

# Test: Read from a table (make sure a table exists in your DB)
try:
    df = spark.read.jdbc(url=jdbc_url, table="mqtt", properties=connection_properties)
    df.show()  # Show first few rows from the table
except Exception as e:
    print(f"Failed to connect to CloudSQL: {e}")

# Stop the Spark session
spark.stop()
