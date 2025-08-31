# routes/learning_algorithm_routes.py

from flask import Blueprint, request, jsonify
# --- CORRECTED IMPORT ---
from services.learning_algorithm_service import learning_algorithm_service
# -------------------------

# We keep the same blueprint name and prefix for consistency.
learning_algorithm_bp = Blueprint('learning_algorithm', __name__)

@learning_algorithm_bp.route('/content-recommendations', methods=['GET'])
def get_content_recommendations():
    """
    This is the main endpoint for generating new content.
    It takes a desired content type and platform as input.
    """
    try:
        # --- Get Parameters from the Request ---
        # We get the user ID, content type, and platform from the query parameters.
        # Example request: /api/learning/content-recommendations?type=listing&platform=instagram
        user_id = request.args.get('user_id', 'default_user') # Default user for now
        content_type = request.args.get('type', 'general')
        platform = request.args.get('platform', 'instagram')

        # --- Call the Service Layer ---
        # We pass the parameters to our new, simplified service to do the actual work.
        recommendations = learning_algorithm_service.generate_content_recommendations(
            user_id=user_id,
            content_type=content_type,
            platform=platform
        )
        
        # --- Return the Response ---
        # The recommendations from the service are returned to the frontend as JSON.
        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'content_type': content_type,
            'platform': platform
        })
        
    except Exception as e:
        # Basic error handling
        print(f"Error in /content-recommendations endpoint: {e}")
        return jsonify({'success': False, 'error': f'Failed to get content recommendations: {str(e)}'}), 500
