import os
from celery import Celery

# configure Celery using config in app.config
broker = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
backend = os.environ.get("CELERY_RESULT_BACKEND", broker)

celery = Celery("ats_tasks", broker=broker, backend=backend)

@celery.task
def send_email_task(recipient_email, subject, body):
    """
    Mocked email send — print to console.
    In production you'd call an email provider SDK here.
    """
    print(f"[send_email_task] To: {recipient_email} | Subject: {subject} | Body: {body}")
    return {"status": "sent", "recipient": recipient_email}
