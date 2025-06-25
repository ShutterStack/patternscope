# src/train.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
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

def train_model(data_path=r"D:\patternscope\data\telco_churn.csv", model_path=r"D:\patternscope\models/latest.pkl"):
    df = pd.read_csv(data_path)
    df = preprocess(df)
    
    X = df.drop("Churn", axis=1)
    y = df["Churn"].apply(lambda x: 1 if x == "Yes" else 0)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)
    print(f"✅ Model saved at {model_path}")

if __name__ == "__main__":
    train_model()
