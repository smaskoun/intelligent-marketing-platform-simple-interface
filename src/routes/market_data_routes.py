from flask import Blueprint, request, jsonify
from ..services.wecar_market_service import wecar_market_service

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

@market_data_bp.route('/market-insights', methods=['GET'])
def get_market_insights():
    """Get detailed market insights and analysis"""
    try:
        data = wecar_market_service.get_market_data()
        insights = data.get('market_insights', {})
        
        # Enhanced insights
        enhanced_insights = {
            'market_summary': {
                'average_price': data.get('average_price', 0),
                'price_change': data.get('average_price_change', '0%'),
                'properties_sold': data.get('properties_sold', 0),
                'sales_change': data.get('properties_sold_change', '0%'),
                'new_listings': data.get('new_listings', 0),
                'listings_change': data.get('new_listings_change', '0%')
            },
            'market_conditions': insights,
            'recommendations': {
                'for_buyers': [],
                'for_sellers': []
            }
        }
        
        # Generate recommendations based on market conditions
        if insights.get('buyer_market'):
            enhanced_insights['recommendations']['for_buyers'] = [
                'Good time to buy with more inventory available',
                'Take advantage of increased negotiating power',
                'Consider multiple properties before making a decision'
            ]
            enhanced_insights['recommendations']['for_sellers'] = [
                'Price competitively to stand out',
                'Consider staging and professional photography',
                'Be prepared for longer time on market'
            ]
        elif insights.get('seller_market'):
            enhanced_insights['recommendations']['for_buyers'] = [
                'Act quickly on properties of interest',
                'Be prepared to make competitive offers',
                'Consider pre-approval for faster transactions'
            ]
            enhanced_insights['recommendations']['for_sellers'] = [
                'Great time to list with strong demand',
                'Price strategically to maximize return',
                'Expect faster sales and multiple offers'
            ]
        else:
            enhanced_insights['recommendations']['for_buyers'] = [
                'Balanced market provides good opportunities',
                'Take time to find the right property',
                'Negotiate fairly based on property condition'
            ]
            enhanced_insights['recommendations']['for_sellers'] = [
                'Price accurately based on recent comparables',
                'Ensure property is in good condition',
                'Market effectively to reach qualified buyers'
            ]
        
        return jsonify({
            'success': True,
            'insights': enhanced_insights,
            'report_period': data.get('report_period', 'Current'),
            'last_updated': data.get('last_updated'),
            'source': 'WECAR - Windsor-Essex County Association of REALTORS',
            'message': 'Market insights retrieved successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch market insights: {str(e)}',
            'message': 'Unable to retrieve market insights'
        }), 500

@market_data_bp.route('/refresh-data', methods=['POST'])
def refresh_market_data():
    """Force refresh of market data cache"""
    try:
        wecar_market_service.clear_cache()
        data = wecar_market_service.get_market_data()
        
        return jsonify({
            'success': True,
            'data': data,
            'message': 'Market data refreshed successfully',
            'last_updated': data.get('last_updated')
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to refresh market data: {str(e)}',
            'message': 'Unable to refresh market data'
        }), 500

@market_data_bp.route('/data-status', methods=['GET'])
def get_data_status():
    """Get status of market data service"""
    try:
        # Check if service is working
        data = wecar_market_service.get_market_data()
        
        status = {
            'service_status': 'operational',
            'data_source': 'WECAR',
            'last_updated': data.get('last_updated'),
            'data_status': data.get('status', 'unknown'),
            'cache_active': wecar_market_service._is_cache_valid(),
            'available_endpoints': [
                '/api/market-data/current-stats',
                '/api/market-data/market-trends',
                '/api/market-data/market-insights',
                '/api/market-data/refresh-data',
                '/api/market-data/data-status'
            ]
        }
        
        if 'error' in data:
            status['service_status'] = 'degraded'
            status['error'] = data['error']
        
        return jsonify({
            'success': True,
            'status': status,
            'message': 'Data status retrieved successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'status': {
                'service_status': 'error',
                'error': str(e)
            },
            'message': 'Unable to retrieve data status'
        }), 500

