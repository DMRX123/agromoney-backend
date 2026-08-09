"""
Weather Service
"""
import requests
import logging
from datetime import datetime
from typing import Dict
from app.config import Config

logger = logging.getLogger(__name__)


class WeatherService:
    """Service for weather and farming advice"""

    # District coordinates for MP
    DISTRICT_COORDINATES = {
        'Bhopal': {'lat': 23.2599, 'lon': 77.4126},
        'Indore': {'lat': 22.7196, 'lon': 75.8577},
        'Jabalpur': {'lat': 23.1815, 'lon': 79.9864},
        'Gwalior': {'lat': 26.2183, 'lon': 78.1828},
        'Ujjain': {'lat': 23.1793, 'lon': 75.7849},
        'Sagar': {'lat': 23.8388, 'lon': 78.7378},
        'Rewa': {'lat': 24.5373, 'lon': 81.3042},
        'Satna': {'lat': 24.6000, 'lon': 80.8333},
        'Ratlam': {'lat': 23.3341, 'lon': 75.0376},
        'Dewas': {'lat': 22.9658, 'lon': 76.0553}
    }

    @staticmethod
    def get_weather_forecast(district: str) -> Dict:
        """Get weather forecast for a district"""
        try:
            coords = WeatherService.DISTRICT_COORDINATES.get(
                district,
                {'lat': 23.2599, 'lon': 77.4126}
            )

            if Config.WEATHER_API_KEY:
                params = {
                    'lat': coords['lat'],
                    'lon': coords['lon'],
                    'appid': Config.WEATHER_API_KEY,
                    'units': 'metric'
                }
                response = requests.get(
                    'https://api.openweathermap.org/data/2.5/weather',
                    params=params,
                    timeout=5
                )

                if response.status_code == 200:
                    data = response.json()
                    return {
                        'district': district,
                        'temperature': data.get('main', {}).get('temp', 0),
                        'feels_like': data.get('main', {}).get('feels_like', 0),
                        'humidity': data.get('main', {}).get('humidity', 0),
                        'pressure': data.get('main', {}).get('pressure', 0),
                        'weather': data.get('weather', [{}])[0].get('main', 'Unknown'),
                        'description': data.get('weather', [{}])[0].get('description', ''),
                        'wind_speed': data.get('wind', {}).get('speed', 0),
                        'clouds': data.get('clouds', {}).get('all', 0),
                        'timestamp': datetime.utcnow().isoformat()
                    }

        except Exception as e:
            logger.error(f"Error fetching weather: {e}")

        # Return mock data if API fails
        return {
            'district': district,
            'temperature': 28.5,
            'feels_like': 30.2,
            'humidity': 65,
            'pressure': 1013,
            'weather': 'Clear',
            'description': 'clear sky',
            'wind_speed': 3.5,
            'clouds': 20,
            'timestamp': datetime.utcnow().isoformat(),
            'forecast': 'Partly cloudy next 3 days'
        }

    @staticmethod
    def get_soil_advice(crop: str, district: str) -> Dict:
        """Get soil and farming advice"""
        crop_requirements = {
            'Wheat': {
                'ideal_soil': 'Loamy soil',
                'ph_range': '6.0-7.5',
                'temperature': '20-25°C',
                'rainfall': '50-75 cm',
                'season': 'Rabi (Oct-Mar)',
                'fertilizer': 'NPK 80:40:40 kg/ha',
                'sowing': 'Oct-Nov',
                'harvest': 'Mar-Apr',
                'duration': '120-150 days'
            },
            'Rice': {
                'ideal_soil': 'Clay loam',
                'ph_range': '5.5-6.5',
                'temperature': '25-35°C',
                'rainfall': '100-150 cm',
                'season': 'Kharif (Jun-Nov)',
                'fertilizer': 'NPK 120:60:40 kg/ha',
                'sowing': 'Jun-Jul',
                'harvest': 'Oct-Nov',
                'duration': '90-120 days'
            },
            'Soybean': {
                'ideal_soil': 'Well-drained loamy',
                'ph_range': '6.0-7.0',
                'temperature': '25-30°C',
                'rainfall': '60-75 cm',
                'season': 'Kharif (Jun-Oct)',
                'fertilizer': 'NPK 20:60:20 kg/ha',
                'sowing': 'Jun-Jul',
                'harvest': 'Sep-Oct',
                'duration': '90-110 days'
            },
            'Onion': {
                'ideal_soil': 'Sandy loam',
                'ph_range': '6.0-7.5',
                'temperature': '20-25°C',
                'rainfall': '50-100 cm',
                'season': 'Rabi (Oct-Mar)',
                'fertilizer': 'NPK 60:50:50 kg/ha',
                'sowing': 'Oct-Nov',
                'harvest': 'Mar-Apr',
                'duration': '120-150 days'
            }
        }

        requirements = crop_requirements.get(crop, crop_requirements['Wheat'])

        return {
            'crop': crop,
            'district': district,
            'requirements': requirements,
            'current_soil': {
                'type': 'Loamy soil',
                'ph': '6.5-7.5',
                'suitability': 'Good'
            },
            'recommendations': [
                'Test soil before sowing',
                'Use certified seeds',
                'Apply recommended fertilizers',
                'Monitor for pests and diseases'
            ]
        }

    @staticmethod
    def get_district_weather(district: str) -> Dict:
        """Get weather for specific district"""
        try:
            # Get weather data
            weather = WeatherService.get_weather_forecast(district)
            
            # Add additional agriculture-specific data
            agri_data = {
                'soil_advice': WeatherService.get_soil_advice('Wheat', district),
                'crop_suitability': {
                    'Wheat': 'Good',
                    'Rice': 'Moderate',
                    'Soybean': 'Excellent',
                    'Onion': 'Good'
                }
            }
            
            return {
                'weather': weather,
                'agriculture': agri_data
            }
        except Exception as e:
            logger.error(f"Error getting district weather: {e}")
            return {
                'weather': WeatherService.get_weather_forecast(district),
                'agriculture': {
                    'soil_advice': 'Soil is suitable for most crops',
                    'crop_suitability': {}
                }
            }