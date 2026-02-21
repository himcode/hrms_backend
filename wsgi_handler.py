import sys
import traceback


_app = None
_error = None


def _init():
    global _app, _error
    try:
        import os
        from pathlib import Path

        project_root = str(Path(__file__).resolve().parent)
        if project_root not in sys.path:
            sys.path.insert(0, project_root)

        from dotenv import load_dotenv
        load_dotenv()

        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')

        from django.core.wsgi import get_wsgi_application
        _app = get_wsgi_application()
    except Exception:
        _error = traceback.format_exc()
        print(_error, file=sys.stderr)


_init()


def handler(environ, start_response):
    if _error:
        start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
        return [_error.encode('utf-8')]
    return _app(environ, start_response)


app = handler
