# 📁 src/evaluate.py
import pandas as pd
import joblib
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
import json
import os

def preprocess(df):
    df = df.drop(columns=["customerID"], errors='ignore')
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].fillna("Unknown")
        if df[col].nunique() <= 2:
            df[col] = LabelEncoder().fit_transform(df[col])
        else:
            df = pd.get_dummies(df, columns=[col], drop_first=True)
    df = df.dropna()
    return df

def evaluate_model(data_path=r"D:\\patternscope\\data\\telco_churn.csv", model_path=r"D:\\patternscope\\models\\latest.pkl", log_path=r"D:\\patternscope\\logs\\metrics.json"):
    df = pd.read_csv(data_path)
    df = preprocess(df)
    X = df.drop("Churn", axis=1)
    y = df["Churn"].apply(lambda x: 1 if x == "Yes" else 0)

    model = joblib.load(model_path)
    y_pred = model.predict(X)

    report = classification_report(y, y_pred, output_dict=True)
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    # Save only f1-score to metrics.json for monitoring
    f1_score = report['weighted avg']['f1-score']
    with open(log_path, "w") as f:
        json.dump({"f1-score": f1_score}, f, indent=4)

    print(f"📊 Evaluation metrics saved to {log_path}")
    return report

if __name__ == "__main__":
    evaluate_model()