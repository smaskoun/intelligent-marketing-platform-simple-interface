# src/main.py

import os
from flask import Flask, send_from_directory
from flask_cors import CORS

# --- CORRECTED IMPORTS ---
# We use a single dot (.) to tell Python to import from the current package (the 'src' folder).
from .models.social_media import db
from .routes.brand_voice import brand_voice_bp
from .routes.learning_algorithm_routes import learning_algorithm_bp
from .routes.ab_testing_routes import ab_testing_bp
from .routes.market_data_routes import market_data_bp
# -------------------------

def create_app():
    """Application Factory Pattern"""
    app = Flask(__name__, static_folder='static')
    app.config['SECRET_KEY'] = 'a_very_secret_key_that_should_be_changed'
    
    # Configure the database URI
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database', 'app.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True) # Ensure the database directory exists
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    CORS(app, origins="*")

    # Register blueprints
    app.register_blueprint(brand_voice_bp, url_prefix='/api/brand-voice')
    app.register_blueprint(learning_algorithm_bp, url_prefix='/api/learning')
    app.register_blueprint(ab_testing_bp, url_prefix='/api/ab-testing')
    app.register_blueprint(market_data_bp, url_prefix='/api/market-data')

    with app.app_context():
        # Create database tables if they don't exist
        db.create_all()

    # --- Static File Serving ---
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'social-media-automation.html')

    return app

# This part runs when you execute the script directly
if __name__ == '__main__':
    app = create_app()
    # Use the PORT environment variable provided by Render, default to 5001 for local dev
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)
