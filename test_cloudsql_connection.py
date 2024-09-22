from pyspark.sql import SparkSession

# Initialize Spark session
spark = SparkSession.builder \
    .appName("CloudSQLProxyTest") \
    .getOrCreate()

# JDBC connection properties
jdbc_url = "jdbc:postgresql://google/postgres?cloudSqlInstance=systool-436201:us-central1:postgres&socketFactory=com.google.cloud.sql.postgres.SocketFactory"
connection_properties = {
    "user": "postgres",
    "password": "pg_password",
    "driver": "org.postgresql.Driver"
}

# Test: Read from a table (make sure a table exists in your DB)
try:
    df = spark.read.jdbc(url=jdbc_url, table="your_table_name", properties=connection_properties)
    df.show()  # Show first few rows from the table
except Exception as e:
    print(f"Failed to connect to CloudSQL: {e}")

# Stop the Spark session
spark.stop()
