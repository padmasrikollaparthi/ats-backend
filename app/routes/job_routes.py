from flask import Blueprint, request, jsonify
from app import db
from app.models import Job
from app.services.authz import require_role

job_bp = Blueprint("jobs", __name__)

@job_bp.route("/", methods=["GET"])
def list_jobs():
    jobs = Job.query.all()
    return jsonify([
        {
            "id": j.id,
            "title": j.title,
            "description": j.description,
            "tenant": j.tenant
        } for j in jobs
    ]), 200

@job_bp.route("/", methods=["POST"])
@require_role("recruiter")
def create_job():
    data = request.get_json() or {}
    title = data.get("title")

    if not title:
        return jsonify({"error": "title required"}), 400

    job = Job(
        title=title,
        description=data.get("description"),
        tenant=data.get("tenant")
    )
    db.session.add(job)
    db.session.commit()

    return jsonify({"message": "job created", "id": job.id}), 201

@job_bp.route("/<int:job_id>", methods=["PUT"])
@require_role("recruiter")
def update_job(job_id):
    job = Job.query.get(job_id)
    if not job:
        return jsonify({"error": "job not found"}), 404

    data = request.get_json() or {}
    job.title = data.get("title", job.title)
    job.description = data.get("description", job.description)
    job.tenant = data.get("tenant", job.tenant)

    db.session.commit()
    return jsonify({"message": "job updated"}), 200

@job_bp.route("/<int:job_id>", methods=["DELETE"])
@require_role("recruiter")
def delete_job(job_id):
    job = Job.query.get(job_id)
    if not job:
        return jsonify({"error": "job not found"}), 404

    db.session.delete(job)
    db.session.commit()
    return jsonify({"message": "job deleted"}), 200
