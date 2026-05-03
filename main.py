#!/usr/bin/env python3
"""
Phone & CNIC Lookup Tool
Main Application Entry Point
"""

import sys
import argparse
from database import Database
from lookup import PhoneLookup, CnicLookup
from colorama import Fore, Back, Style, init

# Initialize colorama for colored output
init(autoreset=True)

class PhoneCnicLookupApp:
    def __init__(self):
        self.db = Database()
        self.phone_lookup = PhoneLookup(self.db)
        self.cnic_lookup = CnicLookup(self.db)
    
    def print_header(self):
        """Print application header"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}    📱 Phone & CNIC Lookup Tool v1.0.0")
        print(f"{Fore.CYAN}{'='*60}\n")
    
    def print_footer(self):
        """Print application footer"""
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    def search_phone(self, phone_number, verbose=False):
        """Search phone number"""
        print(f"\n{Fore.YELLOW}🔍 Searching for: {phone_number}")
        result = self.phone_lookup.search(phone_number)
        
        if result:
            print(f"\n{Fore.GREEN}✓ Record Found!")
            print(f"{Fore.WHITE}{'='*50}")
            print(f"Phone Number    : {Fore.CYAN}{result.get('phone', 'N/A')}")
            print(f"Owner Name      : {Fore.CYAN}{result.get('owner_name', 'N/A')}")
            print(f"Provider        : {Fore.CYAN}{result.get('provider', 'N/A')}")
            print(f"Status          : {Fore.CYAN}{result.get('status', 'N/A')}")
            print(f"Verified        : {Fore.CYAN}{'Yes' if result.get('verified') else 'No'}")
            print(f"Last Updated    : {Fore.CYAN}{result.get('last_updated', 'N/A')}")
            
            if result.get('associated_cnic'):
                print(f"Associated CNIC : {Fore.CYAN}{result.get('associated_cnic', 'N/A')}")
            
            if verbose:
                print(f"\n{Fore.YELLOW}Additional Details:")
                print(f"Region          : {Fore.CYAN}{result.get('region', 'N/A')}")
                print(f"Circle          : {Fore.CYAN}{result.get('circle', 'N/A')}")
            
            print(f"{Fore.WHITE}{'='*50}")
        else:
            print(f"{Fore.RED}✗ No record found for: {phone_number}")
    
    def search_cnic(self, cnic_number, verbose=False):
        """Search CNIC number"""
        print(f"\n{Fore.YELLOW}🔍 Searching for: {cnic_number}")
        result = self.cnic_lookup.search(cnic_number)
        
        if result:
            print(f"\n{Fore.GREEN}✓ Record Found!")
            print(f"{Fore.WHITE}{'='*50}")
            print(f"CNIC Number     : {Fore.CYAN}{result.get('cnic', 'N/A')}")
            print(f"Owner Name      : {Fore.CYAN}{result.get('owner_name', 'N/A')}")
            print(f"Father Name     : {Fore.CYAN}{result.get('father_name', 'N/A')}")
            print(f"Date of Birth   : {Fore.CYAN}{result.get('dob', 'N/A')}")
            print(f"Status          : {Fore.CYAN}{result.get('status', 'N/A')}")
            print(f"Verified        : {Fore.CYAN}{'Yes' if result.get('verified') else 'No'}")
            
            associated_phones = result.get('associated_phones', [])
            if associated_phones:
                print(f"Associated Phones: {Fore.CYAN}{', '.join(associated_phones)}")
            
            if verbose:
                print(f"\n{Fore.YELLOW}Additional Details:")
                print(f"Gender          : {Fore.CYAN}{result.get('gender', 'N/A')}")
                print(f"Profession      : {Fore.CYAN}{result.get('profession', 'N/A')}")
            
            print(f"{Fore.WHITE}{'='*50}")
        else:
            print(f"{Fore.RED}✗ No record found for: {cnic_number}")
    
    def show_stats(self):
        """Show database statistics"""
        stats = self.db.get_statistics()
        
        self.print_header()
        print(f"{Fore.CYAN}📊 Database Statistics")
        print(f"{Fore.WHITE}{'='*50}")
        print(f"Total Phone Records : {Fore.GREEN}{stats['total_phones']}")
        print(f"Total CNIC Records  : {Fore.GREEN}{stats['total_cnics']}")
        print(f"Database Size       : {Fore.GREEN}{stats['db_size']} MB")
        print(f"Last Updated        : {Fore.GREEN}{stats['last_updated']}")
        print(f"{Fore.WHITE}{'='*50}\n")
    
    def init_database(self):
        """Initialize database with sample data"""
        print(f"\n{Fore.YELLOW}Initializing database...")
        self.db.initialize_with_samples()
        print(f"{Fore.GREEN}✓ Database initialized successfully!\n")
    
    def interactive_mode(self):
        """Interactive menu mode"""
        self.print_header()
        
        while True:
            print(f"{Fore.CYAN}Select an option:")
            print(f"{Fore.WHITE}1. {Fore.CYAN}Search by Phone Number")
            print(f"{Fore.WHITE}2. {Fore.CYAN}Search by CNIC")
            print(f"{Fore.WHITE}3. {Fore.CYAN}View Database Statistics")
            print(f"{Fore.WHITE}4. {Fore.CYAN}Exit")
            
            choice = input(f"\n{Fore.YELLOW}Enter your choice (1-4): {Fore.WHITE}").strip()
            
            if choice == '1':
                phone = input(f"{Fore.YELLOW}Enter phone number: {Fore.WHITE}").strip()
                if phone:
                    self.search_phone(phone, verbose=True)
                else:
                    print(f"{Fore.RED}Invalid phone number!")
            
            elif choice == '2':
                cnic = input(f"{Fore.YELLOW}Enter CNIC number: {Fore.WHITE}").strip()
                if cnic:
                    self.search_cnic(cnic, verbose=True)
                else:
                    print(f"{Fore.RED}Invalid CNIC number!")
            
            elif choice == '3':
                self.show_stats()
            
            elif choice == '4':
                print(f"\n{Fore.CYAN}Thank you for using Phone & CNIC Lookup Tool!")
                print(f"{Fore.CYAN}Goodbye! 👋\n")
                break
            
            else:
                print(f"{Fore.RED}Invalid choice! Please try again.\n")
    
    def run(self):
        """Main application entry point"""
        parser = argparse.ArgumentParser(
            description='📱 Phone & CNIC Lookup Tool',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog='''
Examples:
  python main.py --phone "03001234567"
  python main.py --cnic "12345-6789012-3"
  python main.py --interactive
  python main.py --stats
            '''
        )
        
        parser.add_argument('-p', '--phone', type=str, help='Search by phone number')
        parser.add_argument('-c', '--cnic', type=str, help='Search by CNIC number')
        parser.add_argument('-i', '--interactive', action='store_true', help='Interactive mode')
        parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
        parser.add_argument('-s', '--stats', action='store_true', help='Show database statistics')
        parser.add_argument('--init-db', action='store_true', help='Initialize database')
        
        args = parser.parse_args()
        
        # If no arguments provided, show interactive mode
        if len(sys.argv) == 1:
            self.interactive_mode()
        
        # Handle database initialization
        elif args.init_db:
            self.init_database()
        
        # Handle statistics
        elif args.stats:
            self.show_stats()
        
        # Handle phone search
        elif args.phone:
            self.search_phone(args.phone, args.verbose)
        
        # Handle CNIC search
        elif args.cnic:
            self.search_cnic(args.cnic, args.verbose)
        
        # Handle interactive mode
        elif args.interactive:
            self.interactive_mode()
        
        else:
            parser.print_help()

def main():
    try:
        app = PhoneCnicLookupApp()
        app.run()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Operation cancelled by user.")
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
