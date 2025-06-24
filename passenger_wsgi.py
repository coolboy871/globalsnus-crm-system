import os
import sys

# Add project base directory to sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# Set environment variable to use local settings.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'globalsnus_crm.settings')

try:
    from globalsnus_crm.wsgi import application
except ImportError as e:
    def application(environ, start_response):
        status = '200 OK'
        headers = [('Content-type', 'text/html')]
        start_response(status, headers)
        error_msg = f"""
        <html>
        <head><title>Django Import Error</title></head>
        <body>
        <h1>Django Import Error</h1>
        <p>Error: {str(e)}</p>
        <p>Current directory: {BASE_DIR}</p>
        <p>Python path: {sys.path}</p>
        <p>Directory contents: {os.listdir(BASE_DIR)}</p>
        </body>
        </html>
        """
        return [error_msg.encode('utf-8')]
