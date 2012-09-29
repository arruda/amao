from django.conf.urls.defaults import patterns, include, url

password_change_args = {
    'template_name':        'usuarios/password-change.html', 
    'post_change_redirect': '/usuario/senha-alterada', }


urlpatterns = patterns('Core.views',
    url(r'^$', 'index', name='index'),
    url(r'^dashboard/', 'dashboard', name='dashboard'),
)

urlpatterns += patterns('django.contrib.auth.views',               

    url(r'^login/$', 'login', {'template_name': 'usuarios/login.html',}, name='login'),  
    url(r'^logout/$', 'logout', {'template_name': 'usuarios/login.html'},name='logout'),
    
    
    url(r'^usuario/mudar-senha/$', 'password_change', password_change_args, name='password_change'), 
    
    url(r'^usuario/senha-alterada/$', 'password_change_done',  {'template_name':'usuarios/password-change-done.html'}, name='password_change_done'),
    

)
