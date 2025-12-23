from functools import wraps
from flask import request, jsonify
from app.models import User

def require_role(required_role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user_id = request.headers.get("X-User-Id")

            if not user_id:
                return jsonify({"error": "User ID required"}), 401

            user = User.query.get(user_id)
            if not user:
                return jsonify({"error": "Invalid user"}), 401

            if user.role != required_role:
                return jsonify({"error": "Forbidden"}), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator
