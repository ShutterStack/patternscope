# src/api.py
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import pandas as pd
import shutil
import os

from src.train import train_model
from src.evaluate import evaluate_model
from src.drift_detection import calculate_psi, null_check, class_balance
from src.train import preprocess

app = FastAPI()

DATA_PATH =r"D:\patternscope\data\incoming.csv"

@app.post("/upload/")
async def upload_data(file: UploadFile = File(...)):
    with open(DATA_PATH, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"message": f"{file.filename} uploaded successfully."}

@app.post("/drift/")
def drift_report():
    base_df = pd.read_csv(r"D:\patternscope\data\telco_churn.csv")
    new_df = pd.read_csv(DATA_PATH)
    base_proc = preprocess(base_df)
    new_proc = preprocess(new_df)
    psi = calculate_psi(base_proc.drop("Churn", axis=1), new_proc.drop("Churn", axis=1))
    nulls = null_check(new_df)
    class_dist = class_balance(new_df)
    return {
        "psi": psi,
        "nulls": nulls,
        "class_distribution": class_dist
    }

@app.post("/train/")
def retrain():
    train_model(data_path=r"D:\patternscope\data\incoming.csv", model_path=r"D:\patternscope\models\latest.pkl")
    return {"message": "Model retrained and saved."}

@app.get("/metrics/")
def metrics():
    report = evaluate_model(data_path=r"D:\patternscope\data\incoming.csv")
    return JSONResponse(content=report)
