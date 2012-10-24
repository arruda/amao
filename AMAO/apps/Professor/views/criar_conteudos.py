# -*- coding: utf-8 -*-

from django.contrib.auth import login
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to

from django.contrib.auth.models import User
from Professor.models import Professor, Monitor
from Professor.views.utils import prof_monit_exist
from Materia.Turma.models import Turma
from Avaliacao.models import TemplateAvaliacao, Avaliacao
from Avaliacao.Questao.models import QuestaoDeAvaliacao, Questao ,FiltroQuestao

@prof_monit_exist
@login_required  
@render_to('professor/criar/criar_conteudos.html')
def criar_conteudos(request): 
    usu = None
    try:
        professor = request.user.professor_set.get()
        usu = professor
    except Professor.DoesNotExist:
        pass
    try:
        monitor = request.user.monitor_set.get()
        usu = monitor
    except Monitor.DoesNotExist:
        pass
    
    return locals()