# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, redirect
from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory

from Professor.views.utils import prof_monit_exist
from Professor.models import Professor, Monitor
from Avaliacao.Questao.models import Questao ,EntradaGabarito, FonteGabarito ,OpcaoMultiplaEscolha
from Avaliacao.Questao.forms import criarQuestaoForm,criarTipoQuestaoForm
from Corretor.tasks import run_corretor_validar_gabarito
from Corretor.models.retorno import RetornoCorrecao

from forms_amao.widgets import change_widget_to_NoFullPathLinkFileInput

@prof_monit_exist
@login_required
@render_to('avaliacao/questao/criar.html')
def criar_questao(request):
    autor = request.user
    criado=False
    #QuestoesFormsSet = formset_factory(criarFiltroQuestaoForm)
    formsetEntradasInline=inlineformset_factory(Questao,EntradaGabarito,extra=1)
    formsetFontesInline=inlineformset_factory(Questao,FonteGabarito,extra=1)
    formsetOpcoesInline=inlineformset_factory(Questao,OpcaoMultiplaEscolha,extra=4)
    if request.method == "POST":
        form = criarQuestaoForm(request.POST)
        if form.is_valid():
            novaQuestao=form.save(commit=False)
            novaQuestao.autor = autor
            formEntradas = formsetEntradasInline(request.POST, request.FILES,instance=novaQuestao)
            formFontes = formsetFontesInline(request.POST, request.FILES,instance=novaQuestao)
            formOpcoes = formsetOpcoesInline(request.POST,instance=novaQuestao)

            if formEntradas.is_valid() and formFontes.is_valid() and formOpcoes.is_valid():
                novaQuestao.save()
                formEntradas.save()
                formFontes.save()
                formOpcoes.save()
                form.save_m2m()
                novaQuestao.save(verificar=True)
                criado=True
        else:
            #QuestoesForms=formsetInline()
            formEntradas = formsetEntradasInline()
            formFontes = formsetFontesInline()
            formOpcoes = formsetOpcoesInline()
    else:
        #QuestoesForms=formsetInline()
        form = criarQuestaoForm()
        formEntradas = formsetEntradasInline()
        formFontes = formsetFontesInline()
        formOpcoes = formsetOpcoesInline()

    return locals()

@prof_monit_exist
@login_required
@render_to('avaliacao/questao/editar.html')
def editar_questao(request,questao_id):

    questao = get_object_or_404(Questao,pk=questao_id)


    autor = request.user
    criado=False
    formsetEntradasInline=inlineformset_factory(Questao,EntradaGabarito,formfield_callback=change_widget_to_NoFullPathLinkFileInput,extra=1)
    formsetFontesInline=inlineformset_factory(Questao,FonteGabarito,formfield_callback=change_widget_to_NoFullPathLinkFileInput,extra=1)
    formsetOpcoesInline=inlineformset_factory(Questao,OpcaoMultiplaEscolha,extra=4)
    if request.method == "POST":
        #nao permite editar questoes que ja estao sendo usadas ou ja foram usadas antes
        if questao.avaliacoes.count() != 0:
            return redirect('/')

        form = criarQuestaoForm(request.POST,instance=questao)
        if form.is_valid():
            questao=form.save(commit=False)
            questao.autor = autor
            formOpcoes = formsetOpcoesInline(request.POST,instance=questao)
            formEntradas = formsetEntradasInline(request.POST, request.FILES,instance=questao)
            formFontes = formsetFontesInline(request.POST, request.FILES,instance=questao)

            if formEntradas.is_valid() and formOpcoes.is_valid() and formFontes.is_valid():
                questao.save(verificar=False)
                formEntradas.save()
                formFontes.save()
                formOpcoes.save()
                form.as_p()
                form.save_m2m()
                questao.save(verificar=True)
                form = criarQuestaoForm(instance=questao)
                formOpcoes = formsetOpcoesInline(instance=questao)
                formEntradas = formsetEntradasInline(instance=questao)
                formFontes = formsetFontesInline(instance=questao)
                criado=True
    else:
        form = criarQuestaoForm(instance=questao)
        formOpcoes = formsetOpcoesInline(instance=questao)
        formEntradas = formsetEntradasInline(instance=questao)
        formFontes = formsetFontesInline(instance=questao)

    return locals()

@prof_monit_exist
@login_required
@render_to('avaliacao/questao/retorno_correcao.html')
def ajax_retorno_correcao_gabarito(request,questao_id):
    "funcao para o ajax saber qual o status do retorno da correcao de validacao de uma questao gabarito(prof)"

    correcao_msg = "Validando..."
    questao = get_object_or_404(Questao,pk=questao_id)

    retorno_questao = questao.retorno_correcao
    task_id = "%s"%retorno_questao.task_id
    print ">>ajax_retorno_correcao_gabarito: task_id: %s" % task_id
    retorno = run_corretor_validar_gabarito.AsyncResult(task_id)
    if retorno.ready():
        retorno_questao = RetornoCorrecao.objects.get(pk=questao.retorno_correcao.pk)
        correcao_msg = retorno_questao.msg

    return locals()

@login_required
@render_to('avaliacao/questao/criar_tipo.html')
def criar_tipo(request):
    criado=False
    if request.method == "POST":
        form = criarTipoQuestaoForm(request.POST)
        if form.is_valid():
            form.save()
            criado=True
    else:
        form = criarTipoQuestaoForm()

    return locals()
