# routes/learning_algorithm_routes.py

from flask import Blueprint, request, jsonify
from services.learning_algorithm_service import learning_algorithm_service

learning_algorithm_bp = Blueprint('learning_algorithm', __name__)

@learning_algorithm_bp.route('/content-recommendations', methods=['GET'])
def get_content_recommendations():
    """
    This is the main endpoint for generating new content.
    """
    try:
        user_id = request.args.get('user_id', 'default_user')
        content_type = request.args.get('type', 'general')
        platform = request.args.get('platform', 'instagram')

        # --- THIS IS THE FIX ---
        # The service now returns the final dictionary directly.
        # We just need to return it as JSON.
        response_data = learning_algorithm_service.generate_content_recommendations(
            user_id=user_id,
            content_type=content_type,
            platform=platform
        )
        
        return jsonify(response_data)
        # ----------------------
        
    except Exception as e:
        print(f"Error in /content-recommendations endpoint: {e}")
        return jsonify({'success': False, 'error': f'Failed to get content recommendations: {str(e)}'}), 500
