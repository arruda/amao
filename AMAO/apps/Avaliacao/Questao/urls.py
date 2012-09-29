# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *


urlpatterns = patterns('Avaliacao.Questao.views',    
    url(r'^responderQuestao/(?P<questao_id>\S+)/$',   'responderQuestao', name='responderQuestao'),   
    url(r'^corrigirQuestao/(?P<questao_id>\S+)/$',   'corrigirQuestao', name='corrigirQuestao'),    
    url(r'^retorno_ajax/(?P<questao_id>\S+)/$',   'ajax_retorno_correcao', name='ajax_retorno_correcao'),    
    url(r'^gabarito/(?P<questao_id>\S+)/$',   'gabaritoQuestao', name='gabaritoQuestao'),     
    url(r'^criar/$',   'criar_questao', name='criar_questao'),    
    url(r'^criarTipo/$',   'criar_tipo', name='criar_tipo'), 
    url(r'^exibirQuestao/(?P<questao_id>\S+)/$',   'exibirQuestao', name='exibirQuestao'), 
)
