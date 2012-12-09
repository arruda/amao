#coding: utf-8

import os
from util_settings import *


ADMINS = (
     ('Arruda', 'felipe.pontes@uniriotec.br'),
)
MANAGERS = ADMINS

TIME_ZONE = 'America/Sao_Paulo'
LANGUAGE_CODE = 'pt-br'

SITE_ID = 1

USE_I18N = True
USE_L10N = True


# Login/Logout URL
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/dashboard/'

#AUTH_PROFILE_MODULE = 'usuarios.PerfilUsuario'

#Quando tiver o servidor SMTP trocar as infos daqui para utilizar o mesmo.
#EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_HOST_USER = 'email@email.br'
#EMAIL_HOST_PASSWORD = 'pass'
#EMAIL_USE_TLS = True

AUTHENTICATION_BACKENDS = ( 
        'user_backends.email_username.EmailOrUsernameModelBackend',
        'django.contrib.auth.backends.ModelBackend',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    # default template context processors
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',    
    'django.core.context_processors.request',
    #AMAO
    'context_processors.aluno_monitor_professor',
    
)
ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    LOCAL('templates'),
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
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

CORRETORES = (
#    ('nome','Descrição','app.corretor.classe'),
#    ('Base','Um corretor basico.','Corretor.base.Corretor'),
    (1,'CPP','Um corretor basico de c++.','Corretor.corretor.corretor_cpp.CorretorCPP'),
)

#safeexec

SAFEEXEC_PATH = LOCAL('safeexec/safeexec')

#CORRETORES= (
#        ( 0, 'aguardando',  u'Aguardando Pagamento'),
#        ( 1, 'aguardando',  u'Aguardando Pagamento'),
#        )


TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = ['--rednose','--testmatch=^test','--stop','--exclude-dir-file=nose_exclude.txt']#(,'--with-notify')

DEBUG_TOOLBAR_CONFIG = {
'INTERCEPT_REDIRECTS':False,
}