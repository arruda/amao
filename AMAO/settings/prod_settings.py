# -*- coding: utf-8 -*-

from util_settings import *

DATABASES = {
    'default': {
        'ENGINE': 'postgresql_psycopg2',
        'NAME': 'django_db',
        'USER': 'django_login',
        'PASSWORD': 'Amao.2@12',
        'HOST': '',
        'PORT': '',
    }
}

DEBUG = False
TEMPLATE_DEBUG = DEBUG

SERVE_MEDIA = False

MEDIA_ROOT = '/var/www/medias/AMAO/media/'
MEDIA_URL = '/media/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

STATIC_URL = '/static/'
STATICFILES_DIRS = (LOCAL('static'), )
STATIC_ROOT = '/var/www/medias/AMAO/static/' 
