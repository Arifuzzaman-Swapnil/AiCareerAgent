from flask import Blueprint, session, jsonify
from ..firebase_config import db

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/api")


@dashboard_bp.route("/dashboard", methods=["GET"])
def dashboard():
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401

    user_id = session["user_id"]
    doc = db.collection("users").document(user_id).get()
    data = doc.to_dict() or {}

    return jsonify({
        "success": True,
        "data": {
            "feedback_score": data.get("feedback_score", 0),
            "mcq_score": data.get("mcq_score", 0),
            "mcq_total": data.get("mcq_total", 0),
            "career_match": data.get("career_match_percent", 0),
            "career_suggestions": data.get("career_suggestions", ""),
            "resume_summary": data.get("resume_summary", ""),
            "resume_feedback": data.get("resume_feedback", ""),
            "display_name": data.get("displayName", ""),
        }
    })
