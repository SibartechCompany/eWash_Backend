import uuid
import random
import string
from datetime import datetime
from typing import Optional

def generate_order_number() -> str:
    """Generate a unique order number"""
    timestamp = datetime.now().strftime("%Y%m%d")
    random_suffix = ''.join(random.choices(string.digits, k=4))
    return f"ORD-{timestamp}-{random_suffix}"

def generate_uuid() -> uuid.UUID:
    """Generate a new UUID"""
    return uuid.uuid4()

def format_phone_number(phone: str) -> str:
    """Format phone number to standard format"""
    # Remove all non-digit characters
    digits_only = ''.join(filter(str.isdigit, phone))
    
    # Add country code if not present (assuming Colombia +57)
    if len(digits_only) == 10 and not digits_only.startswith('57'):
        digits_only = '57' + digits_only
    
    return digits_only

def validate_email(email: str) -> bool:
    """Basic email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def calculate_service_end_time(start_time: datetime, duration_minutes: int) -> datetime:
    """Calculate service end time based on start time and duration"""
    from datetime import timedelta
    return start_time + timedelta(minutes=duration_minutes) 