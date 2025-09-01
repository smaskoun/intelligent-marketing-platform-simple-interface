# main.py

from flask import Flask, send_from_directory, render_template
from flask_cors import CORS
import os

# Import the database object and all the API blueprints
from models.social_media import db
from routes.brand_voice_routes import brand_voice_bp
from routes.learning_algorithm_routes import learning_algorithm_bp
from routes.ab_testing_routes import ab_testing_bp
from routes.market_data_routes import market_data_bp

# --- App Configuration ---
app = Flask(__name__,
            static_folder='static',
            template_folder='static') # Serve HTML from the 'static' folder

# Configure CORS to allow requests from the frontend
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configure the database URI. Use Render's DATABASE_URL environment variable.
# Provide a local fallback for development.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///local_dev.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the Flask app
db.init_app(app)

# --- API Blueprint Registration ---
# Register all the different parts of our API
app.register_blueprint(brand_voice_bp, url_prefix='/api/brand-voice')
app.register_blueprint(learning_algorithm_bp, url_prefix='/api/learning')
app.register_blueprint(ab_testing_bp, url_prefix='/api/ab-testing')
app.register_blueprint(market_data_bp, url_prefix='/api/market-data')

# --- Route to Serve the Frontend ---
# This route will serve the main HTML page of your application.
@app.route('/')
def serve_index():
    # We use render_template to correctly serve the HTML file
    return render_template('social-media-automation.html')

# --- Create Database Tables ---
# This block ensures that the database tables are created if they don't exist.
with app.app_context():
    db.create_all()

# --- Main Entry Point for Gunicorn ---
if __name__ == '__main__':
    # This part is for local development, not for Render.
    app.run(debug=True, port=5001)

