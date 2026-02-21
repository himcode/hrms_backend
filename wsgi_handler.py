import sys
import traceback
import logging
import os

# Configure logging early
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

_app = None
_error = None


def _init():
    global _app, _error
    try:
        from pathlib import Path

        project_root = str(Path(__file__).resolve().parent)
        if project_root not in sys.path:
            sys.path.insert(0, project_root)

        logger.info("Initializing Django WSGI application")
        logger.info(f"Project root: {project_root}")
        logger.info(f"Python version: {sys.version}")

        # Log environment info
        logger.info(f"Environment: VERCEL={os.environ.get('VERCEL', 'Not set')}")
        logger.info(f"Environment: NODE_ENV={os.environ.get('NODE_ENV', 'Not set')}")
        
        from dotenv import load_dotenv
        load_dotenv()
        logger.info("Loaded environment variables from .env")

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

        from django.core.wsgi import get_wsgi_application
        _app = get_wsgi_application()
        logger.info("Django WSGI application initialized successfully")
    except Exception:
        _error = traceback.format_exc()
        logger.error(f"Failed to initialize Django WSGI application:\n{_error}")
        print(_error, file=sys.stderr)


_init()


def handler(environ, start_response):
    if _error:
        error_response = f"Failed to load Django:\n{_error}"
        logger.error(f"Handler called with initialization error: {error_response}")
        start_response('500 Internal Server Error', [
            ('Content-Type', 'text/plain'),
            ('X-Error-Info', 'Django initialization failed')
        ])
        return [error_response.encode('utf-8')]
    
    try:
        return _app(environ, start_response)
    except Exception as e:
        error_msg = f"Error processing request: {traceback.format_exc()}"
        logger.error(error_msg)
        start_response('500 Internal Server Error', [
            ('Content-Type', 'text/plain'),
            ('X-Error-Info', 'Request processing failed')
        ])
        return [error_msg.encode('utf-8')]


app = handler
