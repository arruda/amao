from django.conf.urls.defaults import patterns, include, url

password_change_args = {
    'template_name':        'usuarios/perfil/password-change.html', 
    'post_change_redirect': '/dashboard/perfil/senha-alterada', }


urlpatterns = patterns('Core.views',
    url(r'^$', 'index', name='index'),
    url(r'^dashboard/$', 'dashboard', name='dashboard'),
    url(r'^dashboard/perfil/$', 'perfil', name='perfil'),
)

urlpatterns += patterns('django.contrib.auth.views',               

    url(r'^login/$', 'login', {'template_name': 'usuarios/login.html',}, name='login'),  
    url(r'^logout/$', 'logout', {'template_name': 'usuarios/login.html'},name='logout'),
    
    
    url(r'^dashboard/perfil/mudar-senha/$', 'password_change', password_change_args, name='password_change'), 
    
    url(r'^dashboard/perfil/senha-alterada/$', 'password_change_done',  {'template_name':'usuarios/perfil/password-change-done.html'}, name='password_change_done'),
    

)


urlpatterns += patterns('Avaliacao.views',            
    url(r'^dashboard/avaliacoes/$', 'listar_avaliacoes', name='listar_avaliacoes'),
)

urlpatterns += patterns('Professor.views',            
    url(r'^dashboard/criar_conteudos/$', 'criar_conteudos', name='criar_conteudos'),
)
