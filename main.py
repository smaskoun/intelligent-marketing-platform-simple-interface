# main.py

from flask import Flask, render_template
from flask_cors import CORS
import os

# Import the database object
from models.social_media import db

def create_app():
    """
    Application Factory Function: Creates and configures the Flask app.
    This is the function Gunicorn will call.
    """
    app = Flask(__name__,
                static_folder='static',
                template_folder='static')

    # --- Configuration ---
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///local_dev.db').replace("postgres://", "postgresql://")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # --- Initialize Extensions ---
    db.init_app(app)

    # --- Import and Register Blueprints ---
    # We import them *inside* the function to avoid circular imports
    from routes.brand_voice_routes import brand_voice_bp
    from routes.learning_algorithm_routes import learning_algorithm_bp
    from routes.ab_testing_routes import ab_testing_bp
    from routes.market_data_routes import market_data_bp

    app.register_blueprint(brand_voice_bp, url_prefix='/api/brand-voice')
    app.register_blueprint(learning_algorithm_bp, url_prefix='/api/learning')
    app.register_blueprint(ab_testing_bp, url_prefix='/api/ab-testing')
    app.register_blueprint(market_data_bp, url_prefix='/api/market-data')

    # --- Main Route for Frontend ---
    @app.route('/')
    def serve_index():
        return render_template('social-media-automation.html')

    # --- Create Database Tables ---
    with app.app_context():
        db.create_all()

    return app

# This allows Gunicorn to find the 'app' object if needed
app = create_app()

if __name__ == '__main__':
    # For local development only
    app.run(debug=True, port=5001)
