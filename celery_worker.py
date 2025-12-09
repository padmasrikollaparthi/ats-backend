from app.services.background_tasks import celery

if __name__ == "__main__":
    # run with: python celery_worker.py worker
    # but we'll use the celery CLI in instructions; keep this small
    print("This file exists to show celery worker entry point if needed.")
