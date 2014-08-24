# -*- coding: utf-8 -*-

from util_settings import *

DATABASE_NAME = JSON_CONFS.get('DATABASE_NAME')
DATABASE_USER = JSON_CONFS.get('DATABASE_USER')
DATABASE_PASSWORD = JSON_CONFS.get('DATABASE_PASSWORD')
DATABASE_HOST = JSON_CONFS.get('DATABASE_HOST')
DATABASE_PORT = JSON_CONFS.get('DATABASE_PORT')

DATABASES = {
    'default': {
        'ENGINE': 'postgresql_psycopg2',
        'NAME': DATABASE_NAME,
        'USER': DATABASE_USER,
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': DATABASE_HOST,
        'PORT': DATABASE_PORT,
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
