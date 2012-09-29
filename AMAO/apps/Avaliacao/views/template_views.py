# -*- coding: utf-8 -*-

from django.contrib.auth import login
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from annoying.decorators import render_to


from django.contrib.auth.models import User
from Aluno.models import Aluno
from Avaliacao.models import TemplateAvaliacao, Avaliacao, Simulado

@render_to('avaliacao/comecar_avaliacao.html')
@login_required     
def comecar_avaliacao(request,template_id):
    try:
        aluno = request.user.aluno_set.get()
    except Aluno.DoesNotExist:
        return redirect('/')
    
    template = get_object_or_404(TemplateAvaliacao,id=template_id)
    #fazer verificacao se o aluno pode mesmo fazer essa avaliacao
    if not template.verifica_aluno(aluno):
        return redirect('/')
        
    avaliacao = Avaliacao.get_or_create(templateAvaliacao=template, aluno=aluno)
            
    #redireciona para a exibicao da avaliacao;
    return redirect('exibir_avaliacao',avaliacao.id)
    
@render_to('avaliacao/comecar_avaliacao.html')
@login_required     
def comecar_simulado(request,template_id):
    try:
        aluno = request.user.aluno_set.get()
    except Aluno.DoesNotExist:
        return redirect('/')
    
    template = get_object_or_404(TemplateAvaliacao,id=template_id)
    #fazer verificacao se o aluno pode mesmo fazer esse simulado
    if not template.verifica_simulado_aluno(aluno):
        return redirect('/')
        
    avaliacao = Simulado.get_or_create(templateAvaliacao=template, aluno=aluno)
            
    #redireciona para a exibicao da avaliacao;
    return redirect('exibir_avaliacao',avaliacao.id)
    