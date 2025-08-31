from flask import Blueprint, request, jsonify
from ..services.learning_algorithm_service import learning_algorithm_service
import json

learning_algorithm_bp = Blueprint('learning_algorithm', __name__)

@learning_algorithm_bp.route('/learning-status', methods=['GET'])
def get_learning_status():
    """Get current learning algorithm status"""
    try:
        return jsonify({
            'success': True,
            'status': 'active',
            'data_points': len(learning_algorithm_service.performance_history),
            'insights_available': bool(learning_algorithm_service.learning_insights),
            'message': 'Learning algorithm is running'
        })
    except Exception as e:
        return jsonify({'error': f'Failed to get learning status: {str(e)}'}), 500

@learning_algorithm_bp.route("/upload-performance-data", methods=["POST"])
def upload_performance_data():
    """Manually upload performance data for posts"""
    try:
        data = request.get_json() or {}
        posts = data.get("posts")
        
        if not posts or not isinstance(posts, list):
            return jsonify({"error": "'posts' field with a list of post data is required"}), 400
        
        # Update the performance data
        learning_algorithm_service.update_performance_history(posts)
        
        return jsonify({
            "success": True,
            "message": f"Successfully uploaded and processed {len(posts)} posts."
        })
        
    except Exception as e:
        return jsonify({"error": f"Failed to upload performance data: {str(e)}"}), 500

@learning_algorithm_bp.route('/analyze-patterns', methods=['POST'])
def analyze_performance_patterns():
    """Analyze performance patterns and generate insights"""
    try:
        # Add input validation
        data = request.get_json() or {}
        
        # Check if we have enough data for analysis
        if len(learning_algorithm_service.performance_history) < 3:
            return jsonify({
                'error': 'Insufficient data for pattern analysis',
                'message': 'Need at least 3 posts for pattern analysis. Please fetch more performance data first.',
                'current_data_points': len(learning_algorithm_service.performance_history)
            }), 400
        
        insights = learning_algorithm_service.analyze_performance_patterns()
        
        # Better error handling for service response
        if isinstance(insights, dict) and 'error' in insights:
            return jsonify(insights), 400
        
        return jsonify({
            'success': True,
            'insights': insights,
            'data_points': len(learning_algorithm_service.performance_history),
            'message': 'Performance patterns analyzed successfully'
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to analyze patterns: {str(e)}'}), 500

@learning_algorithm_bp.route('/insights', methods=['GET'])
def get_learning_insights():
    """Get current learning insights and recommendations"""
    try:
        insights = learning_algorithm_service.learning_insights
        
        if not insights:
            return jsonify({
                'success': False,
                'error': 'No insights available yet',
                'recommendation': 'Upload more content or fetch performance data first'
            }), 400
        
        return jsonify({
            'success': True,
            'insights': insights,
            'last_updated': insights.get('last_updated'),
            'data_points': len(learning_algorithm_service.performance_history)
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get insights: {str(e)}'}), 500

@learning_algorithm_bp.route('/performance-history', methods=['GET'])
def get_performance_history():
    """Get performance history data"""
    try:
        limit = request.args.get('limit', 50, type=int)
        platform = request.args.get('platform')
        
        history = learning_algorithm_service.performance_history
        
        # Filter by platform if specified
        if platform:
            history = [post for post in history if post.get('platform') == platform]
        
        # Limit results
        history = history[-limit:] if limit else history
        
        # Calculate summary statistics
        if history:
            engagement_rates = [post.get('engagement_rate', 0) for post in history]
            total_engagements = [post.get('total_engagement', 0) for post in history]
            
            summary_stats = {
                'avg_engagement_rate': sum(engagement_rates) / len(engagement_rates),
                'max_engagement_rate': max(engagement_rates),
                'min_engagement_rate': min(engagement_rates),
                'avg_total_engagement': sum(total_engagements) / len(total_engagements),
                'total_posts': len(history)
            }
        else:
            summary_stats = {}
        
        return jsonify({
            'success': True,
            'history': history,
            'summary_stats': summary_stats,
            'total_available': len(learning_algorithm_service.performance_history)
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve performance history: {str(e)}'}), 500

@learning_algorithm_bp.route('/optimal-timing', methods=['GET'])
def get_optimal_timing():
    """Get optimal posting timing recommendations"""
    try:
        platform = request.args.get('platform', 'instagram')
        
        # Check if we have enough data
        if len(learning_algorithm_service.performance_history) < 5:
            return jsonify({
                'success': True,
                'optimal_timing': {
                    'best_hours': ['9:00', '12:00', '17:00'],
                    'best_days': ['Tuesday', 'Wednesday', 'Thursday'],
                    'detailed_analysis': {
                        'note': 'Default recommendations - need more data for personalized insights'
                    }
                },
                'platform': platform,
                'confidence': 'low',
                'message': 'Using default timing recommendations. Upload more content for personalized insights.'
            })
        
        insights = learning_algorithm_service.learning_insights
        timing_data = insights.get('optimal_posting_times', {})
        
        if not timing_data:
            # Generate basic timing recommendations
            timing_data = {
                'best_hours': [9, 12, 17],
                'best_days': [1, 2, 3],
                'detailed_analysis': {
                    'note': 'Basic recommendations based on general best practices'
                }
            }
        
        # Convert hour numbers to readable format
        best_hours = timing_data.get('best_hours', [9, 12, 17])
        best_days = timing_data.get('best_days', [1, 2, 3])
        
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        readable_timing = {
            'best_hours': [f"{hour}:00" for hour in best_hours],
            'best_days': [day_names[day] for day in best_days if 0 <= day < len(day_names)],
            'detailed_analysis': timing_data.get('detailed_analysis', {})
        }
        
        return jsonify({
            'success': True,
            'optimal_timing': readable_timing,
            'platform': platform,
            'confidence': 'high' if len(learning_algorithm_service.performance_history) > 30 else 'medium'
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get optimal timing: {str(e)}'}), 500

@learning_algorithm_bp.route('/hashtag-analysis', methods=['GET'])
def get_hashtag_analysis():
    """Get hashtag effectiveness analysis"""
    try:
        insights = learning_algorithm_service.learning_insights
        hashtag_data = insights.get('hashtag_effectiveness', {})
        
        if not hashtag_data:
            return jsonify({
                'success': True,
                'hashtag_analysis': {
                    'top_hashtags': [],
                    'recommendations': ['#RealEstate', '#WindsorEssex', '#DreamHome', '#PropertyListing', '#HomeBuying'],
                    'note': 'Default recommendations - need more posts with hashtags for personalized analysis'
                },
                'message': 'Using default hashtag recommendations. Upload more content for personalized insights.'
            })
        
        top_hashtags = hashtag_data.get('top_performing_hashtags', {})
        
        # Format for better readability
        formatted_hashtags = []
        for hashtag, data in list(top_hashtags.items())[:15]:
            formatted_hashtags.append({
                'hashtag': hashtag,
                'avg_engagement': data.get('avg_engagement', 0),
                'usage_count': data.get('usage_count', 0),
                'effectiveness_score': data.get('effectiveness_score', 0)
            })
        
        return jsonify({
            'success': True,
            'hashtag_analysis': {
                'top_hashtags': formatted_hashtags,
                'total_analyzed': len(top_hashtags),
                'recommendations': hashtag_data.get('recommendations', [])
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get hashtag analysis: {str(e)}'}), 500

@learning_algorithm_bp.route('/content-optimization', methods=['GET'])
def get_content_optimization():
    """Get content optimization recommendations"""
    try:
        insights = learning_algorithm_service.learning_insights
        
        # Provide default recommendations if no insights available
        if not insights or not insights.get('best_performing_content_types'):
            return jsonify({
                'success': True,
                'optimization_tips': {
                    'content_types': ['Educational posts', 'Behind-the-scenes', 'Customer testimonials'],
                    'posting_frequency': 'Daily posting recommended',
                    'engagement_tactics': ['Ask questions', 'Use polls', 'Share stories'],
                    'visual_recommendations': ['High-quality images', 'Consistent branding', 'Video content']
                },
                'message': 'Using default optimization recommendations. Upload more content for personalized insights.'
            })
        
        # Extract optimization insights
        content_types = insights.get('best_performing_content_types', {})
        timing_data = insights.get('optimal_posting_times', {})
        hashtag_data = insights.get('hashtag_effectiveness', {})
        
        optimization_tips = {
            'top_content_types': list(content_types.keys())[:5] if content_types else [],
            'best_posting_times': timing_data.get('best_hours', []),
            'effective_hashtags': list(hashtag_data.get('top_performing_hashtags', {}).keys())[:10],
            'engagement_patterns': insights.get('high_engagement_patterns', {}),
            'recommendations': [
                'Focus on your top-performing content types',
                'Post during your optimal time windows',
                'Use your most effective hashtags',
                'Maintain consistent posting schedule'
            ]
        }
        
        return jsonify({
            'success': True,
            'optimization_tips': optimization_tips,
            'data_points': len(learning_algorithm_service.performance_history)
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get content optimization: {str(e)}'}), 500

@learning_algorithm_bp.route('/content-recommendations', methods=['GET'])
def get_content_recommendations():
    """Get AI-powered content recommendations"""
    try:
        content_type = request.args.get('type', 'general')
        platform = request.args.get('platform', 'instagram')
        
        recommendations = learning_algorithm_service.generate_content_recommendations(content_type, platform)
        
        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'content_type': content_type,
            'platform': platform
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get content recommendations: {str(e)}'}), 500

@learning_algorithm_bp.route('/update-performance', methods=['POST'])
def update_performance_manually():
    """Manually update performance data for posts"""
    try:
        data = request.get_json() or {}
        post_id = data.get('post_id')
        performance_data = data.get('performance_data', {})
        
        if not post_id or not performance_data:
            return jsonify({'error': 'Post ID and performance data are required'}), 400
        
        # Update the performance data
        success = learning_algorithm_service.update_post_performance(post_id, performance_data)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Performance data updated successfully',
                'post_id': post_id
            })
        else:
            return jsonify({'error': 'Failed to update performance data'}), 400
        
    except Exception as e:
        return jsonify({'error': f'Failed to update performance: {str(e)}'}), 500

@learning_algorithm_bp.route('/reset-data', methods=['POST'])
def reset_learning_data():
    """Reset all learning algorithm data"""
    try:
        learning_algorithm_service.reset_data()
        
        return jsonify({
            'success': True,
            'message': 'All learning algorithm data has been reset'
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to reset data: {str(e)}'}), 500

