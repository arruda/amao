# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from django.forms.models import inlineformset_factory

from Avaliacao.Questao.models import QuestaoDeAvaliacao, Fonte


from Corretor.corretor.corretor_cpp import CorretorException,ComparadorException,CompiladorException, ExecutorException
#from Avaliacao.Questao.forms import ResponderQuestaoForm


#@render_to('temporario/corrigir.html')
#def corrigirQuestao(request,questao_id):
#    questaoAvaliacao = get_object_or_404(QuestaoDeAvaliacao,pk=questao_id)
#    corretor = CorretorCPP()
#
#    correcao_msg = "Correto" 
#    try:
#        corretor.corrigir(questao=questaoAvaliacao)
#    except CorretorException as erro:
#        
#        if isinstance()
#        correcao_msg=
#        pass
#        
#    return locals()

@render_to('temporario/responder.html')
def responderQuestao(request,questao_id):
    "faz o upload de uma questao"
    questaoAvaliacao = get_object_or_404(QuestaoDeAvaliacao,pk=questao_id)

    FontesInlineFormSet = inlineformset_factory(QuestaoDeAvaliacao, Fonte)
    if request.method == "POST":
        formset = FontesInlineFormSet(request.POST, request.FILES, instance=questaoAvaliacao)
        if formset.is_valid():
            formset.save()
            formset = FontesInlineFormSet(instance=questaoAvaliacao)
#            return redirect('corrigirQuestao',questao_id=questaoAvaliacao.id)
    else:
        formset = FontesInlineFormSet(instance=questaoAvaliacao)

    return locals()

@render_to('temporario/exibir.html')
def exibirQuestao(request,questao_id):
    "monstrar questao de avaliaca"
    questaoAvaliacao = get_object_or_404(QuestaoDeAvaliacao,pk=questao_id)

    return locals()
