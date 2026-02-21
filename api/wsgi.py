import os
import sys
from pathlib import Path

# Ensure project root is in Python path (needed for Vercel Lambda)
project_root = str(Path(__file__).resolve().parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')

from django.core.wsgi import get_wsgi_application
app = get_wsgi_application()
handler = app
