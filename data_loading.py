import os
import sys

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("LoanDefaultRiskPrediction") \
    .master("local[*]") \
    .config("spark.hadoop.io.native.lib.available", "false") \
    .getOrCreate()

print("=" * 60)
print("LOAN DEFAULT RISK PREDICTION")
print("Spark Version:", spark.version)
print("=" * 60)

file_path = "data\dataset.csv"

print("\nLoading dataset...")

df = spark.read \
    .option("header", True) \
    .option("inferSchema", False) \
    .csv(file_path)

print("Dataset loaded successfully!")

print("\nNumber of columns:", len(df.columns))

print("\nColumn names:")
print(df.columns)

print("\nFirst 5 records:")
df.show(5, truncate=True)

print("\nChecking loan_status:")
df.select("loan_status").show(10)

spark.stop()

print("\nSpark stopped successfully.")