"""
Helper utility functions
"""
import re
import random
from datetime import datetime
from typing import Optional


def format_currency(amount: float) -> str:
    """Format amount as Indian currency"""
    if amount is None:
        return "₹0"
    return f"₹{amount:,.2f}"


def format_date(date_obj: datetime, format_str: str = "%d %b %Y") -> str:
    """Format date to readable string"""
    if not date_obj:
        return ""
    return date_obj.strftime(format_str)


def parse_date(date_str: str, format_str: str = "%Y-%m-%d") -> Optional[datetime]:
    """Parse date from string"""
    try:
        return datetime.strptime(date_str, format_str)
    except ValueError:
        return None


def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """Calculate percentage change"""
    if old_value == 0:
        return 0
    return ((new_value - old_value) / old_value) * 100


def validate_phone_number(phone: str) -> bool:
    """Validate Indian phone number"""
    pattern = r'^[6-9]\d{9}$'
    return bool(re.match(pattern, phone))


def validate_email(email: str) -> bool:
    """Validate email address"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))


def generate_otp(length: int = 6) -> str:
    """Generate OTP of specified length"""
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])


def get_season_from_date(date: datetime) -> str:
    """Get season for MP region"""
    month = date.month
    if month in [10, 11, 12, 1, 2, 3]:
        return 'Rabi'
    elif month in [6, 7, 8, 9]:
        return 'Kharif'
    else:
        return 'Zaid'


def truncate_text(text: str, max_length: int = 100, suffix: str = '...') -> str:
    """Truncate text to specified length"""
    if not text:
        return ''
    if len(text) <= max_length:
        return text
    return text[:max_length] + suffix