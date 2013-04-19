import os
import sys
import site

DIRS = ['/usr/local/venv/trunk/lib/python2.7/site-packages']

for directory in DIRS:
  site.addsitedir(directory)
sys.path.insert(0,directory)

root = os.path.join(os.path.dirname(__file__))

#sys.path.append('/usr/local/venv/pyfreebilling')

sys.path.insert(0,root)
os.environ['DJANGO_SETTINGS_MODULE'] = 'pyfreebilling.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

