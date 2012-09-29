# -*- coding: utf-8 -*-

from django.contrib.auth import login
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from annoying.decorators import render_to

from django.contrib.auth.models import User
from Professor.models import Professor, Monitor
from Professor.views.utils import prof_monit_exist
from Avaliacao.models import TemplateAvaliacao, Avaliacao
from Avaliacao.Questao.models import QuestaoDeAvaliacao
from Avaliacao.Questao.forms import AlterarNotaQuestaoForm

@prof_monit_exist
@login_required     
@render_to('professor/consultar.html')
def consultar(request):
    prof=None
    monitor=None
    try:
        prof = request.user.professor_set.get()
    except Professor.DoesNotExist:
        try:
            monitor = request.user.monitor_set.get()
        except Monitor.DoesNotExist:
            return redirect('/')
        
    template_id = request.GET.get('template',None)
    avaliacao_id = request.GET.get('avaliacao',None)
    questao_id = request.GET.get('questao',None)
    
    template = None
    if template_id != None:
        template = get_object_or_404(TemplateAvaliacao,id=template_id)
    elif avaliacao_id != None:
        avaliacao = get_object_or_404(Avaliacao,id=avaliacao_id)
        template=avaliacao.templateAvaliacao
    elif questao_id != None:
        questao = get_object_or_404(QuestaoDeAvaliacao,id=questao_id)
        if request.POST:
            form_questao = AlterarNotaQuestaoForm(request.POST, instance=questao)
            form_questao.save()
        else:
            form_questao = AlterarNotaQuestaoForm(instance=questao)
        template=questao.avaliacao.templateAvaliacao
        
        
    if prof != None:
        if template == None:
                templates = TemplateAvaliacao.objects.filter(turma__in=prof.turmas.all(),ativa=False)
                return locals()                

        if not template.verifica_professor(prof):
            return redirect('/')
    else:
        if template == None:
                templates = TemplateAvaliacao.objects.filter(turma__in=monitor.materia.turmas.all(),ativa=False)
                return locals()                
            
        if not template.verifica_monitor(monitor):
            return redirect('/')
        
    template = None if template_id == None else template
    return locals()
    