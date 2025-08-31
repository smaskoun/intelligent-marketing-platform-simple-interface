# main.py

import os
from flask import Flask, send_from_directory
from flask_cors import CORS

# --- CORRECTED IMPORTS ---
from models.social_media import db
from routes.brand_voice import brand_voice_bp  # This file now exists
from routes.learning_algorithm_routes import learning_algorithm_bp
from routes.ab_testing_routes import ab_testing_bp
from routes.market_data_routes import market_data_bp
# -------------------------

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'a_very_secret_key_that_should_be_changed'
    
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database', 'app.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    CORS(app, origins="*")

    app.register_blueprint(brand_voice_bp, url_prefix='/api/brand-voice')
    app.register_blueprint(learning_algorithm_bp, url_prefix='/api/learning')
    app.register_blueprint(ab_testing_bp, url_prefix='/api/ab-testing')
    app.register_blueprint(market_data_bp, url_prefix='/api/market-data')

    with app.app_context():
        db.create_all()

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'social-media-automation.html')

    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)
