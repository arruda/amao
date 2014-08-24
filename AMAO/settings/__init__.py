# -*- coding: utf-8 -*-
import os



from conf import *
from installed_apps import *
from celery_settings import *
from util_settings import *


CURRENT_ENV = JSON_CONFS.get('CURRENT_ENV', 'DEV')

if CURRENT_ENV == 'PROD':
    from prod_settings import *
else:
    from dev_settings import *


SECRET_KEY = JSON_CONFS.get('SECRET_KEY')
