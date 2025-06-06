"""
ASGI config for project_name project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

environment = os.environ.get('ENVIRONMENT', 'development')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_name.settings.{}".format(environment))
application = get_asgi_application()
