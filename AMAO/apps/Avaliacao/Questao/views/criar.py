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
