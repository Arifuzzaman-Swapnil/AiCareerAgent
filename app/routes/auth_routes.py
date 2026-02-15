from flask import Blueprint, request, session, jsonify
import firebase_admin.auth as auth
from app import firebase_config

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    id_token = data.get("idToken")
    try:
        decoded_token = auth.verify_id_token(id_token)
        user_id = decoded_token["uid"]
        session["user_id"] = user_id
        return jsonify({"success": True, "user_id": user_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"success": True}), 200


@auth_bp.route("/status", methods=["GET"])
def auth_status():
    if "user_id" in session:
        return jsonify({"authenticated": True, "user_id": session["user_id"]}), 200
    return jsonify({"authenticated": False}), 200
