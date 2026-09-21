import os
import sys

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder \
    .appName("LoanStatusAnalysis") \
    .master("local[*]") \
    .getOrCreate()

file_path = r"D:\loan_default\data\dataset.csv"

df = spark.read \
    .option("header", True) \
    .option("inferSchema", False) \
    .csv(file_path)

print("\nLoan Status Distribution:")
df.groupBy("loan_status") \
    .count() \
    .orderBy(col("count").desc()) \
    .show(30, truncate=False)

spark.stop()