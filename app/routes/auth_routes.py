from flask import Blueprint, request, session, redirect, render_template
import firebase_admin.auth as auth
from app import firebase_config  # শুধু import করলেই initialize হয়ে যাবে

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/")
def home():
    return render_template("login.html")

@auth_bp.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    id_token = data.get("idToken")
    try:
        decoded_token = auth.verify_id_token(id_token)
        user_id = decoded_token["uid"]
        session["user_id"] = user_id
        return "", 200
    except Exception as e:
        return {"error": str(e)}, 401

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")
