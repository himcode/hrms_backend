import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

logger.info("Loading environment variables...")
load_dotenv()
logger.info("Environment variables loaded")

BASE_DIR = Path(__file__).resolve().parent.parent
logger.info(f"BASE_DIR: {BASE_DIR}")

# Log important environment variables (without exposing secrets)
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'strong_ethara_ai')
if os.environ.get('DJANGO_SECRET_KEY'):
    logger.info("DJANGO_SECRET_KEY is set")
else:
    logger.warning("DJANGO_SECRET_KEY not set - using default value")

DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
logger.info(f"DEBUG mode: {DEBUG}")

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '.vercel.app']

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'corsheaders',
    'rest_framework',
    'employees',
    'attendance',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'https://hrms-frontend-1nohiioap-himcodes-projects-2e0d79cd.vercel.app',
]
CORS_ALLOW_ALL_ORIGINS = os.environ.get('CORS_ALLOW_ALL', 'False').lower() == 'true'

ROOT_URLCONF = 'api.urls'
WSGI_APPLICATION = 'api.wsgi.app'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('PGDATABASE', 'neondb'),
        'USER': os.environ.get('PGUSER', ''),
        'PASSWORD': os.environ.get('PGPASSWORD', ''),
        'HOST': os.environ.get('PGHOST', 'localhost'),
        'PORT': os.environ.get('PGPORT', '5432'),
        'OPTIONS': {
            'sslmode': os.environ.get('PGSSLMODE', 'require'),
        },
        'CONN_MAX_AGE': 0,
        'CONN_HEALTH_CHECKS': True,
    }
}

# Log database configuration (without passwords)
logger.info(f"Database Engine: {DATABASES['default']['ENGINE']}")
logger.info(f"Database Name: {DATABASES['default']['NAME']}")
logger.info(f"Database Host: {DATABASES['default']['HOST']}")
logger.info(f"Database Port: {DATABASES['default']['PORT']}")
logger.info(f"Database User: {DATABASES['default']['USER']}")
if os.environ.get('PGPASSWORD'):
    logger.info("Database Password: Set")
else:
    logger.warning("Database Password: NOT SET")
logger.info(f"Database SSL Mode: {DATABASES['default']['OPTIONS']['sslmode']}")

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = False
USE_TZ = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
