# gradio_ui/app.py
import gradio as gr
import requests

API_URL = "http://localhost:8000"

def handle_upload(file):
    files = {'file': open(file.name, 'rb')}
    response = requests.post(f"{API_URL}/upload/", files=files)
    return response.json()["message"]

def detect_drift():
    r = requests.post(f"{API_URL}/drift/")
    drift = r.json()
    out = f"📊 **PSI Scores:**\n{drift['psi']}\n\n🧪 **Null Percentage:**\n{drift['nulls']}\n\n📉 **Class Distribution:**\n{drift['class_distribution']}"
    return out

def trigger_retrain():
    r = requests.post(f"{API_URL}/train/")
    return r.json()["message"]

def get_metrics():
    r = requests.get(f"{API_URL}/metrics/")
    metrics = r.json()
    return f"""
**Accuracy**: {metrics['accuracy']:.2f}
**Precision**: {metrics['weighted avg']['precision']:.2f}
**Recall**: {metrics['weighted avg']['recall']:.2f}
**F1-score**: {metrics['weighted avg']['f1-score']:.2f}
"""

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("## 💡 PatternScope: ML Model Monitoring and Drift Detection")

    with gr.Tab("📁 Upload New Data"):
        file_input = gr.File(label="Upload CSV")
        upload_btn = gr.Button("Upload")
        upload_output = gr.Textbox(label="Upload Status", interactive=False)
        upload_btn.click(fn=handle_upload, inputs=[file_input], outputs=[upload_output])

    with gr.Tab("🧠 Drift Detection"):
        drift_btn = gr.Button("Run Drift Check")
        drift_output = gr.Textbox(label="Drift Report", lines=12, interactive=False)
        drift_btn.click(fn=detect_drift, outputs=[drift_output])

    with gr.Tab("🔁 Retrain Model"):
        retrain_btn = gr.Button("Retrain Model")
        retrain_output = gr.Textbox(label="Retrain Status", interactive=False)
        retrain_btn.click(fn=trigger_retrain, outputs=[retrain_output])

    with gr.Tab("📊 Evaluation Metrics"):
        metrics_btn = gr.Button("Show Latest Metrics")
        metrics_output = gr.Textbox(label="Model Metrics", lines=6, interactive=False)
        metrics_btn.click(fn=get_metrics, outputs=[metrics_output])

demo.launch()
