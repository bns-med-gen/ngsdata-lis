"""
WSGI config for lis project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lis_main.settings')

application = get_wsgi_application()
