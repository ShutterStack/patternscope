# 🧠 PatternScope: End-to-End ML Monitoring & Drift Detection

PatternScope is a fully modular and automated platform for monitoring ML model health in production environments. It integrates CI/CD, drift detection, evaluation logging, alerting, and real-time metrics visualization using FastAPI, Gradio, GitLab, Prometheus, and Grafana.

---

## 📁 Project Structure Overview

```
patternscope/
├── src/                  # ML logic: training, eval, drift detection, alerts
├── gradio_ui/           # Gradio app interface
├── monitoring/          # Prometheus + Grafana docker setup
├── logs/                # Evaluation metrics + drift logs
├── data/                # Datasets (e.g., telco_churn.csv)
├── models/              # Trained models (.pkl)
├── config.yaml          # Configurations (optional)
├── Dockerfile           # Containerizing app
├── .gitlab-ci.yml       # CI/CD pipeline
└── README.md            # This file
```

---

## ✅ Phase 1: ML Pipeline

### ✅ Training

- File: `src/train.py`
- Preprocesses data, trains model, saves to `models/latest.pkl`

### ✅ Evaluation

- File: `src/evaluate.py`
- Computes classification metrics
- Logs F1-score to `logs/metrics.json`

### ✅ Drift Detection

- File: `src/drift_detection.py`
- Computes PSI, null %, class balance
- Logs output to `logs/drift_log.csv`

---

## ✅ Phase 2: API + Gradio Frontend

### ✅ FastAPI Backend

- File: `fastapi_app.py`
- Endpoints:
  - `/upload/` – Upload batch
  - `/drift/` – Run drift check
  - `/train/` – Retrain model
  - `/metrics/` – Get eval metrics

### ✅ Gradio UI

- File: `gradio_ui/app.py`
- Upload CSV, trigger drift, view metrics, retrain model

---

## ✅ Phase 3: Docker + GitLab CI/CD

### ✅ Dockerfile

- Containerizes backend + frontend
- Exposes port `7860` for Gradio

### ✅ .gitlab-ci.yml

- Stages: `test → train → evaluate → check → deploy`
- Fails if F1 < threshold (default 0.85)
- Pushes Docker image to GitLab registry

---

## ✅ Phase 4: Monitoring & Alerting

### ✅ Prometheus + Grafana

- Folder: `monitoring/`
- Files:
  - `docker-compose.yml`: launches both services
  - `prometheus.yml`: scrapes FastAPI `/metrics`

### ✅ FastAPI Monitoring

- Exposed metrics using `prometheus_fastapi_instrumentator`
- Metrics available at `/metrics`

### ✅ Drift + Metric Logging

- Drift logs to `logs/drift_log.csv`
- F1-score logs to `logs/metrics.json`

### ✅ Email Alerts

- File: `src/alert_email.py`
- Uses Gmail SMTP to send alert when F1 < threshold
- Triggered from `.gitlab-ci.yml` `check` stage

---

## 🔧 Setup Instructions

### 1. Install Requirements

```bash
pip install -r requirements.txt
```

### 2. Run Gradio + FastAPI

```bash
python gradio_ui/app.py
# FastAPI should be running at http://localhost:8000
# Gradio should be running at http://localhost:7860
```

### 3. Start Monitoring Stack

```bash
cd monitoring
docker-compose up -d
```

- Prometheus: [http://localhost:9090](http://localhost:9090)
- Grafana: [http://localhost:3000](http://localhost:3000) (admin/admin)

### 4. Add Prometheus in Grafana

- URL: `http://host.docker.internal:9090` (or `172.17.0.1` on Linux)

### 5. Add Panels (in Dashboard)

- `http_requests_total`: line chart of total requests
- `http_request_duration_seconds_count`: request timing histogram
- `custom_model_f1_score` (optional): Gauge panel showing latest F1

### 6. Configure Email Alerts

- Create Gmail App Password
- Store as GitLab CI/CD secrets:
  - `ALERT_EMAIL_SENDER`
  - `ALERT_EMAIL_RECEIVER`
  - `ALERT_EMAIL_PASSWORD`

---

## 🧪 Run Locally

```bash
python src/evaluate.py
python src/drift_detection.py
```

Check:

- `logs/metrics.json`
- `logs/drift_log.csv`

---

## 📦 Build Docker Image Manually

```bash
docker build -t patternscope:latest .
docker run -p 7860:7860 patternscope:latest
```

---

## 📌 Next Steps

- Add `/predict` endpoint with real-time logging
- Enable Slack or advanced Prometheus alerts
- Publish Grafana dashboards
- Auto-retraining and deployment rollback

---

Made with ❤️ for production-grade ML monitoring.

