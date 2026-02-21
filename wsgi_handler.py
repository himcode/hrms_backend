import sys
import os
import traceback
import logging
from pathlib import Path

# Configure logging early
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Set up paths
project_root = str(Path(__file__).resolve().parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

logger.info("Initializing Django WSGI application")
logger.info(f"Project root: {project_root}")
logger.info(f"Python version: {sys.version}")

# Log environment info
logger.info(f"Environment: VERCEL={os.environ.get('VERCEL', 'Not set')}")
logger.info(f"Environment: NODE_ENV={os.environ.get('NODE_ENV', 'Not set')}")

# Load environment variables
from dotenv import load_dotenv
load_dotenv()
logger.info("Loaded environment variables from .env")

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
logger.info("DJANGO_SETTINGS_MODULE set to api.settings")

# Log database config
db_host = os.environ.get('PGHOST', 'Not set')
db_name = os.environ.get('PGDATABASE', 'Not set')
db_user = os.environ.get('PGUSER', 'Not set')
logger.info(f"Database config - Host: {db_host}, DB: {db_name}, User: {db_user}")

if not os.environ.get('PGPASSWORD'):
    logger.warning("PGPASSWORD not set - database connection may fail")
if not os.environ.get('PGHOST'):
    logger.warning("PGHOST not set - using localhost as default")

# Initialize Django
try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    logger.info("Django WSGI application initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Django WSGI application:\n{traceback.format_exc()}")
    raise

# Vercel handler - directly use the Django WSGI application
app = application
