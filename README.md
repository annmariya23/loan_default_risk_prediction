# Loan Default Risk Prediction Using Apache Spark and Machine Learning

## 📌 Project Overview

Loan Default Risk Prediction is a Big Data and Machine Learning project that predicts whether a loan applicant is likely to default on a loan.

The project uses the **Lending Club Loan Dataset** and **Apache Spark / PySpark** to process the data and build machine learning classification models.

The main objective is to identify applicants who are at higher risk of loan default and provide a simple web interface for demonstrating loan risk prediction.

---

## 🎯 Objectives

- Process a large Lending Club loan dataset using Apache Spark.
- Clean and prepare the loan data for machine learning.
- Select relevant features for prediction.
- Create a binary target variable called `default_flag`.
- Train machine learning classification models using Spark MLlib.
- Compare Logistic Regression and Random Forest models.
- Evaluate the models using Accuracy, F1 Score, and AUC.
- Build a simple web interface for loan risk prediction.

---

## 📊 Dataset

The project uses the **Lending Club Historical Loan Dataset**.

### Dataset Information

- Total records: approximately **1.34 million**
- Original attributes: approximately **150**
- Selected features: **16**
- Target variable: `default_flag`

### Target Variable

| Value | Meaning |
|------:|---------|
| `0` | Non-default |
| `1` | Default |

The dataset contains approximately:

- **80% Non-default loans**
- **20% Default loans**

---

## 🔢 Features Used

The following 16 numerical features are used for model training:

1. `loan_amnt`
2. `funded_amnt`
3. `funded_amnt_inv`
4. `int_rate`
5. `installment`
6. `annual_inc`
7. `dti`
8. `delinq_2yrs`
9. `inq_last_6mths`
10. `open_acc`
11. `pub_rec`
12. `revol_bal`
13. `revol_util`
14. `total_acc`
15. `mort_acc`
16. `pub_rec_bankruptcies`

---

## ⚙️ Technologies Used

- Python
- Apache Spark
- PySpark
- Spark MLlib
- Jupyter Notebook
- Pandas
- NumPy
- Matplotlib
- HTML
- CSS
- JavaScript

---

## 🌐 Live Demo

The project web interface is available online:

👉 **[Loan Default Risk Prediction – Live Demo](https://starlit-gelato-4ad3c8.netlify.app/)**

The web application allows users to enter the 16 loan and credit features and view a loan default risk prediction. 1
## 🔄 Project Workflow

```text
Lending Club Dataset
        ↓
Data Ingestion
        ↓
Data Cleaning
        ↓
Feature Selection
        ↓
Create default_flag
        ↓
Train / Test Split
        ↓
VectorAssembler
        ↓
Machine Learning Models
        ↓
Model Evaluation
        ↓
Risk Prediction
        ↓
Web Interface
