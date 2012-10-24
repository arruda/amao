# -*- coding: utf-8 -*-

    
def aluno_monitor_professor(request):
    from Aluno.models import Aluno
    from Professor.models import Professor, Monitor
    user = request.user
    aluno = None
    professor = None
    monitor = None
    
    if user.is_authenticated():
        
        try:
            aluno = user.aluno_set.get()
        except Aluno.DoesNotExist:
            pass
        
        try:
            professor = user.professor_set.get()
        except Professor.DoesNotExist:
            pass
        
        try:
            monitor = user.monitor_set.get()
        except Monitor.DoesNotExist:
            pass
        
    return {'aluno':aluno, 'professor':professor, 'monitor': monitor}


