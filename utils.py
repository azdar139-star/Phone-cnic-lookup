"""
Utility Functions
Phone and CNIC validation and formatting utilities
"""

import re

def validate_phone(phone):
    """
    Validate Pakistani phone number format
    
    Accepted formats:
    - 03001234567 (11 digits)
    - +92-300-1234567
    - +923001234567
    - 0300-123-4567
    
    Args:
        phone (str): Phone number to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    
    if not phone or not isinstance(phone, str):
        return False
    
    # Remove spaces and hyphens
    phone_clean = phone.replace(' ', '').replace('-', '')
    
    # Remove + and country code if present
    if phone_clean.startswith('+92'):
        phone_clean = '0' + phone_clean[3:]
    
    # Check if it's 11 digits starting with 03
    if len(phone_clean) == 11 and phone_clean.startswith('03') and phone_clean.isdigit():
        return True
    
    return False

def normalize_phone(phone):
    """
    Normalize phone number to standard format
    
    Args:
        phone (str): Phone number to normalize
    
    Returns:
        str: Normalized phone number (e.g., 03001234567)
    """
    
    if not phone:
        return None
    
    # Remove spaces and hyphens
    phone_clean = phone.replace(' ', '').replace('-', '')
    
    # Remove + and country code if present
    if phone_clean.startswith('+92'):
        phone_clean = '0' + phone_clean[3:]
    elif phone_clean.startswith('92'):
        phone_clean = '0' + phone_clean[2:]
    
    # Return only digits
    return ''.join(filter(str.isdigit, phone_clean))[-11:] if phone_clean else None

def validate_cnic(cnic):
    """
    Validate Pakistani CNIC format
    
    Accepted formats:
    - 12345-6789012-3
    - 12345 6789012 3
    - 123456789012-3
    
    Args:
        cnic (str): CNIC number to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    
    if not cnic or not isinstance(cnic, str):
        return False
    
    # Remove spaces and hyphens
    cnic_clean = cnic.replace(' ', '').replace('-', '')
    
    # Check if it's 13 digits
    if len(cnic_clean) == 13 and cnic_clean.isdigit():
        return True
    
    return False

def normalize_cnic(cnic):
    """
    Normalize CNIC to standard format (12345-6789012-3)
    
    Args:
        cnic (str): CNIC number to normalize
    
    Returns:
        str: Normalized CNIC number
    """
    
    if not cnic:
        return None
    
    # Remove spaces and hyphens
    cnic_clean = cnic.replace(' ', '').replace('-', '')
    
    # Extract only digits
    cnic_digits = ''.join(filter(str.isdigit, cnic_clean))
    
    # Return in format: 12345-6789012-3
    if len(cnic_digits) == 13:
        return f"{cnic_digits[0:5]}-{cnic_digits[5:12]}-{cnic_digits[12]}"
    
    return None

def format_cnic_display(cnic):
    """Format CNIC for display"""
    normalized = normalize_cnic(cnic)
    return normalized if normalized else cnic

def format_phone_display(phone):
    """Format phone number for display"""
    normalized = normalize_phone(phone)
    if normalized and len(normalized) == 11:
        return f"{normalized[0:4]}-{normalized[4:7]}-{normalized[7:11]}"
    return normalized

def is_valid_name(name):
    """
    Validate if a name contains only letters and spaces
    
    Args:
        name (str): Name to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    
    if not name or not isinstance(name, str):
        return False
    
    # Remove extra spaces
    name_clean = name.strip()
    
    # Check if contains only letters and spaces
    return bool(re.match(r'^[a-zA-Z\s]+$', name_clean)) and len(name_clean) > 0

def is_valid_provider(provider):
    """
    Validate if provider is one of the known Pakistani providers
    
    Args:
        provider (str): Provider name
    
    Returns:
        bool: True if valid, False otherwise
    """
    
    valid_providers = ['Jazz', 'Zong', 'Telenor', 'Warid', 'Ufone', 'Other', 'Unknown']
    return provider in valid_providers

def get_provider_from_phone(phone):
    """
    Determine provider from phone number prefix
    
    Args:
        phone (str): Phone number
    
    Returns:
        str: Provider name
    """
    
    normalized = normalize_phone(phone)
    
    if not normalized or len(normalized) < 4:
        return 'Unknown'
    
    prefix = normalized[0:4]
    
    # Jazz prefixes
    if prefix in ['0300', '0301', '0302', '0303', '0304', '0305']:
        return 'Jazz'
    
    # Zong prefixes
    elif prefix in ['0310', '0311', '0312', '0313', '0314', '0315']:
        return 'Zong'
    
    # Telenor prefixes
    elif prefix in ['0320', '0321', '0322', '0323', '0324', '0325']:
        return 'Telenor'
    
    # Ufone prefixes
    elif prefix in ['0330', '0331', '0332', '0333', '0334', '0335']:
        return 'Ufone'
    
    # Warid prefixes
    elif prefix in ['0340', '0341', '0342', '0343', '0344', '0345']:
        return 'Warid'
    
    return 'Other'

def sanitize_input(user_input):
    """
    Sanitize user input to prevent injection attacks
    
    Args:
        user_input (str): User input string
    
    Returns:
        str: Sanitized input
    """
    
    if not user_input:
        return ''
    
    # Remove potentially harmful characters
    sanitized = re.sub(r'[^\w\s\-+().]', '', str(user_input))
    
    return sanitized.strip()

def get_circle_from_phone(phone):
    """
    Determine circle/region from phone number
    
    Args:
        phone (str): Phone number
    
    Returns:
        str: Circle name
    """
    
    # This is a simplified version - actual implementation would be more detailed
    # In reality, you'd need a mapping database
    
    normalized = normalize_phone(phone)
    
    if not normalized or len(normalized) < 4:
        return 'Unknown'
    
    # For demonstration purposes, return based on prefix
    prefix = normalized[0:4]
    
    # Karachi area codes
    if prefix in ['0300', '0301', '0302']:
        return 'Karachi'
    
    # Lahore area codes
    elif prefix in ['0310', '0311', '0312']:
        return 'Lahore'
    
    # Islamabad area codes
    elif prefix in ['0320', '0321', '0322']:
        return 'Islamabad'
    
    # Peshawar area codes
    elif prefix in ['0330', '0331', '0332']:
        return 'Peshawar'
    
    # Multan area codes
    elif prefix in ['0340', '0341', '0342']:
        return 'Multan'
    
    return 'Pakistan'

def split_name(full_name):
    """
    Split full name into first and last name
    
    Args:
        full_name (str): Full name
    
    Returns:
        tuple: (first_name, last_name)
    """
    
    parts = full_name.strip().split()
    
    if len(parts) == 1:
        return parts[0], ''
    elif len(parts) == 2:
        return parts[0], parts[1]
    else:
        return parts[0], ' '.join(parts[1:])

def get_age_from_dob(dob):
    """
    Calculate age from date of birth
    
    Args:
        dob (str): Date of birth in format YYYY-MM-DD
    
    Returns:
        int: Age in years
    """
    
    from datetime import datetime
    
    try:
        birth_date = datetime.strptime(dob, '%Y-%m-%d')
        today = datetime.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age
    except:
        return None
