"""
WSGI config for Billing project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""
import os
import sys
from django.core.wsgi import get_wsgi_application
from site import addsitedir

# Path to your project directory
PROJECT_DIR = 'C:/Apache24/htdocs/Billing/'

# Add the project directory to sys.path
sys.path.append(PROJECT_DIR)

# Path to the virtual environment's site-packages directory
VIRTUAL_ENV_SITE_PACKAGES = 'C:/Python/BillingEnv/Lib/site-packages'

# Add the virtual environment's site-packages directory
addsitedir(VIRTUAL_ENV_SITE_PACKAGES)

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ['DJANGO_SETTINGS_MODULE'] = 'Billing.settings'

# Get the WSGI application
application = get_wsgi_application()