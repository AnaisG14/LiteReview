import dj_database_url

from .settings import *

DEBUG = False
TEMPLATE_DEBUG = False

DATABASES['default'] = dj_database_url.config()

SECRET_KEY = '0gd*i6-jf^@fz7csa-$b)d3r64rurk5pti7%5&5wcj29)_7lds'

ALLOWED_HOSTS = ['litereview.herokuapp.com']
