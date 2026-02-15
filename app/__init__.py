from flask import Flask
from flask_cors import CORS
import os


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", "supersecretkey")

    # Enable CORS for React frontend
    CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

    # Import blueprints
    from .routes.auth_routes import auth_bp
    from .routes.dashboard_routes import dashboard_bp
    from .routes.ai_routes import ai_bp

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(ai_bp)

    return app
