#!/usr/bin/env python
"""
Web-based migration script for cPanel deployment without terminal access.
Run this script by accessing it through your web browser or executing it via cPanel file manager.
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def main():
    """Run database migrations and create superuser"""
    try:
        # Set the settings module
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'globalsnus_crm.settings_production')
        
        # Setup Django
        django.setup()
        
        print("Starting database migration...")
        
        # Run migrations
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Database migrations completed successfully!")
        
        # Create superuser if it doesn't exist
        from django.contrib.auth.models import User
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@globalsnuscrm.com',
                password='admin123'  # Change this password after first login!
            )
            print("✅ Superuser 'admin' created successfully!")
            print("⚠️  Default password is 'admin123' - CHANGE THIS IMMEDIATELY!")
        else:
            print("ℹ️  Superuser already exists.")
        
        print("\n🎉 Setup completed successfully!")
        print("You can now access the admin panel at: /admin")
        print("Username: admin")
        print("Password: admin123 (CHANGE THIS!)")
        
    except Exception as e:
        print(f"❌ Error during setup: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
