"""
AGMARKNET Service for fetching mandi prices from data.gov.in API
"""
import requests
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from app.config import Config
from app.extensions import db
from app.models import PriceData

logger = logging.getLogger(__name__)


class AgmarknetService:

    RESOURCE_ID = '35985678-0d79-46b4-9ed6-6f13308a1d24'
    BASE_URL = 'https://api.data.gov.in/resource/35985678-0d79-46b4-9ed6-6f13308a1d24'

    @staticmethod
    def fetch_prices(
        district: Optional[str] = None,
        commodity: Optional[str] = None,
        state: str = 'Madhya Pradesh',
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        try:
            all_records = []
            current_offset = offset
            total_fetched = 0
            
            while True:
                filters = {'State': state}
                
                if district:
                    filters['District'] = district
                if commodity:
                    filters['Commodity'] = commodity
                if date_from:
                    filters['Arrival_Date[ge]'] = date_from
                if date_to:
                    filters['Arrival_Date[le]'] = date_to
                
                params = {
                    'api-key': Config.AGMARKNET_API_KEY,
                    'format': 'json',
                    'limit': min(limit, 100),
                    'offset': current_offset
                }
                
                for key, value in filters.items():
                    params[f'filters[{key}]'] = value
                
                logger.info(f"Fetching prices with params: {params}")
                
                response = requests.get(
                    AgmarknetService.BASE_URL,
                    params=params,
                    timeout=Config.AGMARKNET_TIMEOUT
                )
                
                if response.status_code != 200:
                    logger.error(f"API Error: {response.status_code} - {response.text}")
                    break
                
                data = response.json()
                records = data.get('records', [])
                
                if not records:
                    break
                
                parsed_records = AgmarknetService._parse_records(records)
                all_records.extend(parsed_records)
                
                total_fetched += len(records)
                
                total_records = data.get('total', 0)
                if total_fetched >= total_records or len(records) < limit:
                    break
                
                current_offset += len(records)
                
                if total_fetched >= Config.AGMARKNET_MAX_RECORDS:
                    break
            
            logger.info(f"Fetched {len(all_records)} records from API")
            return all_records
            
        except requests.exceptions.Timeout:
            logger.error("API request timeout")
            return []
        except requests.exceptions.RequestException as e:
            logger.error(f"API request error: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Error fetching prices: {str(e)}")
            return []

    @staticmethod
    def _parse_records(records: List[Dict]) -> List[Dict[str, Any]]:
        parsed = []
        
        for record in records:
            try:
                arrival_date = None
                date_str = record.get('Arrival_Date', '').strip()
                
                if date_str:
                    date_formats = ['%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y', '%m/%d/%Y']
                    for fmt in date_formats:
                        try:
                            arrival_date = datetime.strptime(date_str, fmt)
                            break
                        except ValueError:
                            continue
                    
                    if not arrival_date:
                        try:
                            from dateutil import parser
                            arrival_date = parser.parse(date_str)
                        except:
                            pass
                
                def parse_float(value):
                    if value is None or value == '' or value == 'NA' or value == 'N/A':
                        return None
                    try:
                        return float(value)
                    except (ValueError, TypeError):
                        return None
                
                crop = record.get('Commodity', '').strip()
                if crop == 'Soyabean':
                    crop = 'Soybean'
                
                parsed.append({
                    'district': record.get('District', '').strip(),
                    'mandi': record.get('Market', '').strip(),
                    'crop': crop,
                    'variety': record.get('Variety', '').strip() or None,
                    'grade': record.get('Grade', '').strip() or None,
                    'min_price': parse_float(record.get('Min_Price')),
                    'max_price': parse_float(record.get('Max_Price')),
                    'modal_price': parse_float(record.get('Modal_Price')),
                    'arrival_date': arrival_date or datetime.now()
                })
                
            except Exception as e:
                logger.error(f"Error parsing record: {e}, Record: {record}")
                continue
        
        return parsed

    @staticmethod
    def fetch_and_save_prices(
        district: Optional[str] = None,
        commodity: Optional[str] = None,
        days: int = 7,
        max_records: int = 500
    ) -> Dict[str, Any]:
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            date_from = start_date.strftime('%d/%m/%Y')
            date_to = end_date.strftime('%d/%m/%Y')
            
            logger.info(f"Fetching prices from {date_from} to {date_to}")
            
            records = AgmarknetService.fetch_prices(
                district=district,
                commodity=commodity,
                date_from=date_from,
                date_to=date_to,
                limit=100,
                offset=0
            )
            
            if not records:
                return {
                    'count': 0,
                    'fetched': 0,
                    'duplicates': 0,
                    'message': 'No data fetched from API'
                }
            
            saved = 0
            duplicates = 0
            errors = 0
            
            for record in records:
                try:
                    if not record.get('district') or not record.get('crop'):
                        errors += 1
                        continue
                    
                    existing = PriceData.query.filter_by(
                        district=record['district'],
                        mandi=record['mandi'],
                        crop=record['crop'],
                        variety=record.get('variety'),
                        arrival_date=record['arrival_date']
                    ).first()
                    
                    if existing:
                        duplicates += 1
                        continue
                    
                    price = PriceData(**record)
                    db.session.add(price)
                    saved += 1
                    
                    if saved % 100 == 0:
                        db.session.commit()
                        logger.info(f"Saved {saved} records so far...")
                    
                except Exception as e:
                    logger.error(f"Error saving record: {e}")
                    errors += 1
            
            db.session.commit()
            
            logger.info(f"Saved {saved} new records, {duplicates} duplicates, {errors} errors")
            
            return {
                'count': saved,
                'fetched': len(records),
                'duplicates': duplicates,
                'errors': errors,
                'message': f'Saved {saved} new price records'
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error in fetch_and_save_prices: {str(e)}")
            return {
                'count': 0,
                'fetched': 0,
                'duplicates': 0,
                'errors': 1,
                'error': str(e),
                'message': f'Error: {str(e)}'
            }

    @staticmethod
    def fetch_commodities(state: str = 'Madhya Pradesh') -> List[str]:
        try:
            params = {
                'api-key': Config.AGMARKNET_API_KEY,
                'format': 'json',
                'limit': 100,
                'offset': 0,
                'filters[State]': state
            }
            
            response = requests.get(
                AgmarknetService.BASE_URL,
                params=params,
                timeout=Config.AGMARKNET_TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                records = data.get('records', [])
                commodities = sorted(set(
                    r.get('Commodity', '').strip() 
                    for r in records 
                    if r.get('Commodity')
                ))
                return commodities
            
            return []
            
        except Exception as e:
            logger.error(f"Error fetching commodities: {e}")
            return []

    @staticmethod
    def fetch_districts(state: str = 'Madhya Pradesh') -> List[str]:
        try:
            params = {
                'api-key': Config.AGMARKNET_API_KEY,
                'format': 'json',
                'limit': 100,
                'offset': 0,
                'filters[State]': state
            }
            
            response = requests.get(
                AgmarknetService.BASE_URL,
                params=params,
                timeout=Config.AGMARKNET_TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                records = data.get('records', [])
                districts = sorted(set(
                    r.get('District', '').strip() 
                    for r in records 
                    if r.get('District')
                ))
                return districts
            
            return []
            
        except Exception as e:
            logger.error(f"Error fetching districts: {e}")
            return []