# -*- coding: utf-8 -*-

from django.contrib.auth import login
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory
from annoying.decorators import render_to

from django.contrib.auth.models import User
from Professor.models import Professor, Monitor
from Professor.views.utils import prof_monit_exist
from Materia.Turma.models import Turma
from Avaliacao.models import TemplateAvaliacao, Avaliacao
from Avaliacao.Questao.models import QuestaoDeAvaliacao, Questao ,FiltroQuestao
from Avaliacao.forms import criarTemplateAvaliacaoForm,criarFiltroQuestaoForm

@prof_monit_exist
@login_required  
@render_to('avaliacao/criar.html')
def criar_avaliacao(request): 
    
    autor = request.user
    criado=False
    QuestoesFormsSet = formset_factory(criarFiltroQuestaoForm)
    formsetInline=inlineformset_factory(TemplateAvaliacao, FiltroQuestao,extra=1)
    if request.method == "POST":        
        form = criarTemplateAvaliacaoForm(request.POST)
        if form.is_valid():           
            novaAvalicao=form.save(commit=False)
            novaAvalicao.autor = autor
            QuestoesForms=formsetInline(request.POST,instance=novaAvalicao)
                
            if QuestoesForms.is_valid():
                criado=True
                novaAvalicao.save()
                QuestoesForms.save()       
    else:
        QuestoesForms=formsetInline()
        form = criarTemplateAvaliacaoForm()
    return locals()

