#!/usr/bin/env python
"""
Script to install Python packages from requirements.txt using pip
"""
import os
import sys
import subprocess

def install_requirements():
    try:
        print("Starting package installation...")
        
        # Get the directory where this script is located
        current_dir = os.path.dirname(os.path.abspath(__file__))
        requirements_file = os.path.join(current_dir, 'requirements.txt')
        
        if not os.path.exists(requirements_file):
            print(f"❌ Error: requirements.txt not found in {current_dir}")
            return
            
        print(f"📦 Installing packages from: {requirements_file}")
        
        # Use pip to install requirements
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements_file])
        
        print("✅ Package installation completed successfully!")
        
        # Verify mysqlclient installation specifically
        try:
            import mysqlclient
            print("✅ mysqlclient package installed successfully!")
        except ImportError:
            print("⚠️ Warning: mysqlclient package not found. You may need to install it manually.")
            print("Try: pip install mysqlclient==2.2.0")
        
    except Exception as e:
        print(f"❌ Error during package installation: {str(e)}")
        print("\nTroubleshooting steps:")
        print("1. Make sure you have write permissions in the Python packages directory")
        print("2. Try installing packages individually using pip")
        print("3. Contact your hosting provider for assistance with package installation")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    install_requirements()
