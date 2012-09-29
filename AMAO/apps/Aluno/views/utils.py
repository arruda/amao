# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import user_passes_test
from Aluno.models import Aluno

def check_aluno_exist(user):
    try:
        aluno = user.aluno_set.get()
        return True
    except Aluno.DoesNotExist:
        return False
    
    
aluno_exist = user_passes_test(lambda u: check_aluno_exist(u))

