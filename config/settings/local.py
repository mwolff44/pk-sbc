# -*- coding: utf-8 -*-
from .base import *

#  ######### DEBUG CONFIGURATION
DEBUG = True
#  ######### END DEBUG CONFIGURATION

#  ######### HOST CONFIGURATION
#  Add your IP and domain
ALLOWED_HOSTS = ['*', 'localhost', '127.0.0.1']
#  ######### END HOST CONFIGURATION

#  ######### SECRET CONFIGURATION
# Note: This key should only be used for development and testing.
SECRET_KEY = 'securitykeymustbechanged'
#  ######### END SECRET CONFIGURATION

#  ######### MANAGER CONFIGURATION
ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS
#  ######### END MANAGER CONFIGURATION

#  ######### DATABASE CONFIGURATION
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pyfreebilling',
        'USER': 'pyfreebilling',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1',
        'PORT': '',                      # Set to empty string for default.
    }
}
#  ######### END DATABASE CONFIGURATION

#  ######### DEV SPECIFIC
INSTALLED_APPS += (
    'django_extensions',
    'debug_toolbar',
    'pyfreebilling.urgencyfr.apps.UrgencyfrConfig',
)

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INTERNAL_IPS = ('10.0.3.27', )

RUNSERVERPLUS_SERVER_ADDRESS_PORT = '0.0.0.0:8000'
#  ######### END DEV SPECIFIC

#  ######### COUNTRY SPECIFIC
TIME_ZONE = 'Europe/Paris'
# LANGUAGE_CODE = 'it'
#  ######### END COUNTRY SPECIFIC

#  ######### SPECIFIC SETTINGS
OPENEXCHANGERATES_APP_ID = "Your API Key"

#  -- Nb days of CDR to show
PFB_NB_ADMIN_CDR = 3000
PFB_NB_CUST_CDR = 3000
#  ######### END SPECIFIC SETTINGS

#  ######### EMAIL CONFIGURATION
TEMPLATED_EMAIL_BACKEND = 'templated_email.backends.vanilla_django.TemplateBackend'
TEMPLATED_EMAIL_TEMPLATE_DIR = 'templated_email/'
TEMPLATED_EMAIL_FILE_EXTENSION = 'email'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = '%s Team <contact@%s>' % (PROJECT_NAME, 'companyname.com')
EMAIL_HOST = ''
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
#  EMAIL_USE_TLS = True
EMAIL_USE_TLS = True
EMAIL_SIGNATURE = ''
#  ######### END EMAIL CONFIGURATION

#  ADMIN_TOOLS_THEMING_CSS = 'css/theming.css'
