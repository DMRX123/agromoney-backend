"""
AGMARKNET Service for fetching mandi prices
"""
import requests
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
from app.config import Config
from app import db
from app.models import PriceData

logger = logging.getLogger(__name__)


class AgmarknetService:
    """Service for interacting with AGMARKNET API"""

    @staticmethod
    def fetch_prices(
        district: str = None,
        commodity: str = None,
        date_from: str = None,
        date_to: str = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Fetch prices from AGMARKNET API"""
        try:
            params = {
                'api-key': Config.AGMARKNET_API_KEY,
                'format': 'json',
                'limit': limit,
                'filters[State]': 'Madhya Pradesh'
            }

            if district:
                params['filters[District]'] = district
            if commodity:
                params['filters[Commodity]'] = commodity
            if date_from:
                params['filters[Arrival_Date][ge]'] = date_from
            if date_to:
                params['filters[Arrival_Date][le]'] = date_to

            response = requests.get(
                Config.AGMARKNET_BASE_URL,
                params=params,
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                records = data.get('records', [])
                return AgmarknetService._parse_records(records)
            else:
                logger.error(f"API Error: {response.status_code}")
                return []

        except Exception as e:
            logger.error(f"Error fetching prices: {str(e)}")
            return []

    @staticmethod
    def _parse_records(records: List[Dict]) -> List[Dict[str, Any]]:
        """Parse API records"""
        parsed = []
        for record in records:
            try:
                arrival_date = None
                if record.get('Arrival_Date'):
                    try:
                        arrival_date = datetime.strptime(
                            record['Arrival_Date'],
                            '%d/%m/%Y'
                        )
                    except:
                        pass

                parsed.append({
                    'district': record.get('District', ''),
                    'mandi': record.get('Market', ''),
                    'crop': record.get('Commodity', ''),
                    'variety': record.get('Variety', ''),
                    'grade': record.get('Grade', ''),
                    'min_price': float(record.get('Min_Price', 0) or 0),
                    'max_price': float(record.get('Max_Price', 0) or 0),
                    'modal_price': float(record.get('Modal_Price', 0) or 0),
                    'arrival_date': arrival_date or datetime.now()
                })
            except Exception as e:
                logger.error(f"Error parsing record: {e}")
                continue

        return parsed

    @staticmethod
    def fetch_and_save_prices(
        district: str = None,
        commodity: str = None,
        days: int = 7
    ) -> Dict[str, Any]:
        """Fetch and save prices to database"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)

            records = AgmarknetService.fetch_prices(
                district=district,
                commodity=commodity,
                date_from=start_date.strftime('%d/%m/%Y'),
                date_to=end_date.strftime('%d/%m/%Y')
            )

            if not records:
                return {'count': 0, 'message': 'No data fetched'}

            saved = 0
            for record in records:
                # Check if price already exists
                existing = PriceData.query.filter_by(
                    district=record['district'],
                    mandi=record['mandi'],
                    crop=record['crop'],
                    arrival_date=record['arrival_date']
                ).first()

                if not existing:
                    price = PriceData(**record)
                    db.session.add(price)
                    saved += 1

            db.session.commit()

            return {
                'count': saved,
                'total_fetched': len(records),
                'message': f'Saved {saved} price records'
            }

        except Exception as e:
            db.session.rollback()
            logger.error(f"Error saving prices: {str(e)}")
            return {'count': 0, 'error': str(e)}