from flask import Blueprint, request, jsonify
from app import db
from app.models import Job

job_bp = Blueprint("jobs", __name__)

@job_bp.route("/", methods=["GET"])
def list_jobs():
    jobs = Job.query.all()
    result = []
    for j in jobs:
        result.append({"id": j.id, "title": j.title, "description": j.description, "tenant": j.tenant})
    return jsonify({"jobs": result}), 200

@job_bp.route("/", methods=["POST"])
def create_job():
    data = request.get_json() or {}
    title = data.get("title")
    if not title:
        return jsonify({"error": "title required"}), 400
    description = data.get("description")
    tenant = data.get("tenant")
    job = Job(title=title, description=description, tenant=tenant)
    db.session.add(job)
    db.session.commit()
    return jsonify({"message": "job created", "job": {"id": job.id, "title": job.title}}), 201

@job_bp.route("/<int:job_id>", methods=["GET"])
def get_job(job_id):
    job = Job.query.get(job_id)
    if not job:
        return jsonify({"error": "job not found"}), 404
    return jsonify({"id": job.id, "title": job.title, "description": job.description, "tenant": job.tenant}), 200

@job_bp.route("/<int:job_id>", methods=["PUT"])
def update_job(job_id):
    job = Job.query.get(job_id)
    if not job:
        return jsonify({"error": "job not found"}), 404
    data = request.get_json() or {}
    job.title = data.get("title", job.title)
    job.description = data.get("description", job.description)
    job.tenant = data.get("tenant", job.tenant)
    db.session.commit()
    return jsonify({"message": "job updated", "job": {"id": job.id, "title": job.title}}), 200

@job_bp.route("/<int:job_id>", methods=["DELETE"])
def delete_job(job_id):
    job = Job.query.get(job_id)
    if not job:
        return jsonify({"error": "job not found"}), 404
    db.session.delete(job)
    db.session.commit()
    return jsonify({"message": "job deleted"}), 200
