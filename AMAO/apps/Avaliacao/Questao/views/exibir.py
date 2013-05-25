# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, redirect
from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required

from Aluno.views.utils import aluno_exist
from Professor.views.utils import prof_monit_exist
from Avaliacao.Questao.models import QuestaoDeAvaliacao, Fonte, FonteGabarito


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


@aluno_exist
@login_required
@render_to('avaliacao/questao/exibir_fonte.html')
def exibir_arquivo_fonte(request,fonte_id):
    aluno = request.user.aluno_set.get()
    fonte = get_object_or_404(Fonte,pk=fonte_id)

    #so pode ver os fontes das questoes que ele fez
    if not fonte.questao.avaliacao.aluno.pk == aluno.pk:
        return redirect('/')

    return locals()

@prof_monit_exist
@login_required
@render_to('avaliacao/questao/exibir_fonte.html')
def exibir_arquivo_fonte_gabarito(request,fonte_id):
    fonte = get_object_or_404(FonteGabarito,pk=fonte_id)


    return locals()
