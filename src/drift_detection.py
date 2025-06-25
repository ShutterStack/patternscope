# 📁 src/drift_detection.py
import pandas as pd
import numpy as np
from scipy.stats import entropy
from datetime import datetime
import os

def calculate_psi(expected, actual, buckets=10):
    psi_scores = {}
    for col in expected.columns:
        try:
            quantiles = np.percentile(expected[col], np.linspace(0, 100, buckets + 1))
            expected_counts = np.histogram(expected[col], bins=quantiles)[0] + 1e-6
            actual_counts = np.histogram(actual[col], bins=quantiles)[0] + 1e-6
            expected_perc = expected_counts / expected_counts.sum()
            actual_perc = actual_counts / actual_counts.sum()
            psi = np.sum((expected_perc - actual_perc) * np.log(expected_perc / actual_perc))
            psi_scores[col] = round(psi, 4)
        except:
            psi_scores[col] = None
    return psi_scores

def null_check(df):
    return df.isnull().mean().round(4).to_dict()

def class_balance(df, target_col="Churn"):
    return df[target_col].value_counts(normalize=True).round(4).to_dict()

if __name__ == "__main__":
    base = pd.read_csv(r"D:\\patternscope\\data\\telco_churn.csv")
    new = pd.read_csv(r"D:\\patternscope\\data\\telco_churn.csv")  # Simulated new batch
    from train import preprocess
    base_proc = preprocess(base)
    new_proc = preprocess(new)

    psi = calculate_psi(base_proc.drop("Churn", axis=1), new_proc.drop("Churn", axis=1))
    nulls = null_check(new)
    class_dist = class_balance(new)

    print("📊 PSI Scores:")
    print(psi)
    print("\n🧪 Null Value %:")
    print(nulls)
    print("\n📉 Class Distribution:")
    print(class_dist)

    # Save drift results to CSV log
    os.makedirs("logs", exist_ok=True)
    with open("logs/drift_log.csv", "a") as log:
        log.write(f"{datetime.now()},{psi},{nulls},{class_dist}\n")
