"""
Price routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func, desc
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from app import db
from app.models import PriceData, User
from app.services import AgmarknetService, WeatherService

price_bp = Blueprint('prices', __name__)


@price_bp.route('', methods=['GET'])
def get_prices():
    """Get price data with filters"""
    try:
        district = request.args.get('district')
        mandi = request.args.get('mandi')
        crop = request.args.get('crop')
        variety = request.args.get('variety')
        days = int(request.args.get('days', 30))
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 50))

        query = PriceData.query

        if district:
            query = query.filter(PriceData.district == district)
        if mandi:
            query = query.filter(PriceData.mandi == mandi)
        if crop:
            query = query.filter(PriceData.crop == crop)
        if variety:
            query = query.filter(PriceData.variety == variety)

        start_date = datetime.now() - timedelta(days=days)
        query = query.filter(PriceData.arrival_date >= start_date)

        total = query.count()
        prices = query.order_by(
            PriceData.arrival_date.desc()
        ).paginate(page=page, per_page=limit)

        return jsonify({
            'success': True,
            'data': [p.to_dict() for p in prices.items],
            'total': total,
            'page': page,
            'limit': limit,
            'pages': prices.pages
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching prices: {str(e)}'
        }), 500


@price_bp.route('/latest', methods=['GET'])
def get_latest_prices():
    """Get latest prices for all crops/districts"""
    try:
        limit = int(request.args.get('limit', 100))
        district = request.args.get('district')
        crop = request.args.get('crop')

        query = PriceData.query

        if district:
            query = query.filter(PriceData.district == district)
        if crop:
            query = query.filter(PriceData.crop == crop)

        prices = query.order_by(
            PriceData.arrival_date.desc()
        ).limit(limit).all()

        return jsonify({
            'success': True,
            'data': [p.to_dict() for p in prices],
            'count': len(prices)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching latest prices: {str(e)}'
        }), 500


@price_bp.route('/trends', methods=['GET'])
def get_price_trends():
    """Get price trends with grouping"""
    try:
        crop = request.args.get('crop', 'Wheat')
        district = request.args.get('district')
        mandi = request.args.get('mandi')
        interval = request.args.get('interval', 'daily')
        period = request.args.get('period', '1year')

        period_days = {
            '1week': 7, '1month': 30, '3month': 90,
            '6month': 180, '1year': 365, '2year': 730,
            '3year': 1095, '5year': 1825
        }.get(period, 365)

        query = PriceData.query.filter(PriceData.crop == crop)

        if district:
            query = query.filter(PriceData.district == district)
        if mandi:
            query = query.filter(PriceData.mandi == mandi)

        start_date = datetime.now() - timedelta(days=period_days)
        query = query.filter(PriceData.arrival_date >= start_date)

        prices = query.order_by(PriceData.arrival_date.asc()).all()

        if not prices:
            return jsonify({
                'success': True,
                'data': [],
                'message': 'No data available for the selected filters'
            })

        # Group by interval
        trends = {}
        for price in prices:
            date = price.arrival_date

            if interval == 'weekly':
                date_key = f"{date.year}-W{date.isocalendar()[1]:02d}"
            elif interval == 'monthly':
                date_key = f"{date.year}-{date.month:02d}"
            elif interval == 'yearly':
                date_key = str(date.year)
            else:
                date_key = date.strftime('%Y-%m-%d')

            if date_key not in trends:
                trends[date_key] = {
                    'min_prices': [],
                    'max_prices': [],
                    'modal_prices': [],
                    'count': 0
                }

            if price.min_price:
                trends[date_key]['min_prices'].append(price.min_price)
            if price.max_price:
                trends[date_key]['max_prices'].append(price.max_price)
            if price.modal_price:
                trends[date_key]['modal_prices'].append(price.modal_price)
            trends[date_key]['count'] += 1

        result = []
        for date_key, values in trends.items():
            result.append({
                'date': date_key,
                'min_price': round(np.mean(values['min_prices']), 2) if values['min_prices'] else 0,
                'max_price': round(np.mean(values['max_prices']), 2) if values['max_prices'] else 0,
                'modal_price': round(np.mean(values['modal_prices']), 2) if values['modal_prices'] else 0,
                'count': values['count']
            })

        return jsonify({
            'success': True,
            'data': sorted(result, key=lambda x: x['date']),
            'filters': {
                'crop': crop,
                'district': district,
                'mandi': mandi,
                'interval': interval,
                'period': period
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching trends: {str(e)}'
        }), 500


@price_bp.route('/analysis', methods=['GET'])
def get_price_analysis():
    """Advanced price analysis with technical indicators"""
    try:
        crop = request.args.get('crop', 'Wheat')
        district = request.args.get('district')
        days = int(request.args.get('days', 365))

        query = PriceData.query.filter(PriceData.crop == crop)

        if district:
            query = query.filter(PriceData.district == district)

        start_date = datetime.now() - timedelta(days=days)
        prices = query.filter(
            PriceData.arrival_date >= start_date,
            PriceData.modal_price.isnot(None)
        ).order_by(PriceData.arrival_date.asc()).all()

        if len(prices) < 10:
            return jsonify({
                'success': False,
                'message': 'Insufficient data for analysis (minimum 10 data points)'
            }), 400

        # Extract price data
        price_values = [p.modal_price for p in prices]
        dates = [p.arrival_date for p in prices]

        # Basic statistics
        current_price = price_values[-1]
        start_price = price_values[0]

        # Moving averages
        ma_7 = _calculate_ma(price_values, 7)
        ma_30 = _calculate_ma(price_values, 30)

        # Volatility
        returns = np.diff(price_values) / price_values[:-1]
        volatility = float(np.std(returns) * np.sqrt(365) * 100) if len(returns) > 1 else 0

        # Support and resistance
        support = min(price_values[-20:]) if len(price_values) >= 20 else min(price_values)
        resistance = max(price_values[-20:]) if len(price_values) >= 20 else max(price_values)

        # Trend
        percent_change = ((current_price - start_price) / start_price * 100) if start_price > 0 else 0
        trend = 'up' if percent_change > 0 else 'down' if percent_change < 0 else 'stable'

        # Recommendation
        recommendation = _get_recommendation(current_price, percent_change, volatility, ma_7, ma_30)

        return jsonify({
            'success': True,
            'analysis': {
                'crop': crop,
                'district': district or 'All Districts',
                'period_days': days,
                'data_points': len(price_values),
                'current_price': round(current_price, 2),
                'start_price': round(start_price, 2),
                'percent_change': round(percent_change, 2),
                'trend': trend,
                'volatility': round(volatility, 2),
                'moving_average_7': round(ma_7[-1] if ma_7 else current_price, 2),
                'moving_average_30': round(ma_30[-1] if ma_30 else current_price, 2),
                'support_level': round(support, 2),
                'resistance_level': round(resistance, 2),
                'date_range': {
                    'start': dates[0].isoformat() if dates else None,
                    'end': dates[-1].isoformat() if dates else None
                }
            },
            'recommendation': recommendation
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error in analysis: {str(e)}'
        }), 500


@price_bp.route('/crops', methods=['GET'])
def get_crops():
    """Get list of available crops"""
    try:
        crops = PriceData.query.with_entities(
            PriceData.crop
        ).distinct().all()
        crop_list = sorted([c[0] for c in crops if c[0]])

        return jsonify({
            'success': True,
            'data': crop_list,
            'count': len(crop_list)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching crops: {str(e)}'
        }), 500


@price_bp.route('/districts', methods=['GET'])
def get_districts():
    """Get list of districts with price data"""
    try:
        districts = PriceData.query.with_entities(
            PriceData.district
        ).distinct().all()
        district_list = sorted([d[0] for d in districts if d[0]])

        return jsonify({
            'success': True,
            'data': district_list,
            'count': len(district_list)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching districts: {str(e)}'
        }), 500


@price_bp.route('/mandis', methods=['GET'])
def get_mandis():
    """Get list of mandis for a district"""
    try:
        district = request.args.get('district')

        if not district:
            return jsonify({
                'success': False,
                'message': 'District parameter is required'
            }), 400

        mandis = PriceData.query.with_entities(
            PriceData.mandi
        ).filter_by(district=district).distinct().all()
        mandi_list = sorted([m[0] for m in mandis if m[0]])

        return jsonify({
            'success': True,
            'data': mandi_list,
            'count': len(mandi_list),
            'district': district
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching mandis: {str(e)}'
        }), 500


@price_bp.route('/sync', methods=['POST'])
@jwt_required()
def sync_prices():
    """Sync prices from AGMARKNET (admin only)"""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)

        if not user or not user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Admin access required'
            }), 403

        # Sync data
        service = AgmarknetService()
        result = service.fetch_and_save_prices()

        return jsonify({
            'success': True,
            'message': f'Synced {result.get("count", 0)} price records',
            'details': result
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error syncing prices: {str(e)}'
        }), 500


@price_bp.route('/weather-advice', methods=['GET'])
def get_weather_advice():
    """Get weather and farming advice for crop/district"""
    try:
        crop = request.args.get('crop', 'Wheat')
        district = request.args.get('district', 'Bhopal')
        
        advice = WeatherService.get_soil_advice(crop, district)
        
        return jsonify({
            'success': True,
            'crop': crop,
            'district': district,
            **advice
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching weather advice: {str(e)}'
        }), 500


@price_bp.route('/government-schemes', methods=['GET'])
def get_government_schemes():
    """Get government schemes for farmers"""
    try:
        schemes = [
            {
                'title_hi': 'पीएम-किसान योजना',
                'title_en': 'PM-KISAN Scheme',
                'description_hi': 'प्रत्यक्ष आय सहायता ₹6000 प्रति वर्ष',
                'description_en': 'Direct income support of ₹6000 per year',
                'category': 'financial',
                'eligibility': 'All farmers with land',
                'benefits': '₹6000/year in 3 installments'
            },
            {
                'title_hi': 'पीएम फसल बीमा योजना',
                'title_en': 'PM Crop Insurance',
                'description_hi': 'प्रीमियम सब्सिडी के साथ फसल बीमा',
                'description_en': 'Crop insurance with premium subsidy',
                'category': 'insurance',
                'eligibility': 'All farmers',
                'benefits': 'Crop loss coverage'
            },
            {
                'title_hi': 'सॉइल हेल्थ कार्ड योजना',
                'title_en': 'Soil Health Card Scheme',
                'description_hi': 'मुफ्त मिट्टी जांच और सिफारिशें',
                'description_en': 'Free soil testing and recommendations',
                'category': 'advisory',
                'eligibility': 'All farmers',
                'benefits': 'Free soil testing'
            },
            {
                'title_hi': 'किसान क्रेडिट कार्ड',
                'title_en': 'Kisan Credit Card',
                'description_hi': '4% ब्याज दर पर क्रेडिट',
                'description_en': 'Credit at 4% interest rate',
                'category': 'financial',
                'eligibility': 'All farmers with land',
                'benefits': 'Low interest loans'
            },
            {
                'title_hi': 'ई-नाम पोर्टल',
                'title_en': 'e-NAM Platform',
                'description_hi': 'राष्ट्रीय कृषि बाजार ऑनलाइन प्लेटफॉर्म',
                'description_en': 'National Agriculture Market online platform',
                'category': 'market',
                'eligibility': 'All farmers',
                'benefits': 'Online selling platform'
            }
        ]
        
        return jsonify({
            'success': True,
            'schemes': schemes,
            'count': len(schemes)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching schemes: {str(e)}'
        }), 500


@price_bp.route('/farmer-tips', methods=['GET'])
def get_farmer_tips():
    """Get farming tips and advice"""
    try:
        language = request.args.get('language', 'english')
        
        tips_english = [
            'Test soil before sowing for optimal results',
            'Use certified seeds for better yield',
            'Practice crop rotation to maintain soil health',
            'Use drip irrigation to conserve water',
            'Monitor weather forecasts regularly',
            'Apply organic manure for sustainable farming',
            'Implement integrated pest management',
            'Harvest at the right time for best quality',
            'Store produce properly to prevent spoilage',
            'Keep farm records for better management'
        ]
        
        tips_hindi = [
            'इष्टतम परिणामों के लिए बुवाई से पहले मिट्टी का परीक्षण करें',
            'बेहतर उपज के लिए प्रमाणित बीजों का प्रयोग करें',
            'मिट्टी के स्वास्थ्य को बनाए रखने के लिए फसल चक्रण का अभ्यास करें',
            'पानी बचाने के लिए ड्रिप सिंचाई का उपयोग करें',
            'नियमित रूप से मौसम पूर्वानुमान की निगरानी करें',
            'टिकाऊ खेती के लिए जैविक खाद का प्रयोग करें',
            'समेकित कीट प्रबंधन लागू करें',
            'सर्वोत्तम गुणवत्ता के लिए सही समय पर कटाई करें',
            'उत्पाद को खराब होने से बचाने के लिए ठीक से संग्रहित करें',
            'बेहतर प्रबंधन के लिए खेत के रिकॉर्ड रखें'
        ]
        
        tips = tips_hindi if language == 'hindi' else tips_english
        
        return jsonify({
            'success': True,
            'tips': tips,
            'language': language,
            'count': len(tips)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching tips: {str(e)}'
        }), 500


# Helper functions
def _calculate_ma(values, window):
    """Calculate moving average"""
    if len(values) < window:
        return []
    ma = []
    for i in range(window - 1, len(values)):
        ma.append(sum(values[i - window + 1:i + 1]) / window)
    return ma


def _get_recommendation(current_price, percent_change, volatility, ma_7, ma_30):
    """Generate recommendation"""
    buy_signals = 0
    sell_signals = 0

    if percent_change < -10:
        buy_signals += 2
    elif percent_change > 10:
        sell_signals += 2

    if ma_7 and ma_30 and ma_7[-1] and ma_30[-1]:
        if current_price < ma_7[-1] and current_price < ma_30[-1]:
            buy_signals += 1
        elif current_price > ma_7[-1] and current_price > ma_30[-1]:
            sell_signals += 1

    if buy_signals > sell_signals:
        return {
            'action': 'BUY',
            'confidence': 'HIGH' if buy_signals >= 2 else 'MEDIUM',
            'reason': 'Multiple buy signals detected'
        }
    elif sell_signals > buy_signals:
        return {
            'action': 'SELL',
            'confidence': 'HIGH' if sell_signals >= 2 else 'MEDIUM',
            'reason': 'Multiple sell signals detected'
        }
    else:
        return {
            'action': 'HOLD',
            'confidence': 'LOW',
            'reason': 'Mixed signals, market consolidating'
        }