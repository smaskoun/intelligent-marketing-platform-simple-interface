# routes/ab_testing_routes.py

from flask import Blueprint, request, jsonify
from services.ab_testing_service import ab_testing_service

ab_testing_bp = Blueprint('ab_testing', __name__)

# --- THIS IS THE FIX ---
# The original route was '/create-test'.
# The JavaScript is calling '/create'. We will make them match.
@ab_testing_bp.route('/create', methods=['POST'])
# ----------------------
def create_ab_test():
    """
    Creates a new A/B test with variations.
    """
    try:
        data = request.get_json()
        if not data or 'base_content' not in data:
            return jsonify({'success': False, 'error': 'Missing base_content in request.'}), 400

        test_name = data.get('test_name', 'New A/B Test')
        base_content = data['base_content']

        # Call the service to generate variations
        new_test = ab_testing_service.create_test_variations(test_name, base_content)

        return jsonify({'success': True, 'test': new_test})

    except Exception as e:
        print(f"Error in /create-test endpoint: {e}")
        return jsonify({'success': False, 'error': f'Failed to create A/B test: {str(e)}'}), 500

