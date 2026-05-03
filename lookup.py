"""
Lookup Module
Phone and CNIC lookup functionality
"""

from database import Database
from utils import validate_phone, validate_cnic, normalize_phone, normalize_cnic

class PhoneLookup:
    def __init__(self, db=None):
        """Initialize phone lookup with database"""
        self.db = db if db else Database()
    
    def search(self, phone):
        """
        Search for a phone number in the database
        
        Args:
            phone (str): Phone number to search
        
        Returns:
            dict: Phone record if found, None otherwise
        """
        
        # Validate phone format
        if not validate_phone(phone):
            return None
        
        # Search in database
        result = self.db.search_phone(phone)
        
        if result:
            # Get associated CNIC if available
            cnic = result.get('associated_cnic')
            return {
                'phone': result['phone'],
                'owner_name': result['owner_name'],
                'provider': result['provider'],
                'status': result['status'],
                'verified': bool(result['verified']),
                'region': result.get('region', 'N/A'),
                'circle': result.get('circle', 'N/A'),
                'associated_cnic': cnic,
                'last_updated': result['last_updated']
            }
        
        return None
    
    def search_by_owner(self, owner_name):
        """Search for phone records by owner name"""
        # This would require additional database method
        pass
    
    def verify_phone(self, phone):
        """Verify if phone number exists and is valid"""
        return validate_phone(phone) and self.search(phone) is not None

class CnicLookup:
    def __init__(self, db=None):
        """Initialize CNIC lookup with database"""
        self.db = db if db else Database()
    
    def search(self, cnic):
        """
        Search for a CNIC number in the database
        
        Args:
            cnic (str): CNIC number to search
        
        Returns:
            dict: CNIC record if found, None otherwise
        """
        
        # Validate CNIC format
        if not validate_cnic(cnic):
            return None
        
        # Search in database
        result = self.db.search_cnic(cnic)
        
        if result:
            # Get associated phones
            associated_phones = self.db.get_associated_phones(cnic)
            
            return {
                'cnic': result['cnic'],
                'owner_name': result['owner_name'],
                'father_name': result.get('father_name', 'N/A'),
                'dob': result.get('dob', 'N/A'),
                'gender': result.get('gender', 'N/A'),
                'profession': result.get('profession', 'N/A'),
                'status': result['status'],
                'verified': bool(result['verified']),
                'associated_phones': associated_phones,
                'last_updated': result['last_updated']
            }
        
        return None
    
    def search_by_owner(self, owner_name):
        """Search for CNIC records by owner name"""
        # This would require additional database method
        pass
    
    def verify_cnic(self, cnic):
        """Verify if CNIC number exists and is valid"""
        return validate_cnic(cnic) and self.search(cnic) is not None

class ReverseLookup:
    def __init__(self, db=None):
        """Initialize reverse lookup service"""
        self.db = db if db else Database()
        self.phone_lookup = PhoneLookup(db)
        self.cnic_lookup = CnicLookup(db)
    
    def get_by_phone(self, phone):
        """Get CNIC details from phone number"""
        phone_record = self.phone_lookup.search(phone)
        
        if phone_record and phone_record.get('associated_cnic'):
            return self.cnic_lookup.search(phone_record['associated_cnic'])
        
        return None
    
    def get_by_cnic(self, cnic):
        """Get phone details from CNIC number"""
        cnic_record = self.cnic_lookup.search(cnic)
        
        if cnic_record and cnic_record.get('associated_phones'):
            phones = []
            for phone in cnic_record['associated_phones']:
                phone_record = self.phone_lookup.search(phone)
                if phone_record:
                    phones.append(phone_record)
            
            return phones
        
        return None
