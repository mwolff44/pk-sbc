DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3'
    }
}

INSTALLED_APPS = (
    'pyfreebill',
    'switch',
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
#    'djangosecure',
    'django_iban',
    'chroniker',
    'common',
    'clear_cache',
    'axes',
    'qsstats',
    'chartjs',
    'django.contrib.admin',
    'south',
    'django_countries',
    'country_dialcode',
)