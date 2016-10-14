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

#IMPORT SETTINGS
#===============
from base import *

# make tests faster
# False : test will make the test database be created using syncdb
SOUTH_TESTS_MIGRATE = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3'
    }
}

ALLOWED_HOSTS = ['*']

SECRET_KEY = 'securitykeymustbechanged'  # very important - put your key for security - any string

TIME_ZONE = 'Europe/Paris'

# LANGUAGE_CODE = 'it'

OPENEXCHANGERATES_APP_ID = "Your API Key"

#-- Nb days of CDR to show
PFB_NB_ADMIN_CDR = 3
PFB_NB_CUST_CDR = 30

# EMAIL SETUP
TEMPLATED_EMAIL_BACKEND = 'templated_email.backends.vanilla_django.TemplateBackend'
TEMPLATED_EMAIL_TEMPLATE_DIR = 'templated_email/'
TEMPLATED_EMAIL_FILE_EXTENSION = 'email'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = ''
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
#EMAIL_USE_TLS = True
EMAIL_USE_SSL = True
EMAIL_SIGNATURE = ''
