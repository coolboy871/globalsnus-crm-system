#!/usr/bin/env python
"""
Database connection test script for cPanel deployment.
Run this script to verify database connectivity.
"""

import os
import sys
import django
from django.db import connection

def main():
    """Test database connection"""
    try:
        # Set the settings module
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'globalsnus_crm.settings_production')
        
        # Setup Django
        django.setup()
        
        print("Testing database connection...")
        
        # Try to establish database connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        
        if result[0] == 1:
            print("✅ Database connection successful!")
            print("\nDatabase Configuration:")
            print(f"Engine: {connection.settings_dict['ENGINE']}")
            print(f"Name: {connection.settings_dict['NAME']}")
            print(f"User: {connection.settings_dict['USER']}")
            print(f"Host: {connection.settings_dict['HOST']}")
            print(f"Port: {connection.settings_dict['PORT']}")
        
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        print("\nTroubleshooting steps:")
        print("1. Verify database credentials in settings_production.py")
        print("2. Check if MySQL server is running")
        print("3. Ensure database user has proper permissions")
        print("4. Verify MySQL host allows connections from your web server")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
