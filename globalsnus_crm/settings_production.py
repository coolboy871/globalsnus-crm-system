# This file is deprecated since we are reverting back to localhost development.
# You can delete this file safely.

"""
Production settings for globalsnus_crm project on cPanel.
"""

from .settings import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Update allowed hosts for your domain
ALLOWED_HOSTS = [
    'halfcrescentdesign.com',
    'www.halfcrescentdesign.com',
    '*.halfcrescentdesign.com',
    'localhost',
    '127.0.0.1'
]

# Database configuration for MySQL (cPanel)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'globalsnuscrm'),
        'USER': os.environ.get('DB_USER', 'globalsnuscrm_admin'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'global1111snus+7555asad'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}

# Security settings for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Static files settings for cPanel
STATIC_URL = '/globalsnuscrm/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files settings for cPanel
MEDIA_URL = '/globalsnuscrm/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Additional static files directories
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Logging configuration for production
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'django_errors.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# Use a secure secret key from environment variable
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-8=y%9zmnjs5y_6k_yqhxjhd^!1pax$yq_j*ho-gn^qqzmcvec8')

# Session security
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
