from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

from django.contrib import admin
from django.conf import settings



admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('Core.urls')),
    url(r'^admin/',     include(admin.site.urls)),
    url(r'^aluno/',  include('Aluno.urls')),
    url(r'^avaliacao/',  include('Avaliacao.urls')),
    url(r'^questao/',  include('Avaliacao.Questao.urls')),
    url(r'^professor/',  include('Professor.urls')),
#    (r'^aluno/', include('AMAO.Aluno.urls')),
    
#    (r'^testeCompilacao/(?P<questao_id>.+)/$', 'AMAO.Teste.views.testeCompilacao'),
#    (r'^testeRodar/(?P<questao_id>.+)/$', 'AMAO.Teste.views.testeRodar'),
#    (r'^testeComparacao/(?P<questao_id>.+)/$', 'AMAO.Teste.views.testeComparacao'),
#    (r'^testeTudo/(?P<questao_id>.+)/$', 'AMAO.Teste.views.testeTudo'),
    
    
   

   
)

if settings.SERVE_MEDIA:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 
            'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, }),
    )