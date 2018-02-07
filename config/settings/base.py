# Copyright 2013 Mathias WOLFF
# This file is part of pyfreebilling.
#
# pyfreebilling is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfreebilling is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfreebilling.  If not, see <http://www.gnu.org/licenses/>

# Django settings for pyfreebilling project.
from __future__ import absolute_import, unicode_literals

# SECRET_KEY = 'securitykeymustbechanged
#import django
#django.setup()

from os.path import abspath, basename, dirname, join, normpath
from sys import path


#  ######### PATH CONFIGURATION
# Absolute filesystem path to the config directory:
CONFIG_ROOT = dirname(dirname(abspath(__file__)))

# Absolute filesystem path to the project directory:
PROJECT_ROOT = dirname(CONFIG_ROOT)
APP_DIR = normpath(join(PROJECT_ROOT, 'pyfreebilling'))
APPS_DIR = APP_DIR

# Absolute filesystem path to the django repo directory:
DJANGO_ROOT = PROJECT_ROOT

# Project name:
PROJECT_NAME = basename(PROJECT_ROOT).capitalize()

# Project folder:
PROJECT_FOLDER = basename(PROJECT_ROOT)

# Project domain:
# PROJECT_DOMAIN = '%s.com' % PROJECT_NAME.lower()

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
path.append(CONFIG_ROOT)
#  ######### END PATH CONFIGURATION

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pyfreebilling',
        'USER': 'pyfreebilling',
        'PASSWORD' : 'password',
        'HOST': '127.0.0.1',
        'PORT': '',  # Set to empty string for default.
    }
}

#  ######### APP CONFIGURATION
DJANGO_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    #'admin_tools.dashboard ,
    #'jet.dashboard ,
    #'jet',
    'django.contrib.admin',
    'django.contrib.admindocs',
)

THIRD_PARTY_APPS = (
    'import_export',
    'admin_honeypot',
    'chroniker',
    'axes',
    'qsstats',
    'django_countries',
    'datetimewidget',
    'bootstrap3',
    'currencies',
    'django_tables2',
    'bootstrap_pagination',
    'mathfilters',
    'crispy_forms',
    'solo',
    'django_filters',
    'migrate_sql',
)

PROJECT_APPS = (
    'pyfreebilling.pyfreebill.apps.PyfreebillConfig',
    'pyfreebilling.did.apps.DidConfig',
    'pyfreebilling.switch.apps.SwitchConfig',
    'pyfreebilling.customerdirectory.apps.CustomerDirectoryConfig',
    'pyfreebilling.customerportal.apps.CustomerPortalConfig',
    'pyfreebilling.normalizationrule.apps.NormalizationRuleConfig',
    'pyfreebilling.cdr.apps.CDRConfig',
    'pyfreebilling.antifraud.apps.AntiFraudConfig',
)

EXTENSION_APPS = (
    #'extensions.authtools',
    #'extensions.django_rq',
    #'extensions.rq_scheduler',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS + EXTENSION_APPS
#  ######### END APP CONFIGURATION

#  ######### MIDDLEWARE CONFIGURATION
MIDDLEWARE_CLASSES = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
#  ######### END MIDDLEWARE CONFIGURATION

#  ######### FIXTURE CONFIGURATION
FIXTURE_DIRS = (
    normpath(join(APP_DIR, 'fixtures')),
)
#  ######### END FIXTURE CONFIGURATION

# ######### GENERAL CONFIGURATION
# https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
TIME_ZONE = 'Europe/Paris'

# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True
# ######### END GENERAL CONFIGURATION

#  ######### TEMPLATE CONFIGURATION
TEMPLATES = [
    {
        'BACKEND' : 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            normpath(join(APP_DIR, 'templates')),
            normpath(join(APP_DIR, 'extensions')),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'currencies.context_processors.currencies',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                'admin_tools.template_loaders.Loader',
            ],
            'string_if_invalid': 'NULL',
        },
    },
]
#  ######### END TEMPLATE CONFIGURATION

#  ######### PASSWORD CONFIGURATION

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 11,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ########## END PASSWORD CONFIGURATION

#  ######### LOCALE FILE CONFIGURATION
LOCALE_PATHS = (
    normpath(join(APP_DIR, 'locale')),
)
LANGUAGE_CODE = 'en_US'
#  ######### END LOCALE FILE CONFIGURATION

#  ######### MEDIA CONFIGURATION
MEDIA_ROOT = normpath(join(PROJECT_ROOT, 'media'))

MEDIA_URL = '/media/'
#  ######### END MEDIA CONFIGURATION

#  ######### STATIC FILE CONFIGURATION
STATIC_ROOT = normpath(join(PROJECT_ROOT, 'staticfiles'))

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    normpath(join(APP_DIR, 'static')),
)

STATICFILES_FINDERS_IGNORE = [
    '*.scss',
    '*.coffee',
    '*.map',
    '*.html',
    '*.txt',
    '*tests*',
    '*uncompressed*',
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
#  ######### END STATIC FILE CONFIGURATION

# ######### URL CONFIGURATION
ROOT_URLCONF = 'config.urls'
#  ######### END URL CONFIGURATION


#  ######### LOGIN/LOGOUT CONFIGURATION
# LOGIN_REDIRECT_URL = '/'
# LOGIN_URL = '/login/'
# LOGOUT_URL = '/logout/'
#  ######### END LOGIN/LOGOUT CONFIGURATION


#  ######### WSGI CONFIGURATION
WSGI_APPLICATION = 'config.wsgi.application'
#  ######### END WSGI CONFIGURATION


#  ######### USER MODEL CONFIGURATION
AUTH_USER_MODEL = 'auth.User'
#  ######### END USER MODEL CONFIGURATION


#  ######### TESTING CONFIGURATION
TEST_RUNNER = 'django.test.runner.DiscoverRunner'
#  ######### END TESTING CONFIGURATION

#  ######### LOGGING CONFIGURATION
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'production_only': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'development_only': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)-8s [%(name)s:%(lineno)s] %(message)s',
            'datefmt': '%m/%d/%Y %H:%M:%S',
        },
        'simple': {
            'format': '%(levelname)-8s [%(name)s:%(lineno)s] %(message)s',
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'default': {
            'level': 'DEBUG',
            'class': 'config.lib.colorstreamhandler.ColorStreamHandler',
        },
        'console_dev': {
            'level': 'DEBUG',
            'filters': ['development_only'],
            'class': 'config.lib.colorstreamhandler.ColorStreamHandler',
            'formatter': 'simple',
        },
        'console_prod': {
            'level': 'INFO',
            'filters': ['production_only'],
            'class': 'config.lib.colorstreamhandler.ColorStreamHandler',
            'formatter': 'simple',
        },
        # 'file_log': {
        #     'level': 'DEBUG',
        #     'filters': ['development_only'],
        #     'class': 'logging.handlers.RotatingFileHandler',
        #     'filename': join(DJANGO_ROOT, 'logs/log.log'),
        #     'maxBytes': 1024 * 1024,
        #     'backupCount': 3,
        #     'formatter': 'verbose',
        # },
        # 'file_sql': {
        #     'level': 'DEBUG',
        #     'filters': ['development_only'],
        #     'class': 'logging.handlers.RotatingFileHandler',
        #     'filename': join(DJANGO_ROOT, 'logs/sql.log'),
        #     'maxBytes': 1024 * 1024,
        #     'backupCount': 3,
        #     'formatter': 'verbose',
        # },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['production_only'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
    },
    # Catch-all modules that use logging
    # Writes to console and file on development, only to console on production
    'root': {
        'handlers': ['console_dev', 'console_prod'],
        'level': 'DEBUG',
    },
    'loggers': {
        # Write all SQL queries to a file
        # 'django.db.backends': {
        #     'handlers': ['file_sql'],
        #     'level': 'DEBUG',
        #     'propagate': False,
        # },
        # Email admins when 500 error occurs
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}
#  ######### END LOGGING CONFIGURATION


#  ######### SECURITY CONFIGURATION
SECRET_KEY = 'securitykeymustbechanged'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_FRAME_DENY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 86400
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'DENY'
AXES_LOGIN_FAILURE_LIMIT = 5
ADMIN_HONEYPOT_EMAIL_ADMINS = False
#  ######### END SECURITY CONFIGURATION

# -----------------------------------
COUNTRIES_FLAG_PATH = 'flags/%s.png'

# ADMIN SETTINGS
BOOTSTRAP_ADMIN_SIDEBAR_MENU = True
ADMIN_SITE_NAME = 'PyFreeBilling'
ADMIN_SITE_TITLE = 'PyFreeBilling administration'
ADMIN_SITE_DESCRIPTION = 'Softswitch and billing application'
ADMIN_SITE_LOGO_HTML = '<div id="myproject-logo hidden-phone">Logo</div>'
ADMIN_DISABLE_APP_INDEX = 'True'
ADMIN_TOOLS_THEMING_CSS = 'css/theming.css'
ADMIN_TOOLS_MENU = 'config.menu.CustomMenu'

# ---------
# Currency settings
# ---------
CURRENCIES_BASE = 'EUR'

# ----------
# Chroniker
# ----------
CHRONIKER_USE_PID = False
CHRONIKER_SELECT_FOR_UPDATE = False
CHRONIKER_CHECK_LOCK_FILE = False


# -- Nb days of CDR to show
PFB_NB_ADMIN_CDR = 3
PFB_NB_CUST_CDR = 30

# -----#

# try:
#     from .local_settings import *
# except ImportError:
#     pass

# -----#


# --- Import export settings
IMPORT_EXPORT_SKIP_ADMIN_LOG = True

# -----
# -- Upload settings
FILE_UPLOAD_MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024
FILE_UPLOAD_TEMP_DIR = '/tmp'
# FILE_UPLOAD_PERMISSIONS = 0644
# FILE_UPLOAD_DIRECTORY_PERMISSIONS
# FILE_UPLOAD_HANDLERS

# Crispy forms
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Location of root django.contrib.admin URL
HONEYPOT_URL = r'^admin/'
ADMIN_URL = r'^extranet/'

# -------------------------#
# ANTIFRAUD SYSTEM SETTINGS
# general settings
antifraud_activate = False # to activate threshold antifraud system, set to True
antifraud_activate_sip_blocking = False # mettre a YES pour activer le blocage sur seuil
antifraud_activate_customer = False # mettre a YES pour activer l'antifraude sur les comptes clients
antifraud_activate_customer_force = False # To force antifraud system for all customers using default settings, set to YES
antifraud_activate_sipaccount = False # mettre a YES pour activer l'antifraude sur les comptes SIP

# customer account default settings
antifraud_cust_amount_alert = 100 # valeur en monnaie de consommation maximum d un compte client declenchant une alerte
antifraud_cust_minutes_alert = 10000 # valeur en minutes de consommation maximum d un compte client declenchant une alerte
antifraud_cust_amount_block = 200 # valeur en monnaie de consommation maximum d un compte client declenchant un blocage
antifraud_cust_minutes_block = 20000 # valeur en minutes de consommation maximum d un compte client declenchant un blocage

# SIP account default settings
antifraud_sip_amount_alert = 100 # valeur en monnaie de consommation maximum d un compte client declenchant une alerte
antifraud_sip_minutes_alert = 10000 # valeur en minutes de consommation maximum d un compte client declenchant une alerte
antifraud_sip_amount_block = 200 # valeur en monnaie de consommation maximum d un compte client declenchant un blocage
antifraud_sip_minutes_block = 20000 # valeur en minutes de consommation maximum d un compte client declenchant un blocage
# -------------------------#
