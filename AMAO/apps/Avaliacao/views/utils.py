# -*- coding: utf-8 -*-

from functools import wraps
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404
from Avaliacao.models import Avaliacao, TemplateAvaliacao

def avaliacao_ativa_or_404(avaliacao):
    "verifica se a avaliacao ta ativa se nao estiver levanto 404"
    if not avaliacao.ativa:
        raise Http404('Avaliação %s não está ativa.' % avaliacao.pk)
    return True

#def verifica_avaliacao_ativa(view_func):
#    def _decorator(request, *args, **kwargs):
#        avaliacao = get_object_or_404(Avaliacao,pk=request.avaliacao_id)
#        if not avaliacao.ativa:
#            raise Http404('Avaliação %s não está ativa.' % avaliacao.pk)
#        
#        response = view_func(request, *args, **kwargs)
#        return response
#    return wraps(view_func)(_decorator)
#
#def verifica_templateAvaliacao_ativa(view_func):
#    def _decorator(request, *args, **kwargs):
#        avaliacao = get_object_or_404(TemplateAvaliacao,pk=request.template_id)
#        if not avaliacao.ativa:
#            return redirect('')
#        
#        response = view_func(request, *args, **kwargs)
#        return response
#    return wraps(view_func)(_decorator)
