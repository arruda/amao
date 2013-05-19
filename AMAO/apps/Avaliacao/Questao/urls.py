# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *


urlpatterns = patterns('Avaliacao.Questao.views',
    url(r'^responderQuestao/(?P<questao_id>\S+)/$',   'responderQuestao', name='responderQuestao'),
    url(r'^corrigirQuestao/(?P<questao_id>\S+)/$',   'corrigirQuestao', name='corrigirQuestao'),
    url(r'^retorno_ajax/(?P<questao_id>\S+)/$',   'ajax_retorno_correcao', name='ajax_retorno_correcao'),
    url(r'^retorno_gabarito_ajax/(?P<questao_id>\S+)/$',   'ajax_retorno_correcao_gabarito', name='ajax_retorno_correcao_gabarito'),
    url(r'^gabarito/(?P<questao_id>\S+)/$',   'gabaritoQuestao', name='gabaritoQuestao'),
    url(r'^criar/$',   'criar_questao', name='criar_questao'),
    url(r'^editar/(?P<questao_id>\S+)/$',   'editar_questao', name='editar_questao'),
    url(r'^criarTipo/$',   'criar_tipo', name='criar_tipo'),
    url(r'^exibirQuestao/(?P<questao_id>\S+)/$',   'exibirQuestao', name='exibirQuestao'),
    url(r'^exibirFonte/(?P<fonte_id>\S+)/$',   'exibir_arquivo_fonte', name='exibir_arquivo_fonte'),
    url(r'^exibirFonteGabarito/(?P<fonte_id>\S+)/$',   'exibir_arquivo_fonte_gabarito', name='exibir_arquivo_fonte_gabarito'),


    url(r'^listar/$',   'listar_questoes', name='listar_questoes'),
)
