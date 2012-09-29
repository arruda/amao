# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, redirect
from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required

from Aluno.views.utils import aluno_exist
from Avaliacao.Questao.models import QuestaoDeAvaliacao


@aluno_exist
@login_required
@render_to('avaliacao/questao/exibir.html')
def exibirQuestao(request,questao_id):
    aluno = request.user.aluno_set.get()
    questaoAvaliacao = get_object_or_404(QuestaoDeAvaliacao,pk=questao_id)    
    
    #so pode ver o gabarito das questoes que ele fez
    if not questaoAvaliacao.avaliacao.aluno.pk == aluno.pk:
        return redirect('/')
    
    
        
    return locals()