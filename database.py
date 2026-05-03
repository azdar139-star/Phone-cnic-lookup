"""
Database Module
Handles SQLite database operations for phone and CNIC records
"""

import sqlite3
import os
from datetime import datetime
from utils import normalize_phone, normalize_cnic

class Database:
    def __init__(self, db_path='data/phonecnic.db'):
        """Initialize database connection"""
        self.db_path = db_path
        
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        """Create database tables if they don't exist"""
        
        # Phone records table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS phone_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone TEXT UNIQUE NOT NULL,
                owner_name TEXT NOT NULL,
                provider TEXT,
                status TEXT DEFAULT 'active',
                verified BOOLEAN DEFAULT 0,
                region TEXT,
                circle TEXT,
                associated_cnic TEXT,
                last_updated TEXT,
                created_at TEXT
            )
        ''')
        
        # CNIC records table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cnic_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cnic TEXT UNIQUE NOT NULL,
                owner_name TEXT NOT NULL,
                father_name TEXT,
                dob TEXT,
                gender TEXT,
                profession TEXT,
                status TEXT DEFAULT 'active',
                verified BOOLEAN DEFAULT 0,
                last_updated TEXT,
                created_at TEXT
            )
        ''')
        
        # Associated phones table (for CNIC-Phone relationship)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS associated_phones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cnic TEXT NOT NULL,
                phone TEXT NOT NULL,
                FOREIGN KEY(cnic) REFERENCES cnic_records(cnic),
                FOREIGN KEY(phone) REFERENCES phone_records(phone),
                UNIQUE(cnic, phone)
            )
        ''')
        
        self.conn.commit()
    
    def add_phone_record(self, phone, owner_name, provider='Unknown', 
                        region='N/A', circle='N/A', associated_cnic=None):
        """Add or update a phone record"""
        phone = normalize_phone(phone)
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO phone_records 
                (phone, owner_name, provider, region, circle, associated_cnic, 
                 verified, status, last_updated, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (phone, owner_name, provider, region, circle, associated_cnic, 
                  1, 'active', now, now))
            
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error adding phone record: {e}")
            return False
    
    def add_cnic_record(self, cnic, owner_name, father_name='N/A', dob='N/A',
                       gender='N/A', profession='N/A'):
        """Add or update a CNIC record"""
        cnic = normalize_cnic(cnic)
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO cnic_records 
                (cnic, owner_name, father_name, dob, gender, profession,
                 verified, status, last_updated, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (cnic, owner_name, father_name, dob, gender, profession,
                  1, 'active', now, now))
            
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error adding CNIC record: {e}")
            return False
    
    def add_associated_phone(self, cnic, phone):
        """Add associated phone to CNIC"""
        cnic = normalize_cnic(cnic)
        phone = normalize_phone(phone)
        
        try:
            self.cursor.execute('''
                INSERT OR IGNORE INTO associated_phones (cnic, phone)
                VALUES (?, ?)
            ''', (cnic, phone))
            
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error adding associated phone: {e}")
            return False
    
    def search_phone(self, phone):
        """Search for a phone record"""
        phone = normalize_phone(phone)
        
        self.cursor.execute('''
            SELECT * FROM phone_records WHERE phone = ?
        ''', (phone,))
        
        row = self.cursor.fetchone()
        return dict(row) if row else None
    
    def search_cnic(self, cnic):
        """Search for a CNIC record"""
        cnic = normalize_cnic(cnic)
        
        self.cursor.execute('''
            SELECT * FROM cnic_records WHERE cnic = ?
        ''', (cnic,))
        
        row = self.cursor.fetchone()
        return dict(row) if row else None
    
    def get_associated_phones(self, cnic):
        """Get all phones associated with a CNIC"""
        cnic = normalize_cnic(cnic)
        
        self.cursor.execute('''
            SELECT phone FROM associated_phones WHERE cnic = ?
        ''', (cnic,))
        
        rows = self.cursor.fetchall()
        return [row[0] for row in rows]
    
    def get_statistics(self):
        """Get database statistics"""
        self.cursor.execute('SELECT COUNT(*) FROM phone_records')
        phone_count = self.cursor.fetchone()[0]
        
        self.cursor.execute('SELECT COUNT(*) FROM cnic_records')
        cnic_count = self.cursor.fetchone()[0]
        
        # Get database file size
        db_size = os.path.getsize(self.db_path) / (1024 * 1024)  # Convert to MB
        
        return {
            'total_phones': phone_count,
            'total_cnics': cnic_count,
            'db_size': f"{db_size:.2f}",
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def initialize_with_samples(self):
        """Initialize database with sample data"""
        
        # Sample phone records
        phone_samples = [
            ('03001234567', 'John Doe', 'Jazz', 'Karachi', 'South', '12345-6789012-3'),
            ('03111234567', 'Jane Smith', 'Zong', 'Lahore', 'Central', '12345-6789012-4'),
            ('03201234567', 'Ali Khan', 'Telenor', 'Islamabad', 'North', '12345-6789012-5'),
            ('03301234567', 'Fatima Ahmed', 'Warid', 'Multan', 'Central', '12345-6789012-6'),
            ('03001111111', 'Hassan Hassan', 'Jazz', 'Karachi', 'South', '12345-6789012-7'),
            ('03002222222', 'Ayesha Khan', 'Zong', 'Peshawar', 'North', '12345-6789012-8'),
            ('03003333333', 'Muhammad Ali', 'Telenor', 'Rawalpindi', 'North', '12345-6789012-9'),
            ('03004444444', 'Zainab Malik', 'Jazz', 'Lahore', 'Central', '12345-6789012-10'),
        ]
        
        for phone, name, provider, region, circle, cnic in phone_samples:
            self.add_phone_record(phone, name, provider, region, circle, cnic)
        
        # Sample CNIC records
        cnic_samples = [
            ('12345-6789012-3', 'John Doe', 'Ahmed Doe', '1980-05-15', 'M', 'Engineer'),
            ('12345-6789012-4', 'Jane Smith', 'David Smith', '1985-08-20', 'F', 'Doctor'),
            ('12345-6789012-5', 'Ali Khan', 'Hassan Khan', '1975-03-10', 'M', 'Businessman'),
            ('12345-6789012-6', 'Fatima Ahmed', 'Ahmed Siddiqui', '1990-12-25', 'F', 'Teacher'),
            ('12345-6789012-7', 'Hassan Hassan', 'Hassan Ali', '1988-06-30', 'M', 'Accountant'),
            ('12345-6789012-8', 'Ayesha Khan', 'Khan Malik', '1992-09-12', 'F', 'Software Developer'),
            ('12345-6789012-9', 'Muhammad Ali', 'Ali Ahmed', '1980-01-05', 'M', 'Lawyer'),
            ('12345-6789012-10', 'Zainab Malik', 'Malik Hassan', '1995-07-18', 'F', 'Student'),
        ]
        
        for cnic, name, father, dob, gender, profession in cnic_samples:
            self.add_cnic_record(cnic, name, father, dob, gender, profession)
        
        # Add associated phones
        for phone, name, _, _, _, cnic in phone_samples:
            self.add_associated_phone(cnic, phone)
        
        print("Sample data loaded successfully!")
    
    def close(self):
        """Close database connection"""
        self.conn.close()
    
    def __del__(self):
        """Destructor to close database connection"""
        try:
            self.close()
        except:
            pass
