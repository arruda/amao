from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('Avaliacao.views',
    url(r'^$', 'index'),
    url(r'^exibir/(?P<template_id>\d+)/$', 'exibir',name='exibir_avaliacao'),
    url(r'^iniciar/(?P<template_id>\d+)/$', 'comecar_avaliacao',name='comecar_avaliacao'), 
    url(r'^iniciar_simulado/(?P<template_id>\d+)/$', 'comecar_simulado',name='comecar_simulado'),    
    url(r'^criar/$', 'criar_avaliacao',name='criar_avaliacao'),  
)
