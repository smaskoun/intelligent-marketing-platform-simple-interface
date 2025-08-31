import os
import sys
# This line is important for your project's structure, so we keep it.
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS

# --- 1. UPDATED MODEL IMPORT ---
# We now import the 'db' object from our new, clean models file.
from src.models.social_media import db

# --- 2. UPDATED BLUEPRINT IMPORTS ---
# We only import the blueprints that are part of our new, refactored application.
# For now, that is just the brand_voice blueprint. We will add the A/B testing one later.
from src.routes.brand_voice import brand_voice_bp
# We will also keep the market_data_routes for now as it seems independent.
from src.routes.market_data_routes import market_data_bp


# --- Application Factory Pattern ---
# It's best practice to create the app inside a function.
def create_app():
    """Creates and configures the Flask application."""
    
    app = Flask(__name__, static_folder='static')
    app.config['SECRET_KEY'] = 'a-new-secret-key-is-better' # It's good practice to change default keys.

    # Enable CORS for all routes
    CORS(app)

    # --- Database Configuration ---
    # This path is corrected to work from within the 'src' directory.
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'app.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # --- 3. REGISTER CLEANED BLUEPRINTS ---
    # We only register the blueprints we are actively using.
    app.register_blueprint(brand_voice_bp) # From our new brand_voice.py
    app.register_blueprint(market_data_bp) # From your existing market_data_routes.py

    # --- 4. SIMPLIFIED ROUTE TO SERVE THE FRONTEND ---
    # This single route will serve your main HTML page.
    @app.route('/')
    def serve_index():
        return send_from_directory(app.static_folder, 'social-media-automation.html')

    # This block creates the database tables (e.g., 'training_data') if they don't exist.
    with app.app_context():
        db.create_all()
        
    return app

# --- Main execution block ---
if __name__ == '__main__':
    app = create_app()
    # Use port 5001 to avoid potential conflicts with other services like React dev server
    app.run(host='0.0.0.0', port=5001, debug=True)

