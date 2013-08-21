# -*- coding: utf-8 -*-

from util_settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': LOCAL('db.sqlite'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

DEBUG = True
TEMPLATE_DEBUG = DEBUG
SERVE_MEDIA = True

MEDIA_ROOT = LOCAL('media')
MEDIA_URL = '/media/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

STATIC_URL = '/static/'
STATICFILES_DIRS = ( LOCAL('static'), )
STATIC_ROOT = LOCAL('static_root')


#settings this for debug tools
INTERNAL_IPS = ('127.0.0.1',)
