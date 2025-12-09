from app.services.background_tasks import send_email_task

def send_application_update(recipient_email, new_state):
    subject = f"Application status updated: {new_state}"
    body = f"Your application status is now: {new_state}"
    # schedule background task
    send_email_task.delay(recipient_email, subject, body)
