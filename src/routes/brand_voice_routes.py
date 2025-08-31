from flask import Blueprint, request, jsonify
from ..services.brand_voice_service import brand_voice_service
import json

brand_voice_bp = Blueprint('brand_voice', __name__)

@brand_voice_bp.route('/analyze-posts', methods=['POST'])
def analyze_posts():
    """Analyze user's social media posts to learn their brand voice"""
    try:
        data = request.get_json() or {}
        
        # Check if this is a manual content analysis request
        if 'posts' in data:
            posts = data.get('posts', [])
            if not posts:
                return jsonify({'error': 'No posts provided for analysis'}), 400
            
            # Analyze the provided posts
            analysis = brand_voice_service.analyze_writing_style(posts)
            voice_profile = brand_voice_service.create_brand_voice_profile(analysis)
            
            return jsonify({
                'success': True,
                'posts_analyzed': len(posts),
                'analysis': analysis,
                'voice_profile': voice_profile,
                'message': f'Successfully analyzed {len(posts)} posts'
            })
        
        # Original token-based analysis
        access_token = data.get('access_token')
        platform = data.get('platform', 'facebook')
        limit = data.get('limit', 50)
        
        if not access_token:
            return jsonify({'error': 'Access token or posts data is required'}), 400
        
        # Fetch user's posts
        posts = brand_voice_service.fetch_user_posts(access_token, platform, limit)
        
        if not posts:
            return jsonify({'error': 'No posts found or unable to fetch posts'}), 404
        
        # Analyze writing style
        analysis = brand_voice_service.analyze_writing_style(posts)
        
        # Create brand voice profile
        voice_profile = brand_voice_service.create_brand_voice_profile(analysis)
        
        return jsonify({
            'success': True,
            'posts_analyzed': len(posts),
            'analysis': analysis,
            'voice_profile': voice_profile,
            'message': f'Successfully analyzed {len(posts)} posts from {platform}'
        })
        
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@brand_voice_bp.route('/upload-content', methods=['POST'])
def upload_content_for_analysis():
    """Upload text content for brand voice analysis"""
    try:
        data = request.get_json() or {}
        content_text = data.get('content')
        
        if not content_text:
            return jsonify({'error': 'Content text is required'}), 400
        
        # Convert single content to list format for analysis
        posts = [{'text': content_text}]
        
        # Analyze writing style
        analysis = brand_voice_service.analyze_writing_style(posts)
        
        # Create brand voice profile
        voice_profile = brand_voice_service.create_brand_voice_profile(analysis)
        
        return jsonify({
            'success': True,
            'content_analyzed': True,
            'analysis': analysis,
            'voice_profile': voice_profile,
            'message': 'Content uploaded and analyzed successfully'
        })
        
    except Exception as e:
        return jsonify({'error': f'Content analysis failed: {str(e)}'}), 500

@brand_voice_bp.route('/voice-profile', methods=['GET'])
def get_voice_profile():
    """Get current brand voice profile"""
    try:
        profile = brand_voice_service.get_current_voice_profile()
        
        if not profile:
            # Return a default/sample profile instead of 404
            default_profile = {
                'tone': 'Professional and approachable',
                'style': 'Informative with personal touch',
                'vocabulary': 'Industry-specific but accessible',
                'personality_traits': ['Knowledgeable', 'Trustworthy', 'Helpful'],
                'sample_phrases': ['Let me help you understand...', 'Based on my experience...', 'I recommend...'],
                'last_updated': None,
                'status': 'default',
                'message': 'This is a default profile. Upload content or analyze posts to create a personalized voice profile.'
            }
            
            return jsonify({
                'success': True,
                'voice_profile': default_profile,
                'is_default': True,
                'message': 'Using default voice profile. Upload content or analyze posts for personalized insights.'
            })
        
        return jsonify({
            'success': True,
            'voice_profile': profile,
            'is_default': False,
            'last_updated': profile.get('last_updated')
        })
        
    except Exception as e:
        # Better error handling for 500 errors
        error_message = f'Failed to get voice profile: {str(e)}'
        
        # Return a safe fallback response instead of 500
        return jsonify({
            'success': False,
            'error': 'Service temporarily unavailable',
            'message': 'Unable to retrieve voice profile at this time. Please try again later.',
            'debug_info': error_message
        }), 500

@brand_voice_bp.route('/generate-content', methods=['POST'])
def generate_content_with_voice():
    """Generate content using the learned brand voice"""
    try:
        data = request.get_json() or {}
        topic = data.get('topic')
        content_type = data.get('content_type', 'social_post')
        platform = data.get('platform', 'instagram')
        
        if not topic:
            return jsonify({'error': 'Topic is required'}), 400
        
        # Get current voice profile
        voice_profile = brand_voice_service.get_current_voice_profile()
        
        if not voice_profile:
            return jsonify({'error': 'No voice profile available. Analyze posts first.'}), 400
        
        # Generate content
        generated_content = brand_voice_service.generate_content_with_voice(
            topic, content_type, platform, voice_profile
        )
        
        return jsonify({
            'success': True,
            'generated_content': generated_content,
            'topic': topic,
            'content_type': content_type,
            'platform': platform
        })
        
    except Exception as e:
        return jsonify({'error': f'Content generation failed: {str(e)}'}), 500

@brand_voice_bp.route('/sample-analysis', methods=['GET'])
def get_sample_analysis():
    """Get a sample brand voice analysis for demonstration"""
    try:
        sample_analysis = {
            'writing_style': {
                'tone': 'Professional yet approachable',
                'formality_level': 'Semi-formal',
                'sentence_structure': 'Varied with emphasis on clarity',
                'vocabulary_complexity': 'Accessible professional language'
            },
            'brand_characteristics': {
                'personality_traits': ['Knowledgeable', 'Trustworthy', 'Helpful'],
                'communication_style': 'Direct and informative',
                'emotional_tone': 'Confident and reassuring'
            },
            'content_patterns': {
                'common_themes': ['Market insights', 'Home buying tips', 'Local expertise'],
                'call_to_action_style': 'Encouraging and supportive',
                'hashtag_usage': 'Strategic and relevant'
            },
            'recommendations': [
                'Maintain professional expertise while staying approachable',
                'Continue using market data to support claims',
                'Keep calls-to-action clear and helpful'
            ]
        }
        
        return jsonify({
            'success': True,
            'sample_analysis': sample_analysis,
            'message': 'This is a sample analysis. Upload your content for personalized insights.'
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get sample analysis: {str(e)}'}), 500

@brand_voice_bp.route('/reset-profile', methods=['POST'])
def reset_voice_profile():
    """Reset the current brand voice profile"""
    try:
        brand_voice_service.reset_voice_profile()
        
        return jsonify({
            'success': True,
            'message': 'Brand voice profile has been reset'
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to reset profile: {str(e)}'}), 500

@brand_voice_bp.route('/training-status', methods=['GET'])
def get_training_status():
    """Get the current training status of the brand voice model"""
    try:
        status = brand_voice_service.get_training_status()
        
        return jsonify({
            'success': True,
            'training_status': status
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get training status: {str(e)}'}), 500

