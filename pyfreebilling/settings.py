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

import os
# Django settings for pyfreebilling project.


DEBUG = False
TEMPLATE_DEBUG = DEBUG

SETTINGS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SETTINGS_DIR)

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pyfreebilling',
        'USER': 'pyfreebilling',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1',
        'PORT': '',  # Set to empty string for default.
    }
}

# APPLICATION_DIR = os.path.dirname(globals()['__file__'])

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
# MEDIA_ROOT = os.path.join(APPLICATION_DIR, 'media')

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

LOCALE_PATHS = (
    os.path.join(PROJECT_DIR, 'locale'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '&mr1sl68uoiwgbdb6ax$44-$(0=_c9^)s@!g1!v&wohgkgemx6'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
        'django.template.loaders.eggs.Loader',
    )),
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'request.middleware.RequestMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'djangosecure.middleware.SecurityMiddleware',
    'axes.middleware.FailedLoginMiddleware',
    # For django < 1.6
    'yawdadmin.middleware.PopupMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
)

ROOT_URLCONF = 'pyfreebilling.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'pyfreebilling.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
    # "/usr/local/venv/pyfreebilling/templates",
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'pyfreebill',
    'switch',
    'customerportal',
    'yawdadmin',
    'import_export',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.comments',
    'admin_honeypot',
    'django_iban',
    'chroniker',
    'common',
    'clear_cache',
    'axes',
    'qsstats',
    'django.contrib.admin',
    'south',
    'cities_light',
    'django_countries',
    'country_dialcode',
    'database_size',
    'did',
    'simple_import',
    'sysmon',
    'request',
    'datetimewidget',
    'bootstrap3',
    'currencies',
    'djangosecure',
    'country_block',
    'django_tables2',
    'bootstrap_toolkit',
    'bootstrap_pagination',
    'mathfilters',
    'dbbackup',
    'crispy_forms',
    #'django_extensions',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# AUTH - DJANGO 1.6
# AUTH_USER_MODEL = 'pyfreebill.CustomUser'
AUTH_USER_MODEL = 'auth.User'


# SECURITY - ADJUST YOURS PARAMETERS


# AXES_LOGIN_FAILURE_LIMIT: The number of login attempts allowed before a record is created for the failed logins. Default: 3
AXES_LOGIN_FAILURE_LIMIT = 5
# AXES_LOCK_OUT_AT_FAILURE: After the number of allowed login attempts are exceeded, should we lock out this IP (and optional user agent)? Default: True

# AXES_USE_USER_AGENT: If True, lock out / log based on an IP address AND a user agent. This means requests from different user agents but from the same IP are treated differently. Default: False

# AXES_COOLOFF_TIME: If set, defines a period of inactivity after which old failed login attempts will be forgotten. Can be set to a python timedelta object or an integer. If an integer, will be interpreted as a number of hours. Default: None

# AXES_LOGGER: If set, specifies a logging mechanism for axes to use. Default: 'axes.watch_login'

# AXES_LOCKOUT_TEMPLATE: If set, specifies a template to render when a user is locked out. Template receives cooloff_time and failure_limit as context variables. Default: None

# AXES_LOCKOUT_URL: If set, specifies a URL to redirect to on lockout. If both AXES_LOCKOUT_TEMPLATE and AXES_LOCKOUT_URL are set, the template will be used. Default: None

# AXES_VERBOSE: If True, you'll see slightly more logging for Axes. Default: True


# -----------------------------------
# For the flags head over to http://www.famfamfam.com/lab/icons/flags/ and download the ISO 3166-1 alpha-2 country code flag package. Add a 'flags' directory to your media root and copy the .gif flags there.
# COUNTRIES_FLAG_PATH = '<path relative to media root>flags/%s.png' Specify directory
COUNTRIES_FLAG_PATH = 'flags/%s.png'

# YAWD ADMIN SETTINGS
ADMIN_SITE_NAME = 'PyFreeBilling'
ADMIN_SITE_DESCRIPTION = 'Softswitch and billing application'
# ADMIN_SITE_LOGO_HTML = '<div id="myproject-logo hidden-phone">Logo</div>'
ADMIN_DISABLE_APP_INDEX = 'True'


# ----------
# django-cities-light
# ----------
SOUTH_MIGRATION_MODULES = {
    'cities_light': 'cities_light.south_migrations',
}

# ----------
# Chroniker
# ----------
CHRONIKER_USE_PID = False
CHRONIKER_SELECT_FOR_UPDATE = False
CHRONIKER_CHECK_LOCK_FILE = False

# SECURING SITE ACCESS
ADMIN_HONEYPOT_EMAIL_ADMINS = False

# ----------
# Django Secure
# ----------
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
# CSRF_COOKIE_SECURE = True

# EMAIL SETUP
# TEMPLATED_EMAIL_BACKEND = 'templated_email.backends.vanilla_django.TemplateBackend'
# TEMPLATED_EMAIL_TEMPLATE_DIR = 'templated_email/'
# TEMPLATED_EMAIL_FILE_EXTENSION = 'email'
#
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = ''
# EMAIL_PORT = 587
# EMAIL_HOST_USER = ''
# EMAIL_HOST_PASSWORD = ''
# #EMAIL_USE_TLS = True
# EMAIL_USE_SSL = True
# EMAIL_SIGNATURE = 'PyFreeBilling'

# ------
# -- Nb days of CDR to show
PFB_NB_ADMIN_CDR = 3
PFB_NB_CUST_CDR = 30

# -----#

try:
    from .local_settings import *
except ImportError:
    pass

# -----#

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

# -- dbbackup settings
DBBACKUP_SERVER_NAME = 'pyfreebilling'
# DBBACKUP_CLEANUP_KEEP = 10
FORCE_ENGINE = 'postgres'
# DBBACKUP_POSTGRESQL_BACKUP_COMMANDS = 'pg_dump --username=pyfreebilling --host=localhost pyfreebilling'
DBBACKUP_BACKUP_DIRECTORY = 'backups'
DBBACKUP_SERVER_NAME = 'pyfreebilling'
DBBACKUP_SEND_EMAIL = True
DBBACKUP_GPG_ALWAYS_TRUST = False
DBBACKUP_GPG_RECIPIENT = None
# - FTP
# DBBACKUP_STORAGE = 'dbbackup.storage.ftp_storage'
# DBBACKUP_FTP_HOST = 'ftp.host'
# DBBACKUP_FTP_USER = 'user, blank if anonymous'
# DBBACKUP_FTP_PASSWORD = 'password, can be blank'
# DBBACKUP_FTP_PATH = 'path, blank for default'
