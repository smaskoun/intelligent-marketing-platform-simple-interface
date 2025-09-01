# main.py
"""
Application entry point.

This module provides a factory function `create_app()` used by Gunicorn
and the Flask CLI to create and configure the Flask application.  It
sets up the database, CORS, registers blueprints and serves the static
frontend.
"""

import os
from flask import Flask, send_from_directory
from flask_cors import CORS

# Import the shared database instance
from models import db

# --- THIS IS THE FIX ---
# Correctly import the blueprints from their respective files.
# The original code had a typo, importing from 'routes.brand_voice_routes'
# which should have been 'routes.brand_voice'.
from routes.brand_voice import brand_voice_bp
from routes.learning_algorithm_routes import learning_algorithm_bp
from routes.ab_testing_routes import ab_testing_bp
from routes.market_data_routes import market_data_bp
# ---------------------


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__, static_folder='static', template_folder='static')

    # --- Configuration ---
    db_url = os.environ.get('DATABASE_URL', 'sqlite:///local_dev.db')
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    CORS(app)

    # --- Initialize Database ---
    db.init_app(app)

    # --- Register Blueprints ---
    app.register_blueprint(brand_voice_bp, url_prefix="/api/brand-voice")
    app.register_blueprint(learning_algorithm_bp, url_prefix="/api/learning")
    app.register_blueprint(ab_testing_bp, url_prefix="/api/ab-testing")
    app.register_blueprint(market_data_bp, url_prefix="/api/market-data")

    # --- Frontend Serving Route ---
    # This route serves the self-contained HTML file.
    @app.route('/')
    def serve_app():
        return send_from_directory(app.static_folder, 'social-media-automation.html')

    # --- Create Database Tables ---
    with app.app_context():
        db.create_all()

    return app


# This part is for local development and can be ignored by Gunicorn
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
