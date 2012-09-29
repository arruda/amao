from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('Professor.views',
    url(r'^consultar/$', 'consultar',name='professor_consultar'),
)
