# routes/market_data_routes.py

from flask import Blueprint, request, jsonify
# --- CORRECTED IMPORT ---
from services.wecar_market_service import wecar_market_service
# -------------------------

market_data_bp = Blueprint('market_data', __name__)

@market_data_bp.route('/current-stats', methods=['GET'])
def get_current_market_stats():
    """Get current Windsor-Essex market statistics from WECAR"""
    try:
        data = wecar_market_service.get_market_data()
        
        return jsonify({
            'success': True,
            'data': data,
            'source': 'WECAR - Windsor-Essex County Association of REALTORS',
            'message': 'Current market statistics retrieved successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch market data: {str(e)}',
            'message': 'Unable to retrieve current market statistics'
        }), 500

# Note: The other routes in this file are for potential future enhancements
# and can be left as they are. The main '/current-stats' route is the one
# used by our frontend.

@market_data_bp.route('/market-trends', methods=['GET'])
def get_market_trends():
    """Get market trends and historical data"""
    try:
        trends = wecar_market_service.get_historical_trends()
        current_data = wecar_market_service.get_market_data()
        
        return jsonify({
            'success': True,
            'trends': trends,
            'current_period': current_data.get('report_period', 'Current'),
            'insights': current_data.get('market_insights', {}),
            'source': 'WECAR - Windsor-Essex County Association of REALTORS',
            'message': 'Market trends retrieved successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch market trends: {str(e)}',
            'message': 'Unable to retrieve market trends'
        }), 500
