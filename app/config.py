import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Using SQLite for simplicity (single-file DB), exactly what project needs
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "..", "ats.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")
    # Celery broker (worker) connection
    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
