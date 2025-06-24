#!/usr/bin/env python
"""
Web-based static files collection script for cPanel deployment.
Run this script to collect all static files for production.
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def main():
    """Collect static files for production"""
    try:
        # Set the settings module
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'globalsnus_crm.settings_production')
        
        # Setup Django
        django.setup()
        
        print("Starting static files collection...")
        
        # Collect static files
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
        
        print("✅ Static files collected successfully!")
        print("Static files are now available in the 'staticfiles' directory.")
        
    except Exception as e:
        print(f"❌ Error during static files collection: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
