from flask import Blueprint, request, jsonify

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Simple registration endpoint.
    Expected JSON: { "email": "...", "role": "candidate" }
    """
    data = request.get_json() or {}
    email = data.get("email")
    role = data.get("role", "candidate")
    if not email:
        return jsonify({"error": "email required"}), 400

    # For this project we do not store passwords; we create a minimal user record.
    from app import db
    from app.models import User
    existing = User.query.filter_by(email=email).first()
    if existing:
        return jsonify({"message": "user already exists", "id": existing.id}), 200

    user = User(email=email, role=role)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "user registered", "id": user.id}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Simple login stub: expects { "email": "..." }.
    Returns user id and role in response for client to use.
    """
    data = request.get_json() or {}
    email = data.get("email")
    if not email:
        return jsonify({"error": "email required"}), 400

    from app.models import User
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "user not found"}), 404

    # No JWT in this minimal project — return basic info
    return jsonify({"message": "login success", "user": {"id": user.id, "email": user.email, "role": user.role}}), 200
