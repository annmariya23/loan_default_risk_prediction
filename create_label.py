import os
import sys

# Use Python from the virtual environment
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when

# Start Spark
spark = SparkSession.builder \
    .appName("Loan Default Risk Prediction") \
    .master("local[*]") \
    .config("spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version", "2") \
    .config("spark.hadoop.mapreduce.fileoutputcommitter.cleanup-failures.ignored", "true") \
    .getOrCreate()
print("=" * 60)
print("MEMBER 1 - LOAN DATA PREPROCESSING")
print("=" * 60)

# Dataset
file_path = r"D:\loan_default\data\dataset.csv"

print("\nLoading dataset...")

df = spark.read \
    .option("header", True) \
    .option("inferSchema", False) \
    .csv(file_path)

print("Dataset loaded successfully!")

# Valid loan statuses
valid_statuses = [
    "Fully Paid",
    "Current",
    "In Grace Period",
    "Charged Off",
    "Late (31-120 days)",
    "Late (16-30 days)",
    "Default"
]

# Remove unwanted statuses
df = df.filter(
    col("loan_status").isin(valid_statuses)
)

print("\nInvalid/unwanted statuses removed.")

# Create target label
df = df.withColumn(
    "label",
    when(
        col("loan_status").isin(
            "Charged Off",
            "Late (31-120 days)",
            "Late (16-30 days)",
            "Default"
        ),
        1
    ).otherwise(0)
)

print("\nLabel created:")
print("0 = Non-default")
print("1 = Default")

# Show distribution
print("\nLabel Distribution:")

df.groupBy("label") \
    .count() \
    .orderBy("label") \
    .show()

print("\nLoan Status + Label:")

df.groupBy("loan_status", "label") \
    .count() \
    .orderBy("label", "loan_status") \
    .show(truncate=False)

# Remove duplicate records
before = df.count()

df = df.dropDuplicates()

after = df.count()

print("\nDuplicates removed:", before - after)

print("Remaining records:", after)

# Save processed dataset
# Save processed dataset as CSV

output_path = r"D:\loan_default\data\labeled_loan_data"

print("\nSaving processed dataset...")

df.write \
    .mode("overwrite") \
    .parquet(output_path)

print("\nProcessed dataset saved successfully!")

print(output_path)

spark.stop()
print("\nProcessed dataset saved successfully!")

print(output_path)

spark.stop()

print("\n" + "=" * 60)
print("MEMBER 1 LABEL CREATION COMPLETED")
print("=" * 60)