# -*- coding: utf-8 -*-
from django.contrib.auth import login
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from annoying.decorators import render_to


from django.contrib.auth.models import User
from Aluno.models import Aluno
from Professor.models import Professor, Monitor

@render_to('index.html')
def index(request):
    if request.user!= None:
        if request.user.is_authenticated():
            return redirect('dashboard')
    return locals()

def aluno_dashboad(request,dic):
    "prepara as variaveis do dashboard do aluno"
    try:
        aluno = request.user.aluno_set.get()
    except Aluno.DoesNotExist:
        return
    
    avaliacoes_comecar = aluno.avaliacoes_iniciar()
    avaliacoes_andamento = aluno.avaliacoes_andamento()
    avaliacoes_passadas =  aluno.avaliacoes_passadas()
    avaliacoes_futuras = aluno.avaliacoes_futuras()
    
    dic.update(locals())
    dic.pop('dic')
    
def monitor_dashboad(request,dic):
    "prepara as variaveis do dashboard do monitor"
    try:
        monitor = request.user.monitor_set.get()
    except Monitor.DoesNotExist:
        return
    
    
    dic.update(locals())
    dic.pop('dic')

def professor_dashboad(request,dic):
    "prepara as variaveis do dashboard do monitor"
    try:
        professor = request.user.professor_set.get()
    except Professor.DoesNotExist:
        return
    
    
    dic.update(locals())
    dic.pop('dic')

    

@login_required     
@render_to('usuarios/dashboard.html')
def dashboard(request):
    #prepara um dicionario que vai ser populado com variaveis
    #de cada tipo de dashboard
    dic = {}
    aluno_dashboad(request,dic)
    monitor_dashboad(request,dic)
    professor_dashboad(request,dic)
    
    
    retorno = locals()
    retorno.update(dic)
    return retorno