from flask import Blueprint, jsonify, request
from utils.agmarknet import AgmarknetAPI
from utils.candle_utils import CandleUtils
from datetime import datetime, timedelta
import requests
import random

market_bp = Blueprint('market', __name__)
agmarknet = AgmarknetAPI()

@market_bp.route('/rates', methods=['GET'])
def get_market_rates():
    try:
        crop = request.args.get('crop')
        district = request.args.get('district', 'Indore')
        limit = request.args.get('limit', 50, type=int)
        
        # Get yesterday's date for latest data
        yesterday = datetime.now() - timedelta(days=1)
        date_str = yesterday.strftime('%Y-%m-%d')
        
        print(f"Fetching rates for crop: {crop}, district: {district}, date: {date_str}")
        
        # Try to get real data from Agmarknet API
        data = agmarknet.get_latest_rates(crop, district, date_str, limit)
        
        if data and len(data) > 0:
            return jsonify({
                'success': True, 
                'data': data,
                'count': len(data),
                'source': 'agmarknet_live',
                'date': date_str
            })
        else:
            # Generate realistic sample data if no real data available
            sample_data = _generate_sample_market_data(crop, district, limit)
            return jsonify({
                'success': True,
                'data': sample_data,
                'count': len(sample_data),
                'source': 'sample_data',
                'date': date_str
            })
        
    except Exception as e:
        print(f"Error fetching market rates: {e}")
        return jsonify({
            'success': False, 
            'error': str(e)
        }), 500

@market_bp.route('/crops', methods=['GET'])
def get_crops():
    from config import Config
    return jsonify({'success': True, 'crops': Config.CROPS})

@market_bp.route('/districts', methods=['GET'])
def get_districts():
    from config import Config
    return jsonify({'success': True, 'districts': Config.MP_DISTRICTS})

@market_bp.route('/historical', methods=['GET'])
def get_historical_data():
    try:
        crop = request.args.get('crop')
        district = request.args.get('district', 'Indore')
        years = request.args.get('years', 10, type=int)
        
        if not crop:
            return jsonify({'success': False, 'error': 'Crop parameter is required'})
        
        print(f"Fetching historical data for crop: {crop}, district: {district}, years: {years}")
        
        # Try to get real data first
        data = agmarknet.get_historical_data(crop, district, years)
        
        if data and len(data) > 0:
            return jsonify({
                'success': True, 
                'data': data,
                'count': len(data),
                'source': 'agmarknet',
                'years': years
            })
        else:
            # Generate 10 years of historical sample data
            sample_data = _generate_10_years_historical_data(crop, district)
            return jsonify({
                'success': True,
                'data': sample_data,
                'count': len(sample_data),
                'source': 'sample_data',
                'years': years
            })
        
    except Exception as e:
        print(f"Error fetching historical data: {e}")
        return jsonify({
            'success': False, 
            'error': str(e)
        }), 500

@market_bp.route('/flexible-data', methods=['GET'])
def get_flexible_data():
    try:
        crop = request.args.get('crop')
        district = request.args.get('district', 'Indore')
        years = request.args.get('years', 1, type=float)
        interval_days = request.args.get('interval_days', 1, type=int)
        
        if not crop:
            return jsonify({'success': False, 'error': 'Crop parameter is required'})
        
        print(f"Fetching flexible data for crop: {crop}, district: {district}, "
              f"years: {years}, interval_days: {interval_days}")
        
        # Use common utility for candle data
        data = CandleUtils.generate_flexible_historical_data(crop, district, years, interval_days)
        
        if data and len(data) > 0:
            return jsonify({
                'success': True, 
                'data': data,
                'count': len(data),
                'years': years,
                'interval_days': interval_days,
                'source': 'generated'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'No data available'
            })
        
    except Exception as e:
        print(f"Error fetching flexible data: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@market_bp.route('/candle-data', methods=['GET', 'OPTIONS'])
def get_candle_data():
    """Get candle stick data for market analysis with 10 years support"""
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', '*')
        response.headers.add('Access-Control-Allow-Methods', '*')
        return response
    
    try:
        crop = request.args.get('crop', 'wheat').title()
        district = request.args.get('district', 'Indore')
        years = float(request.args.get('years', 0.25))
        interval_days = int(request.args.get('interval_days', 1))
        
        print(f"📊 Fetching candle data for {crop} ({years} years, interval: {interval_days} days)")
        
        # Use common utility for candle data
        candle_data = CandleUtils.generate_candle_data(crop, district, years, interval_days)
        
        return jsonify({
            'success': True,
            'crop': crop,
            'district': district,
            'period_years': years,
            'interval_days': interval_days,
            'candle_data': candle_data,
            'data_points': len(candle_data),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"❌ Candle data error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def _generate_sample_market_data(crop=None, district=None, limit=50):
    """Generate realistic sample market data for MP"""
    
    base_prices = {
        # Cereals
        "Wheat": 2400, "Rice": 3000, "Maize": 2200, "Jowar": 2600, "Bajra": 2400,
        # Pulses
        "Gram": 5200, "Lentil": 6000, "Pigeon Pea": 7000, "Black Gram": 6500, 
        "Green Gram": 7000, "Cowpea": 4800,
        # Oilseeds
        "Soybean": 4800, "Mustard": 5200, "Groundnut": 6000, "Sunflower": 5200, 
        "Sesame": 8000, "Linseed": 4800, "Castor": 5800,
        # Vegetables
        "Tomato": 1500, "Onion": 2000, "Potato": 1800, "Garlic": 4500, 
        "Cabbage": 1200, "Cauliflower": 1500, "Brinjal": 2000, "Okra": 3000, 
        "Peas": 3500, "Carrot": 2200, "Radish": 1500, "Cucumber": 1800, 
        "Bitter Gourd": 2500, "Bottle Gourd": 1600, "Spinach": 1200,
        # Spices
        "Coriander": 6500, "Chilli": 5500, "Cumin": 10000, "Fenugreek": 5000, 
        "Turmeric": 7500, "Ginger": 6500, "Coriander Seed": 7500,
        # Cash Crops
        "Cotton": 7000, "Sugarcane": 3500, "Tobacco": 10000, "Jute": 4200,
        # Fruits
        "Mango": 4500, "Banana": 2200, "Guava": 3000, "Orange": 3500, 
        "Papaya": 1800, "Pomegranate": 5500, "Lemon": 3000,
        # Other
        "Honey": 12000, "Mushroom": 15000
    }
    
    mp_markets = {
        "Indore": ["Indore Mandi", "Sitapur Mandi", "Sanwer", "Mhow", "Depalpur"],
        "Bhopal": ["Bhopal Mandi", "Hathaikheda", "Berasia"],
        "Ujjain": ["Ujjain Mandi", "Nagda", "Khachrod", "Mahidpur"],
        "Gwalior": ["Gwalior Mandi", "Morar", "Dabra"],
        "Jabalpur": ["Jabalpur Mandi", "Adhartal", "Khamaria"],
        "Ratlam": ["Ratlam Mandi", "Jaora", "Alot"],
        "Sagar": ["Sagar Mandi", "Rahatgarh", "Bina"],
        "Rewa": ["Rewa Mandi", "Mauganj", "Hanumana"],
        "Satna": ["Satna Mandi", "Maihar", "Nagod"],
        "Dewas": ["Dewas Mandi", "Sonkatch", "Kannod"]
    }
    
    target_crops = [crop] if crop else list(base_prices.keys())[:10]
    target_districts = [district] if district else list(mp_markets.keys())
    
    data = []
    today = datetime.now().strftime('%Y-%m-%d')
    
    for dist in target_districts:
        markets = mp_markets.get(dist, [f"{dist} Mandi"])
        
        for crp in target_crops:
            if crp in base_prices:
                base_price = base_prices[crp]
                
                for market in markets:
                    variation = random.uniform(-0.15, 0.15)
                    current_price = base_price * (1 + variation)
                    
                    data.append({
                        'commodity': crp,
                        'district': dist,
                        'market': market,
                        'min_price': round(current_price * 0.9, 2),
                        'max_price': round(current_price * 1.1, 2),
                        'modal_price': round(current_price, 2),
                        'arrival_date': today,
                        'timestamp': datetime.now().isoformat()
                    })
    
    return data[:limit]

def _generate_10_years_historical_data(crop, district=None):
    """Generate 10 years of realistic historical data"""
    
    base_prices = {
        "Wheat": 2400, "Rice": 3000, "Maize": 2200, "Soybean": 4800, "Gram": 5200,
        "Tomato": 1500, "Onion": 2000, "Potato": 1800, "Garlic": 4500, "Coriander": 6500,
        "Cumin": 10000, "Cotton": 7000, "Sugarcane": 3500, "Mango": 4500, "Banana": 2200
    }
    
    base_price = base_prices.get(crop, 3000)
    data = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=10*365)
    
    current_date = start_date
    
    while current_date <= end_date:
        month = current_date.month
        
        if crop in ["Wheat", "Gram", "Mustard"]:
            seasonal_factor = 1.0 + (0.2 * abs(6 - month) / 6)
        elif crop in ["Rice", "Soybean", "Maize"]:
            seasonal_factor = 1.0 + (0.15 * abs(12 - month) / 6)
        elif crop in ["Tomato", "Onion", "Potato"]:
            seasonal_factor = 1.0 + (0.4 * random.uniform(-1, 1))
        else:
            seasonal_factor = 1.0 + (0.2 * random.uniform(-1, 1))
        
        years_passed = (current_date - start_date).days / 365
        trend_factor = 1.0 + (0.05 * years_passed)
        
        random_factor = random.uniform(0.9, 1.1)
        
        price = base_price * seasonal_factor * trend_factor * random_factor
        
        data.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'price': round(price, 2),
            'volume': random.randint(100, 1000),
            'commodity': crop,
            'district': district or 'Multiple Districts',
            'category': _get_crop_category(crop)
        })
        
        current_date += timedelta(days=30)
    
    return data

def _get_crop_category(crop):
    """Get category for a crop"""
    categories = {
        'Cereals': ['Wheat', 'Rice', 'Maize', 'Jowar', 'Bajra'],
        'Pulses': ['Gram', 'Lentil', 'Pigeon Pea', 'Black Gram', 'Green Gram', 'Cowpea'],
        'Oilseeds': ['Soybean', 'Mustard', 'Groundnut', 'Sunflower', 'Sesame', 'Linseed', 'Castor'],
        'Vegetables': ['Tomato', 'Onion', 'Potato', 'Garlic', 'Cabbage', 'Cauliflower', 'Brinjal', 
                      'Okra', 'Peas', 'Carrot', 'Radish', 'Cucumber', 'Bitter Gourd', 'Bottle Gourd', 'Spinach'],
        'Spices': ['Coriander', 'Chilli', 'Cumin', 'Fenugreek', 'Turmeric', 'Ginger', 'Coriander Seed'],
        'Cash Crops': ['Cotton', 'Sugarcane', 'Tobacco', 'Jute'],
        'Fruits': ['Mango', 'Banana', 'Guava', 'Orange', 'Papaya', 'Pomegranate', 'Lemon'],
        'Other': ['Honey', 'Mushroom']
    }
    
    for category, crops_list in categories.items():
        if crop in crops_list:
            return category
    return 'Other'

@market_bp.route('/trends', methods=['GET'])
def get_market_trends():
    """Get market trends for a specific crop with 10 years data"""
    try:
        crop = request.args.get('crop')
        district = request.args.get('district', 'Indore')
        
        if not crop:
            return jsonify({'success': False, 'error': 'Crop parameter is required'})
        
        historical_data = _generate_10_years_historical_data(crop, district)
        
        if not historical_data:
            return jsonify({'success': False, 'error': 'No data available for trend analysis'})
        
        recent_prices = [item['price'] for item in historical_data[-12:]]
        older_prices = [item['price'] for item in historical_data[-24:-12]]
        
        if len(recent_prices) >= 6 and len(older_prices) >= 6:
            current_avg = sum(recent_prices) / len(recent_prices)
            previous_avg = sum(older_prices) / len(older_prices)
            
            price_change_7d = ((recent_prices[-1] - recent_prices[-7]) / recent_prices[-7]) * 100 if len(recent_prices) > 7 else 0
            price_change_30d = ((current_avg - previous_avg) / previous_avg) * 100
        else:
            price_change_7d = random.uniform(-5, 5)
            price_change_30d = random.uniform(-10, 10)
        
        if price_change_30d > 5:
            trend = 'increasing'
        elif price_change_30d < -5:
            trend = 'decreasing'
        else:
            trend = 'stable'
        
        trend_analysis = {
            'crop': crop,
            'district': district,
            'current_trend': trend,
            'price_change_7d': f"{price_change_7d:+.1f}%",
            'price_change_30d': f"{price_change_30d:+.1f}%",
            'current_price': recent_prices[-1] if recent_prices else 0,
            'recommendation': _get_trend_recommendation(trend),
            'analysis_period': '10 years',
            'data_points': len(historical_data)
        }
        
        return jsonify({
            'success': True,
            'trend_analysis': trend_analysis,
            'historical_data_points': len(historical_data)
        })
        
    except Exception as e:
        print(f"Error in market trends: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

def _get_trend_recommendation(trend):
    """Get recommendation based on market trend"""
    recommendations = {
        'increasing': 'Good time to sell. Prices are rising.',
        'decreasing': 'Consider waiting. Prices are falling.',
        'stable': 'Market is stable. Monitor for opportunities.'
    }
    return recommendations.get(trend, 'Monitor market regularly.')