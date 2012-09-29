# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import user_passes_test
from Professor.models import Professor, Monitor

def check_professor_or_monitor_exist(user):
    try:
        prof = user.professor_set.get()
        return True
    except Professor.DoesNotExist:
        try:
            mon = user.monitor_set.get()
            return True
        except Monitor.DoesNotExist:
            return False
        
    return False
    
prof_monit_exist = user_passes_test(lambda u: check_professor_or_monitor_exist(u))
