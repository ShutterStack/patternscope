import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_alert(f1_score):
    sender = "your_email@gmail.com"
    receiver = "target_email@gmail.com"
    password = "your_app_password"  # Use App Password

    message = MIMEMultipart("alternative")
    message["Subject"] = "PatternScope: 🚨 Model Performance Alert"
    message["From"] = sender
    message["To"] = receiver

    html = f"""
    <html>
      <body>
        <p>🚨 Alert: Model F1-score dropped below threshold.<br>
           Current F1-score: <b>{f1_score:.2f}</b><br>
           Please investigate.</p>
      </body>
    </html>
    """
    message.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, message.as_string())