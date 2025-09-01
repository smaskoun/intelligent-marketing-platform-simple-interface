# main.py

# --- THIS IS THE FINAL FIX ---
import sys
import os
# Add the project's root directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# ---------------------------

from flask import Flask, render_template
from flask_cors import CORS
from models.social_media import db
from routes.brand_voice_routes import brand_voice_bp
from routes.learning_algorithm_routes import learning_algorithm_bp
from routes.ab_testing_routes import ab_testing_bp
from routes.market_data_routes import market_data_bp

# --- App Creation ---
app = Flask(__name__,
            static_folder='static',
            template_folder='static')

# --- Configuration ---
# Fix for Render's PostgreSQL URL format
db_url = os.environ.get('DATABASE_URL', 'sqlite:///local_dev.db')
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app, resources={r"/api/*": {"origins": "*"}})

# --- Initialize Extensions ---
db.init_app(app)

# --- Register Blueprints ---
app.register_blueprint(brand_voice_bp, url_prefix='/api/brand-voice')
app.register_blueprint(learning_algorithm_bp, url_prefix='/api/learning')
app.register_blueprint(ab_testing_bp, url_prefix='/api/ab-testing')
app.register_blueprint(market_data_bp, url_prefix='/api/market-data')

# --- Main Route for Frontend ---
@app.route('/')
def serve_index():
    return render_template('social-media-automation.html')

# --- Create Database Tables ---
# This context is crucial for the app to know about the database
with app.app_context():
    db.create_all()

# --- Main Entry Point ---
if __name__ == '__main__':
    # For local development only
    app.run(debug=True, port=5001)

