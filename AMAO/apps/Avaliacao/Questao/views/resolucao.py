# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from django.forms.models import inlineformset_factory
#from multithread.postpone import postpone
#import threading


from Aluno.views.utils import aluno_exist
from Avaliacao.Questao.models import QuestaoDeAvaliacao, Fonte, OpcaoMultiplaEscolha
from Avaliacao.Questao.forms import ResolucaoQuestaoAvaliacaoForm
from Corretor.models import RetornoCorrecao
from Corretor.base import CorretorException,ComparadorException,CompiladorException, ExecutorException, LockException
from Corretor.tasks import run_corretor
from forms_amao.widgets import NoFullPathLinkFileInput,change_widget_to_NoFullPathLinkFileInput
#from Avaliacao.Questao.forms import ResponderQuestaoForm

@aluno_exist
@login_required
@render_to('avaliacao/questao/responder.html')
def responderQuestao(request,questao_id):
    "faz o upload de uma questao"
    aluno = request.user.aluno_set.get()
    questaoAvaliacao = get_object_or_404(QuestaoDeAvaliacao,pk=questao_id)
    if not questaoAvaliacao.verifica_aluno(aluno):
        return redirect('/')
    fontes_extra_gabarito = [fonte for fonte in questaoAvaliacao.questao.fontesGabarito.filter(usarNaResolucao=True)]
    FontesInlineFormSet = inlineformset_factory(QuestaoDeAvaliacao, Fonte,formfield_callback=change_widget_to_NoFullPathLinkFileInput,extra=1)
#    RespostasMultiplaInlineFormSet = inlineformset_factory(QuestaoDeAvaliacao, OpcaoMultiplaEscolha)#,formfield_callback=change_widget_to_NoFullPathLinkFileInput)
    if request.method == "POST":
        questao_form = ResolucaoQuestaoAvaliacaoForm(request.POST, instance=questaoAvaliacao)
        fontes_formset = FontesInlineFormSet(request.POST, request.FILES, instance=questaoAvaliacao)
#        respostas_formset = RespostasMultiplaInlineFormSet(request.POST, request.FILES, instance=questaoAvaliacao)
        if fontes_formset.is_valid() and questao_form.is_valid():# and respostas_formset.is_valid():
            questao_form.save()
            questao_form = ResolucaoQuestaoAvaliacaoForm(instance=questaoAvaliacao)
            fontes_formset.save()
            fontes_formset = FontesInlineFormSet(instance=questaoAvaliacao)
#            respostas_formset.save()
#            respostas_formset = RespostasMultiplaInlineFormSet(instance=questaoAvaliacao)

    else:
        questao_form = ResolucaoQuestaoAvaliacaoForm(instance=questaoAvaliacao)
        fontes_formset = FontesInlineFormSet(instance=questaoAvaliacao)
#        respostas_formset = RespostasMultiplaInlineFormSet(instance=questaoAvaliacao)

    return locals()

#def chamar_corrigir_threaded(**kwargs):
#    "chama o processo que é rodado em paralelo"
#    questaoAvaliacao = kwargs.get('questaoAvaliacao',None)
#    correcao_msg = kwargs.get('correcao_msg',"")
#    corretor = questaoAvaliacao.questao.corretor()
#    tipo = "Carregando..."
#    try:
#        corretor.corrigir.delay(questao=questaoAvaliacao,limitar=["prog"])
#        tipo = "Correto..."
#        correcao_msg="Parabéns"
#    except CorretorException as erro:
#        if isinstance(erro,ExecutorException):
#            tipo = RetornoCorrecao.TIPOS.execucao
#            correcao_msg = erro.message
#        if isinstance(erro,CompiladorException):
#            tipo = RetornoCorrecao.TIPOS.compilacao
#            correcao_msg = erro.message
#        if isinstance(erro,ComparadorException):
#            tipo = RetornoCorrecao.TIPOS.comparacao
#            correcao_msg = erro.message
#        if isinstance(erro,LockException):
#            tipo = RetornoCorrecao.TIPOS.lock
#            correcao_msg = erro.message
##
#    if questaoAvaliacao.retorno_correcao:
#        ret = questaoAvaliacao.retorno_correcao
#    else:
#        ret = RetornoCorrecao()
#    ret.tipo = tipo
#    ret.msg = correcao_msg
#    ret.save()
#    questaoAvaliacao.retorno_correcao = ret
#    questaoAvaliacao.save()


@aluno_exist
@login_required
@render_to('avaliacao/questao/corrigir.html')
def corrigirQuestao(request,questao_id):
    aluno = request.user.aluno_set.get()
    questaoAvaliacao = get_object_or_404(QuestaoDeAvaliacao,pk=questao_id)
    if not questaoAvaliacao.verifica_aluno(aluno):
        return redirect('/')

    correcao_msg = "Corrigindo..."
    if questaoAvaliacao.retorno_correcao != None and questaoAvaliacao.retorno_correcao:
#        questaoAvaliacao.retorno_correcao.delete()
        pass

    corretor = questaoAvaliacao.questao.corretor()
#    dados_corretor = {
#                      'corretor':corretor,
#                      'questao':questaoAvaliacao,
#                      'limitar':["prog"],
#                      }
    retorno = questaoAvaliacao.get_retorno_or_create
    questaoAvaliacao.save()

    corretor_task = run_corretor.delay(corretor=corretor,questao=questaoAvaliacao,limitar=["prog"])
    retorno.task_id = corretor_task.task_id
    retorno.save()
    print ">>>corrigirQuestao: retorno.task_id: %s" % retorno.task_id
#    chamar_corrigir_threaded(correcao_msg=correcao_msg,questaoAvaliacao=questaoAvaliacao)
#    t = threading.Thread(target=_corrigir_thread,
#                         args=[],
#                         kwargs={'correcao_msg':correcao_msg,'questaoAvaliacao':questaoAvaliacao})
#    t.setDaemon(True)
#    t.start()

    return locals()

@aluno_exist
@login_required
@render_to('avaliacao/questao/retorno_correcao.html')
def ajax_retorno_correcao(request,questao_id):
    "funcao para o ajax saber qual o status do retorno da correcao"
    aluno = request.user.aluno_set.get()
    questaoAvaliacao = get_object_or_404(QuestaoDeAvaliacao,pk=questao_id)
    correcao_msg = "Carregando..."

    if questaoAvaliacao.verifica_aluno(aluno):
        retorno_questao = questaoAvaliacao.retorno_correcao
        task_id = "%s"%retorno_questao.task_id
        print ">>ajax_retorno_Correcao: task_id: %s" % task_id
        retorno = run_corretor.AsyncResult(task_id)
        if retorno.ready():
            print ">>retorno.ready()"
            if retorno.successful() == True:
                print ">>retorno.successful()"
                tipo = RetornoCorrecao.TIPOS.correto
                correcao_msg = "Correto!"
            elif isinstance(retorno.result,CorretorException):
                erro = retorno.result
                print "erro: %s" % erro.message
                if isinstance(erro,ExecutorException):
                    correcao_msg = erro.message
                    tipo = RetornoCorrecao.TIPOS.execucao
                if isinstance(erro,CompiladorException):
                    correcao_msg = erro.message
                    tipo = RetornoCorrecao.TIPOS.compilacao
                if isinstance(erro,ComparadorException):
                    correcao_msg = erro.message
                    tipo = RetornoCorrecao.TIPOS.comparacao
                if isinstance(erro,LockException):
                    correcao_msg = erro.message
                    tipo = RetornoCorrecao.TIPOS.lock

            retorno_questao.msg=correcao_msg
            retorno_questao.tipo = tipo
            retorno_questao.save()


#            questaoAvaliacao.retorno_correcao=None
#
#            questaoAvaliacao.save()

    return locals()

