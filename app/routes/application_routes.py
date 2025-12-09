from flask import Blueprint, request, jsonify
from app import db
from app.models import Application, Job
from app.services.state_machine import ApplicationStateMachine
from app.services.email_service import send_application_update

application_bp = Blueprint("applications", __name__)

@application_bp.route("/", methods=["POST"])
def create_application():
    """
    Create application:
    JSON expected: { "candidate_name": "...", "candidate_email": "...", "job_id": 1 }
    """
    data = request.get_json() or {}
    name = data.get("candidate_name")
    email = data.get("candidate_email")
    job_id = data.get("job_id")
    if not name or not email or not job_id:
        return jsonify({"error": "candidate_name, candidate_email and job_id are required"}), 400

    job = Job.query.get(job_id)
    if not job:
        return jsonify({"error": "job not found"}), 404

    appn = Application(candidate_name=name, candidate_email=email, job_id=job_id, status="applied")
    db.session.add(appn)
    db.session.commit()

    # send background notification (mock)
    send_application_update(email, "applied")

    return jsonify({"message": "application created", "application": {"id": appn.id, "status": appn.status}}), 201

@application_bp.route("/<int:app_id>", methods=["GET"])
def get_application(app_id):
    appn = Application.query.get(app_id)
    if not appn:
        return jsonify({"error": "application not found"}), 404
    return jsonify({
        "id": appn.id,
        "candidate_name": appn.candidate_name,
        "candidate_email": appn.candidate_email,
        "job_id": appn.job_id,
        "status": appn.status,
        "created_at": appn.created_at.isoformat()
    }), 200

@application_bp.route("/<int:app_id>/transition", methods=["POST"])
def transition(app_id):
    """
    Transition application state.
    JSON: { "to_state": "screening" }
    Allowed transitions handled by state_machine.
    """
    appn = Application.query.get(app_id)
    if not appn:
        return jsonify({"error": "application not found"}), 404

    data = request.get_json() or {}
    to_state = data.get("to_state")
    if not to_state:
        return jsonify({"error": "to_state required"}), 400

    machine = ApplicationStateMachine(appn.status)
    ok, message = machine.transition(to_state)
    if not ok:
        return jsonify({"error": message}), 400

    # persist new state
    appn.status = to_state
    db.session.commit()

    # send background notification (mock)
    send_application_update(appn.candidate_email, to_state)

    return jsonify({"message": "transitioned", "application": {"id": appn.id, "status": appn.status}}), 200
