# -*- coding: utf-8 -*-
import os
CURRENT_ENV = os.environ.get('AMAO_ENV', 'DEV')

SECRET_KEY = ')=k_lqfhkqpbqi6us3aqk^qwte45d4nw@zpo1qozx94&&pbu@#'

from conf import *
from installed_apps import *
from celery_settings import *

if CURRENT_ENV == 'PROD':
    from prod_settings import *
else:
    from dev_settings import *
