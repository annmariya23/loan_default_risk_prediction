import os
import sys

# Force Spark to use this virtual environment's Python
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("TestWrite")
    .master("local[2]")
    .config("spark.driver.host", "127.0.0.1")
    .config("spark.driver.bindAddress", "127.0.0.1")
    .getOrCreate()
)

print("Spark started")

df = spark.range(10)

print("Rows:", df.count())

output_path = r"D:\loan_default\data\test_output"

print("Writing Parquet...")

df.write.mode("overwrite").parquet(output_path)

print("PARQUET WRITE SUCCESS!")
print(output_path)

spark.stop()