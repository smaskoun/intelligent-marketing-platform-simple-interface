# routes/brand_voice.py

from flask import Blueprint, request, jsonify
from services.brand_voice_service import brand_voice_service

brand_voice_bp = Blueprint('brand_voice', __name__)

@brand_voice_bp.route('/train', methods=['POST'])
def train_brand_voice():
    """Endpoint to receive training data from the user."""
    data = request.get_json()
    if not data or 'content' not in data or 'post_type' not in data:
        return jsonify({"success": False, "error": "Missing required fields: content, post_type"}), 400

    try:
        training_data = brand_voice_service.add_training_data(
            user_id=data.get('user_id', 'default_user'),
            content=data['content'],
            image_url=data.get('image_url'),
            post_type=data['post_type']
        )
        return jsonify({"success": True, "message": "Training data added successfully.", "data_id": training_data.id})
    except Exception as e:
        # A real app would have more specific error handling and logging
        return jsonify({"success": False, "error": f"An unexpected error occurred: {str(e)}"}), 500
