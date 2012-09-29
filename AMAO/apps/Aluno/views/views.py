# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, render_to_response
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from Aluno.models import Aluno

@login_required     
def minhasAvaliacoes(request):
    aluno = request.user.aluno_set.get()
    avaliacoes = aluno.avaliacoes.all()
    
    return direct_to_template(request, "Aluno/perfil/avaliacoes.html", extra_context={'avaliacoes':avaliacoes})
    
@login_required     
def minhasAvaliacoesPendentes(request):
    aluno = request.user.aluno_set.get()
    from Avaliacoes.models import TemplateAvaliacao
    
    avaliacoesPendentes = TemplateAvaliacao.filter(materia__in = aluno.materias.all())
    
    return direct_to_template(request, "Aluno/perfil/avaliacoes.html", extra_context={'avaliacoesPendentes':avaliacoesPendentes})
