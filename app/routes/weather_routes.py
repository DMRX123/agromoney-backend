"""
Weather routes
"""
from flask import Blueprint, request, jsonify
from datetime import datetime
from app.services import WeatherService

weather_bp = Blueprint('weather', __name__)


@weather_bp.route('/forecast', methods=['GET'])
def get_weather():
    """Get weather forecast for a district"""
    try:
        district = request.args.get('district', 'Bhopal')
        weather_data = WeatherService.get_weather_forecast(district)

        return jsonify({
            'success': True,
            'data': weather_data,
            'district': district,
            'timestamp': datetime.utcnow().isoformat()
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching weather: {str(e)}'
        }), 500


@weather_bp.route('/advice', methods=['GET'])
def get_weather_advice():
    """Get weather and farming advice"""
    try:
        crop = request.args.get('crop', 'Wheat')
        district = request.args.get('district', 'Bhopal')

        advice = WeatherService.get_soil_advice(crop, district)

        return jsonify({
            'success': True,
            'crop': crop,
            'district': district,
            'advice': advice
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching advice: {str(e)}'
        }), 500


@weather_bp.route('/crop-calendar', methods=['GET'])
def get_crop_calendar():
    """Get crop calendar for Madhya Pradesh"""
    try:
        crop = request.args.get('crop', 'Wheat')

        calendar = {
            'Wheat': {
                'sowing': 'Oct-Nov', 'sowing_hindi': 'अक्टूबर-नवंबर',
                'growth': 'Dec-Feb', 'growth_hindi': 'दिसंबर-फरवरी',
                'harvest': 'Mar-Apr', 'harvest_hindi': 'मार्च-अप्रैल',
                'duration': '120-150 days', 'season': 'Rabi',
                'temperature': '20-25°C', 'rainfall': '50-75 cm',
                'soil': 'Loamy soil', 'fertilizer': 'NPK 80:40:40 kg/ha'
            },
            'Rice': {
                'sowing': 'Jun-Jul', 'sowing_hindi': 'जून-जुलाई',
                'growth': 'Aug-Oct', 'growth_hindi': 'अगस्त-अक्टूबर',
                'harvest': 'Oct-Nov', 'harvest_hindi': 'अक्टूबर-नवंबर',
                'duration': '90-120 days', 'season': 'Kharif',
                'temperature': '25-35°C', 'rainfall': '100-150 cm',
                'soil': 'Clay loam', 'fertilizer': 'NPK 120:60:40 kg/ha'
            },
            'Soybean': {
                'sowing': 'Jun-Jul', 'sowing_hindi': 'जून-जुलाई',
                'growth': 'Aug-Sep', 'growth_hindi': 'अगस्त-सितंबर',
                'harvest': 'Sep-Oct', 'harvest_hindi': 'सितंबर-अक्टूबर',
                'duration': '90-110 days', 'season': 'Kharif',
                'temperature': '25-30°C', 'rainfall': '60-75 cm',
                'soil': 'Well-drained loamy', 'fertilizer': 'NPK 20:60:20 kg/ha'
            },
            'Onion': {
                'sowing': 'Oct-Nov', 'sowing_hindi': 'अक्टूबर-नवंबर',
                'growth': 'Dec-Feb', 'growth_hindi': 'दिसंबर-फरवरी',
                'harvest': 'Mar-Apr', 'harvest_hindi': 'मार्च-अप्रैल',
                'duration': '120-150 days', 'season': 'Rabi',
                'temperature': '20-25°C', 'rainfall': '50-100 cm',
                'soil': 'Sandy loam', 'fertilizer': 'NPK 60:50:50 kg/ha'
            },
            'Garlic': {
                'sowing': 'Oct-Nov', 'sowing_hindi': 'अक्टूबर-नवंबर',
                'growth': 'Dec-Jan', 'growth_hindi': 'दिसंबर-जनवरी',
                'harvest': 'Feb-Mar', 'harvest_hindi': 'फरवरी-मार्च',
                'duration': '120-140 days', 'season': 'Rabi',
                'temperature': '15-25°C', 'rainfall': '50-75 cm',
                'soil': 'Sandy loam', 'fertilizer': 'NPK 150:50:50 kg/ha'
            },
            'Tomato': {
                'sowing': 'Jun-Jul, Oct-Nov', 'sowing_hindi': 'जून-जुलाई, अक्टूबर-नवंबर',
                'growth': 'Aug-Sep, Dec-Jan', 'growth_hindi': 'अगस्त-सितंबर, दिसंबर-जनवरी',
                'harvest': 'Sep-Oct, Jan-Feb', 'harvest_hindi': 'सितंबर-अक्टूबर, जनवरी-फरवरी',
                'duration': '90-100 days', 'season': 'Kharif & Rabi',
                'temperature': '20-30°C', 'rainfall': '50-100 cm',
                'soil': 'Well-drained loamy', 'fertilizer': 'NPK 100:50:50 kg/ha'
            },
            'Coriander': {
                'sowing': 'Oct-Nov', 'sowing_hindi': 'अक्टूबर-नवंबर',
                'growth': 'Dec-Jan', 'growth_hindi': 'दिसंबर-जनवरी',
                'harvest': 'Feb-Mar', 'harvest_hindi': 'फरवरी-मार्च',
                'duration': '90-110 days', 'season': 'Rabi',
                'temperature': '20-25°C', 'rainfall': '40-60 cm',
                'soil': 'Loamy soil', 'fertilizer': 'NPK 40:30:30 kg/ha'
            },
            'Gram': {
                'sowing': 'Oct-Nov', 'sowing_hindi': 'अक्टूबर-नवंबर',
                'growth': 'Dec-Feb', 'growth_hindi': 'दिसंबर-फरवरी',
                'harvest': 'Mar-Apr', 'harvest_hindi': 'मार्च-अप्रैल',
                'duration': '100-120 days', 'season': 'Rabi',
                'temperature': '20-25°C', 'rainfall': '40-60 cm',
                'soil': 'Sandy loam', 'fertilizer': 'NPK 20:40:20 kg/ha'
            },
            'Peas': {
                'sowing': 'Oct-Nov', 'sowing_hindi': 'अक्टूबर-नवंबर',
                'growth': 'Dec-Jan', 'growth_hindi': 'दिसंबर-जनवरी',
                'harvest': 'Feb-Mar', 'harvest_hindi': 'फरवरी-मार्च',
                'duration': '90-100 days', 'season': 'Rabi',
                'temperature': '15-20°C', 'rainfall': '40-60 cm',
                'soil': 'Loamy soil', 'fertilizer': 'NPK 40:40:30 kg/ha'
            },
            'Fenugreek': {
                'sowing': 'Oct-Nov', 'sowing_hindi': 'अक्टूबर-नवंबर',
                'growth': 'Dec-Jan', 'growth_hindi': 'दिसंबर-जनवरी',
                'harvest': 'Feb-Mar', 'harvest_hindi': 'फरवरी-मार्च',
                'duration': '90-100 days', 'season': 'Rabi',
                'temperature': '15-25°C', 'rainfall': '30-50 cm',
                'soil': 'Well-drained sandy', 'fertilizer': 'NPK 30:20:20 kg/ha'
            }
        }

        crop_data = calendar.get(crop, calendar['Wheat'])

        return jsonify({
            'success': True,
            'crop': crop,
            'calendar': crop_data,
            'source': 'MP Agriculture Department'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching crop calendar: {str(e)}'
        }), 500


@weather_bp.route('/farming-tips', methods=['GET'])
def get_farming_tips():
    """Get farming tips"""
    try:
        language = request.args.get('language', 'english')
        crop = request.args.get('crop')

        tips_english = [
            'Test soil before sowing for better yield',
            'Use certified seeds for better germination',
            'Practice crop rotation to maintain soil health',
            'Use drip irrigation to save water',
            'Apply organic manure for better soil health',
            'Monitor weather forecasts regularly',
            'Use integrated pest management',
            'Harvest at the right time for maximum yield',
            'Store produce properly to prevent spoilage',
            'Maintain proper records for better management'
        ]

        tips_hindi = [
            'बेहतर उपज के लिए बुवाई से पहले मिट्टी की जांच करें',
            'बेहतर अंकुरण के लिए प्रमाणित बीजों का उपयोग करें',
            'मिट्टी के स्वास्थ्य के लिए फसल चक्रण करें',
            'पानी बचाने के लिए ड्रिप सिंचाई का उपयोग करें',
            'मिट्टी के स्वास्थ्य के लिए जैविक खाद का उपयोग करें',
            'नियमित रूप से मौसम पूर्वानुमान देखें',
            'समेकित कीट प्रबंधन का उपयोग करें',
            'अधिकतम उपज के लिए सही समय पर कटाई करें',
            'उत्पाद को खराब होने से बचाएं',
            'बेहतर प्रबंधन के लिए रिकॉर्ड रखें'
        ]

        tips = tips_hindi if language == 'hindi' else tips_english

        # Crop-specific tips
        crop_tips = {
            'Wheat': {'english': ['Sow in well-prepared field', 'Apply first irrigation after 20-25 days'],
                      'hindi': ['अच्छी तरह तैयार खेत में बोएं', '20-25 दिन बाद पहली सिंचाई करें']},
            'Rice': {'english': ['Maintain 2-3 cm standing water', 'Transplant at 4-5 leaf stage'],
                     'hindi': ['2-3 सेंटीमीटर पानी रखें', '4-5 पत्ती पर रोपाई करें']}
        }

        if crop and crop in crop_tips:
            tips.extend(crop_tips[crop][language if language == 'hindi' else 'english'])

        return jsonify({
            'success': True,
            'tips': tips,
            'language': language,
            'crop': crop,
            'count': len(tips)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching farming tips: {str(e)}'
        }), 500


@weather_bp.route('/yield-prediction', methods=['GET'])
def get_yield_prediction():
    """Get yield prediction for crop and district"""
    try:
        crop = request.args.get('crop', 'Wheat')
        district = request.args.get('district', 'Bhopal')
        area = float(request.args.get('area', 1.0))

        # Base yields (quintals per hectare)
        base_yields = {
            'Wheat': {'min': 25, 'max': 40, 'avg': 32},
            'Rice': {'min': 20, 'max': 35, 'avg': 28},
            'Soybean': {'min': 15, 'max': 25, 'avg': 20},
            'Onion': {'min': 150, 'max': 250, 'avg': 200},
            'Garlic': {'min': 50, 'max': 80, 'avg': 65}
        }

        # District factors
        district_factors = {
            'Bhopal': 1.0, 'Indore': 1.1, 'Jabalpur': 1.05,
            'Gwalior': 0.95, 'Ujjain': 1.0, 'Sagar': 0.9
        }

        crop_data = base_yields.get(crop, base_yields['Wheat'])
        factor = district_factors.get(district, 1.0)

        predicted = {
            'min': round(crop_data['min'] * factor * area, 2),
            'max': round(crop_data['max'] * factor * area, 2),
            'avg': round(crop_data['avg'] * factor * area, 2),
            'unit': 'quintals' if crop in ['Onion', 'Garlic'] else 'quintals/hectare'
        }

        # Mock current price
        current_price = 1800

        return jsonify({
            'success': True,
            'prediction': {
                'crop': crop,
                'district': district,
                'area_hectares': area,
                'yield': predicted,
                'estimated_revenue': {
                    'min': round(predicted['min'] * current_price * 0.8, 2),
                    'max': round(predicted['max'] * current_price * 1.2, 2),
                    'avg': round(predicted['avg'] * current_price, 2),
                    'currency': 'INR'
                },
                'confidence': 'Medium',
                'recommendations': [
                    'Conduct soil testing for accurate results',
                    'Use quality seeds for better yield',
                    'Follow recommended irrigation schedule'
                ]
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error in yield prediction: {str(e)}'
        }), 500