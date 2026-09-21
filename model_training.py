import os

from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, OneHotEncoder, VectorAssembler
from pyspark.ml.classification import LogisticRegression, RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator


# ============================================================
# MEMBER 3 - LOAN DEFAULT MODEL COMPARISON
# ============================================================

# Spark temporary directory
spark_temp = r"D:\loan_default\spark_temp"
os.makedirs(spark_temp, exist_ok=True)

spark = (
    SparkSession.builder
    .appName("LoanDefaultModelComparison")
    .master("local[2]")
    .config("spark.driver.memory", "4g")
    .config("spark.local.dir", spark_temp)
    .config("spark.sql.shuffle.partitions", "8")
    .config("spark.default.parallelism", "8")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

print("=" * 60)
print("MEMBER 3 - LOAN DEFAULT MODEL COMPARISON")
print("=" * 60)


# ============================================================
# 1. LOAD MEMBER 2 CLEANED DATA
# ============================================================

data_path = r"D:\loan_default\data\data_cleaned"

print("\nLoading cleaned dataset...")

df = spark.read.parquet(data_path)

print("Dataset loaded successfully.")


# ============================================================
# 2. TAKE A REPRESENTATIVE SAMPLE
# ============================================================

print("\nCreating sample for model training...")

# Keep full data_cleaned untouched.
# Use 100,000 rows for faster model development.

df = df.sample(
    withReplacement=False,
    fraction=0.05,
    seed=42
)

# Limit to 100,000 rows if the sample is larger
df = df.limit(20000)
print("Sample created.")

print("Sample rows: 20,000 maximum")

# ============================================================
# 3. CHECK LABEL
# ============================================================

if "label" not in df.columns:
    raise Exception(
        "ERROR: 'label' column not found in cleaned data."
    )

df = df.withColumn(
    "label",
    col("label").cast("double")
)

print("\nLabel distribution:")

df.groupBy("label").count().orderBy("label").show()


# ============================================================
# 4. REMOVE DATA-LEAKAGE COLUMN
# ============================================================

if "loan_status" in df.columns:
    df = df.drop("loan_status")


# ============================================================
# 5. FIND FEATURE TYPES
# ============================================================

numeric_columns = []
categorical_columns = []

for field in df.schema.fields:

    if field.name == "label":
        continue

    data_type = field.dataType.simpleString()

    if data_type in [
        "int",
        "bigint",
        "double",
        "float",
        "long",
        "short"
    ]:
        numeric_columns.append(field.name)

    elif data_type == "string":
        categorical_columns.append(field.name)


print("\nNumeric columns:")
print(numeric_columns)

print("\nCategorical columns:")
print(categorical_columns)


# ============================================================
# 6. HANDLE MISSING VALUES
# ============================================================

for c in numeric_columns:
    df = df.fillna({c: 0})

for c in categorical_columns:
    df = df.fillna({c: "Unknown"})


# ============================================================
# 7. STRING INDEXING
# ============================================================

indexers = []

for c in categorical_columns:

    indexers.append(
        StringIndexer(
            inputCol=c,
            outputCol=c + "_index",
            handleInvalid="keep"
        )
    )


# ============================================================
# 8. ONE-HOT ENCODING
# ============================================================

encoded_columns = []

if categorical_columns:

    encoder = OneHotEncoder(
        inputCols=[
            c + "_index"
            for c in categorical_columns
        ],
        outputCols=[
            c + "_encoded"
            for c in categorical_columns
        ]
    )

    encoded_columns = [
        c + "_encoded"
        for c in categorical_columns
    ]

else:
    encoder = None


# ============================================================
# 9. FEATURE ASSEMBLER
# ============================================================

feature_columns = (
    numeric_columns +
    encoded_columns
)

assembler = VectorAssembler(
    inputCols=feature_columns,
    outputCol="features",
    handleInvalid="keep"
)


# ============================================================
# 10. TRAIN / TEST SPLIT
# ============================================================

print("\nSplitting sample...")

train_data, test_data = df.randomSplit(
    [0.8, 0.2],
    seed=42
)

print("Training rows:", train_data.count())
print("Testing rows :", test_data.count())


# ============================================================
# 11. EVALUATOR
# ============================================================

f1_evaluator = MulticlassClassificationEvaluator(
    labelCol="label",
    predictionCol="prediction",
    metricName="f1"
)

accuracy_evaluator = MulticlassClassificationEvaluator(
    labelCol="label",
    predictionCol="prediction",
    metricName="accuracy"
)

precision_evaluator = MulticlassClassificationEvaluator(
    labelCol="label",
    predictionCol="prediction",
    metricName="weightedPrecision"
)

recall_evaluator = MulticlassClassificationEvaluator(
    labelCol="label",
    predictionCol="prediction",
    metricName="weightedRecall"
)


# ============================================================
# 12. FUNCTION TO TRAIN MODEL
# ============================================================

def train_model(model, model_name):

    print("\n" + "=" * 60)
    print("TRAINING:", model_name)
    print("=" * 60)

    stages = indexers.copy()

    if encoder is not None:
        stages.append(encoder)

    stages.append(assembler)
    stages.append(model)

    pipeline = Pipeline(
        stages=stages
    )

    trained_model = pipeline.fit(train_data)

    predictions = trained_model.transform(test_data)

    accuracy = accuracy_evaluator.evaluate(
        predictions
    )

    precision = precision_evaluator.evaluate(
        predictions
    )

    recall = recall_evaluator.evaluate(
        predictions
    )

    f1 = f1_evaluator.evaluate(
        predictions
    )

    print("\nResults:")
    print("Accuracy :", round(accuracy, 4))
    print("Precision:", round(precision, 4))
    print("Recall   :", round(recall, 4))
    print("F1 Score :", round(f1, 4))

    return (
        trained_model,
        predictions,
        accuracy,
        precision,
        recall,
        f1
    )


# ============================================================
# 13. LOGISTIC REGRESSION
# ============================================================

lr = LogisticRegression(
    featuresCol="features",
    labelCol="label",
    maxIter=10
)

(
    lr_model,
    lr_predictions,
    lr_accuracy,
    lr_precision,
    lr_recall,
    lr_f1
) = train_model(
    lr,
    "Logistic Regression"
)


# ============================================================
# 14. RANDOM FOREST
# ============================================================

rf = RandomForestClassifier(
    featuresCol="features",
    labelCol="label",
    numTrees=20,
    maxDepth=5,
    seed=42
)

(
    rf_model,
    rf_predictions,
    rf_accuracy,
    rf_precision,
    rf_recall,
    rf_f1
) = train_model(
    rf,
    "Random Forest"
)


# ============================================================
# 15. COMPARE MODELS
# ============================================================

print("\n" + "=" * 60)
print("MODEL COMPARISON")
print("=" * 60)

print("\nLogistic Regression")
print("Accuracy :", round(lr_accuracy, 4))
print("Precision:", round(lr_precision, 4))
print("Recall   :", round(lr_recall, 4))
print("F1 Score :", round(lr_f1, 4))

print("\nRandom Forest")
print("Accuracy :", round(rf_accuracy, 4))
print("Precision:", round(rf_precision, 4))
print("Recall   :", round(rf_recall, 4))
print("F1 Score :", round(rf_f1, 4))


# ============================================================
# 16. SELECT BETTER MODEL
# ============================================================

if rf_f1 > lr_f1:

    best_model = rf_model
    best_predictions = rf_predictions
    best_name = "Random Forest"
    best_f1 = rf_f1

else:

    best_model = lr_model
    best_predictions = lr_predictions
    best_name = "Logistic Regression"
    best_f1 = lr_f1


print("\n" + "=" * 60)
print("BEST MODEL")
print("=" * 60)

print("Selected model:", best_name)
print("F1 Score:", round(best_f1, 4))


# ============================================================
# 17. SAVE ONLY BEST MODEL
# ============================================================

model_output = r"D:\loan_default\best_model"

best_model.write().overwrite().save(
    model_output
)

print("\nBest model saved to:")

print(model_output)


# ============================================================
# 18. SAVE FINAL PREDICTIONS
# ============================================================

prediction_output = (
    r"D:\loan_default\data\final_predictions"
)

best_predictions.select(
    "label",
    "prediction",
    "probability"
).write.mode(
    "overwrite"
).parquet(
    prediction_output
)

print("\nFinal predictions saved to:")

print(prediction_output)


# ============================================================
# 19. FINISHED
# ============================================================

print("\n" + "=" * 60)
print("MEMBER 3 COMPLETED")
print("=" * 60)

print("Final model:", best_name)

spark.stop()