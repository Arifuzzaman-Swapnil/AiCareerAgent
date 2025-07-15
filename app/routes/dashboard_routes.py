from flask import Blueprint, session, redirect, render_template
from ..firebase_config import db

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")

    user_id = session["user_id"]
    doc = db.collection("users").document(user_id).get()
    data = doc.to_dict() or {}

    context = {
        "labels": ["Resume Feedback Score", "Interview MCQ Score", "Career Match %"],
        "feedback_score": data.get("feedback_score", 0),
        "mcq_score": data.get("mcq_score", 0),
        "mcq_total": data.get("mcq_total", 0),
        "career_match": data.get("career_match_percent", 0),
        "career_suggestions": data.get("career_suggestions", "No suggestions yet."),
        "resume_summary": data.get("resume_summary", "No summary uploaded yet."),
        "resume_feedback": data.get("resume_feedback", "No feedback yet."),
    }

    return render_template("dashboard.html", **context)