from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False)  # candidate, recruiter, hiring_manager


class Job(db.Model):
    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(1000))
    tenant = db.Column(db.String(200))  # company name


class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)
    candidate_name = db.Column(db.String(200), nullable=False)
    candidate_email = db.Column(db.String(200), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=False)
    status = db.Column(db.String(50), nullable=False, default="applied")
    created_at = db.Column(db.DateTime, default=db.func.now())

class ApplicationHistory(db.Model):
    __tablename__ = "application_history"

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, nullable=False)
    from_state = db.Column(db.String(50))
    to_state = db.Column(db.String(50))
    changed_at = db.Column(db.DateTime, default=db.func.now())

