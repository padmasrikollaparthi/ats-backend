from flask import Blueprint, request, jsonify
from app import db
from app.models import Application, Job, ApplicationHistory
from app.services.state_machine import ApplicationStateMachine
from app.services.email_service import send_application_update
from app.services.authz import require_role

application_bp = Blueprint("applications", __name__)

@application_bp.route("/", methods=["POST"])
def create_application():
    data = request.get_json() or {}

    name = data.get("candidate_name")
    email = data.get("candidate_email")
    job_id = data.get("job_id")

    if not name or not email or not job_id:
        return jsonify({"error": "candidate_name, candidate_email, job_id required"}), 400

    job = Job.query.get(job_id)
    if not job:
        return jsonify({"error": "job not found"}), 404

    appn = Application(
        candidate_name=name,
        candidate_email=email,
        job_id=job_id,
        status="applied"
    )

    db.session.add(appn)
    db.session.commit()

    send_application_update(email, "applied")

    return jsonify({
        "id": appn.id,
        "status": appn.status
    }), 201


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
@require_role("recruiter")
def transition(app_id):
    appn = Application.query.get(app_id)
    if not appn:
        return jsonify({"error": "application not found"}), 404

    data = request.get_json() or {}
    new_state = data.get("to_state")

    if not new_state:
        return jsonify({"error": "to_state required"}), 400

    machine = ApplicationStateMachine(appn.status)
    ok, message = machine.transition(new_state)
    if not ok:
        return jsonify({"error": message}), 400

    old_state = appn.status
    appn.status = new_state

    history = ApplicationHistory(
        application_id=appn.id,
        from_state=old_state,
        to_state=new_state
    )

    db.session.add(history)
    db.session.commit()

    send_application_update(appn.candidate_email, new_state)

    return jsonify({
        "message": "transitioned",
        "from": old_state,
        "to": new_state
    }), 200


@application_bp.route("/<int:app_id>/history", methods=["GET"])
def get_history(app_id):
    history = ApplicationHistory.query.filter_by(application_id=app_id).all()

    return jsonify([
        {
            "from": h.from_state,
            "to": h.to_state,
            "at": h.changed_at.isoformat()
        } for h in history
    ]), 200
