# routes/ab_testing_routes.py

from flask import Blueprint, request, jsonify
# --- CORRECTED IMPORTS ---
from services.ab_testing_service import ab_testing_service
from services.learning_algorithm_service import learning_algorithm_service
# -------------------------
import json

ab_testing_bp = Blueprint('ab_testing', __name__)

@ab_testing_bp.route('/create-test', methods=['POST'])
def create_ab_test():
    """Create a new A/B test based on a content recommendation"""
    try:
        data = request.get_json()
        if not data or 'base_content' not in data:
            return jsonify({'success': False, 'error': 'Missing base_content in request'}), 400

        base_content = data['base_content']
        test_name = data.get('test_name', f"A/B Test for '{base_content.get('focus', 'content')}'")
        platform = data.get('platform', 'instagram')
        
        # The base_content dictionary now comes directly from the frontend,
        # passed from the content generator.
        
        ab_test = ab_testing_service.create_ab_test(
            test_name=test_name,
            base_content=base_content,
            variation_types=['hooks', 'cta_styles'], # Default variation types
            platform=platform
        )
        
        # Convert to dict for JSON serialization
        test_data = {
            'id': ab_test.id,
            'name': ab_test.name,
            'status': ab_test.status,
            'variations': [
                {
                    'id': var.id,
                    'content': var.content,
                    'hashtags': var.hashtags
                }
                for var in ab_test.variations
            ]
        }
        
        return jsonify({
            'success': True,
            'test': test_data,
            'message': f'A/B test created with {len(ab_test.variations)} variations'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': f'Failed to create A/B test: {str(e)}'}), 500

@ab_testing_bp.route('/analyze-results/<test_id>', methods=['GET'])
def analyze_results(test_id):
    """
    In our new system, this route's primary job is to return the variations
    for manual posting, as the automatic performance tracking is not implemented.
    """
    try:
        test = ab_testing_service.active_tests.get(test_id)
        if not test:
            return jsonify({"success": False, "error": "Test not found"}), 404

        # Prepare the data in the format the frontend expects
        response_data = {
            "test_id": test.id,
            "test_name": test.name,
            "status": "ready_for_manual_testing",
            "message": "Content variations are ready for manual posting and testing.",
            "variations": [
                {
                    "version": f"Variation {chr(65 + i)}", # A, B, C...
                    "content": var.content,
                    "focus": f"Test variation focusing on {var.id}"
                }
                for i, var in enumerate(test.variations)
            ],
            "instructions": [
                "1. Post each variation to your social media accounts.",
                "2. Post them at different times or days for fair testing.", 
                "3. Track engagement (likes, comments, shares) for each version.",
                "4. Note which version performs best.",
                "5. Use the winning elements in future content."
            ]
        }
        
        return jsonify({
            "success": True,
            "data": response_data
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error retrieving test results: {str(e)}"
        }), 500

# Note: The other routes like /start-test, /update-performance, etc., are
# kept for future enhancements but are not used by the current frontend.
# They can be left as they are for now.

@ab_testing_bp.route('/tests', methods=['GET'])
def get_all_tests():
    """Get all A/B tests"""
    try:
        tests = ab_testing_service.get_all_tests()
        return jsonify({'success': True, 'tests': tests})
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve tests: {str(e)}'}), 500

@ab_testing_bp.route('/test/<test_id>', methods=['DELETE'])
def delete_test(test_id):
    """Delete an A/B test"""
    try:
        success = ab_testing_service.delete_test(test_id)
        if success:
            return jsonify({'success': True, 'message': f'Test {test_id} deleted successfully'})
        else:
            return jsonify({'error': 'Test not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Failed to delete test: {str(e)}'}), 500

