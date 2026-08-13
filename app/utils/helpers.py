"""
Helper utility functions - Updated with API helpers
"""
import re
import random
from datetime import datetime, timedelta
from typing import Optional


def format_currency(amount: float) -> str:
    if amount is None:
        return "₹0"
    return f"₹{amount:,.2f}"


def format_date(date_obj: datetime, format_str: str = "%d %b %Y") -> str:
    if not date_obj:
        return ""
    return date_obj.strftime(format_str)


def parse_date(date_str: str, format_str: str = "%Y-%m-%d") -> Optional[datetime]:
    try:
        return datetime.strptime(date_str, format_str)
    except ValueError:
        return None


def parse_api_date(date_str: str) -> Optional[datetime]:
    if not date_str:
        return None
    
    formats = ['%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y', '%m/%d/%Y']
    for fmt in formats:
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue
    
    try:
        from dateutil import parser
        return parser.parse(date_str)
    except:
        return None


def format_api_date(date_obj: datetime) -> str:
    if not date_obj:
        return ""
    return date_obj.strftime('%d/%m/%Y')


def calculate_percentage_change(old_value: float, new_value: float) -> float:
    if old_value == 0:
        return 0
    return ((new_value - old_value) / old_value) * 100


def validate_phone_number(phone: str) -> bool:
    pattern = r'^[6-9]\d{9}$'
    return bool(re.match(pattern, phone))


def validate_email(email: str) -> bool:
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))


def generate_otp(length: int = 6) -> str:
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])


def get_season_from_date(date: datetime) -> str:
    month = date.month
    if month in [10, 11, 12, 1, 2, 3]:
        return 'Rabi'
    elif month in [6, 7, 8, 9]:
        return 'Kharif'
    else:
        return 'Zaid'


def truncate_text(text: str, max_length: int = 100, suffix: str = '...') -> str:
    if not text:
        return ''
    if len(text) <= max_length:
        return text
    return text[:max_length] + suffix


def get_date_range_for_api(days: int = 7) -> tuple:
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    return start_date, end_date


def clean_price_value(value) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        value = value.strip()
        if not value or value in ['', 'NA', 'N/A', '-']:
            return None
        try:
            return float(value)
        except ValueError:
            return None
    return None


def is_valid_date(date_str: str) -> bool:
    if not date_str:
        return False
    
    date_obj = parse_api_date(date_str)
    if not date_obj:
        return False
    
    if date_obj.year < 2010:
        return False
    
    return True