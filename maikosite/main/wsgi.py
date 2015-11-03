'''
WSGI config file.
This is the entry point for ALL project code, called directly from
Apache. Setting any and all customized path and environment variables
here will allow them to apply to ALL project code.
'''

import os
import sys

# Root directory of project. We can self-determine this now, it's just the
# parent directory to the one this file (wsgi.py) resides in.
this_dir = os.path.dirname(__file__)
PROJECT_ROOT_DIR = os.path.abspath(os.path.join(this_dir, '..'))
sys.path.insert(0, PROJECT_ROOT_DIR)

#os.environ['DJANGO_SETTINGS_MODULE'] = 'main.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")

# enable software collections
from sdg.scl import SDGCollections
SDGCollections.enable('python27', 'sdg_2015a_python27')

# path shenanigans -- put our local dir back to being first
del sys.path[1]
sys.path.insert(0, PROJECT_ROOT_DIR)

# Fire off the application.
# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
