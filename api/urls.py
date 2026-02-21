import os
import logging
from django.http import JsonResponse
from django.urls import path, include

logger = logging.getLogger(__name__)


def health(request):
    logger.info("Health check requested")
    return JsonResponse({
        "status": "ok",
        "message": "HRMS Backend API is running",
        "environment": os.environ.get('VERCEL', 'local'),
    })


def debug_info(request):
    """Debug endpoint - shows environment and database config"""
    logger.info("Debug info requested")
    
    # Check environment variables
    db_password_set = bool(os.environ.get('PGPASSWORD'))
    
    info = {
        "status": "ok",
        "environment": {
            "VERCEL": os.environ.get('VERCEL', 'Not set'),
            "DEBUG": os.environ.get('DEBUG', 'Not set'),
            "PGHOST": os.environ.get('PGHOST', 'Not set'),
            "PGDATABASE": os.environ.get('PGDATABASE', 'Not set'),
            "PGUSER": os.environ.get('PGUSER', 'Not set'),
            "PGPASSWORD": 'Set' if db_password_set else 'Not set',
            "PGPORT": os.environ.get('PGPORT', 'Not set'),
        }
    }
    
    # Check for missing critical variables
    missing = []
    if not os.environ.get('PGHOST'):
        missing.append('PGHOST')
    if not os.environ.get('PGDATABASE'):
        missing.append('PGDATABASE')
    if not os.environ.get('PGUSER'):
        missing.append('PGUSER')
    if not os.environ.get('PGPASSWORD'):
        missing.append('PGPASSWORD')
    
    if missing:
        info['warnings'] = [f"Missing environment variables: {', '.join(missing)}"]
    
    return JsonResponse(info)


api_patterns = [
    path('health/', health, name='health'),
    path('debug/', debug_info, name='debug'),
    path('employees/', include('employees.urls')),
    path('attendance/', include('attendance.urls')),
]

urlpatterns = [
    path('', health, name='root'),
    path('api/', include(api_patterns)),
]
