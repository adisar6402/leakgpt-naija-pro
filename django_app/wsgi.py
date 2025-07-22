"""
WSGI config for LeakGPT Django app
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_app.settings')

django_application = get_wsgi_application()