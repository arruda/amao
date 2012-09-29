# -*- coding: utf-8 -*-

from django.contrib.auth import login
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from annoying.decorators import render_to


from django.contrib.auth.models import User
from Aluno.models import Aluno

@render_to('aluno/perfil.html')
@login_required     
def perfil(request):
    try:
        aluno = request.user.aluno_set.get()
    except Aluno.DoesNotExist:
        return redirect('/')
    avaliacoes_comecar = aluno.avaliacoes_iniciar()
    avaliacoes_andamento = aluno.avaliacoes_andamento()
    avaliacoes_passadas =  aluno.avaliacoes_passadas()
    avaliacoes_futuras = aluno.avaliacoes_futuras()
    
    
    return locals()
    
#@login_required     
#def minhasAvaliacoesPendentes(request):
#    aluno = request.user.aluno_set.get()
#    from Avaliacoes.models import TemplateAvaliacao
#    
#    avaliacoesPendentes = TemplateAvaliacao.filter(materia__in = aluno.materias.all())
#    
#    return direct_to_template(request, "Aluno/perfil/avaliacoes.html", extra_context={'avaliacoesPendentes':avaliacoesPendentes})
