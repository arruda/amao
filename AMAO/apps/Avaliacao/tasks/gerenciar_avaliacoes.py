# -*- coding: utf-8 -*-
"""
Gerencia as avaliacoes, isso é 
Inicia todas as avaliacoes que estão inativas e estao dentro da data.
ou
Termina todas as avaliacoes que estão em aberto e que a data final expirou.
"""

from celery.task import periodic_task
from Avaliacao.models import Avaliacao, TemplateAvaliacao, Simulado
import datetime

INTERVALO_EXEC=8

@periodic_task(run_every=datetime.timedelta(seconds=INTERVALO_EXEC))
def iniciar_avaliacoes():
    "Inicia todas as avaliacoes que estão inativas e estao dentro da data."
    templates = TemplateAvaliacao.objects.filter(ativa=False,
                                                 data_inicio__lte=datetime.datetime.now(),
                                                 data_termino__gte=datetime.datetime.now())
                                                 
    for template in templates:
        template.ativa=True
        template.save()

@periodic_task(run_every=datetime.timedelta(seconds=INTERVALO_EXEC))
def finalizar_avaliacoes():
    "Termina todas as avaliacoes que estão em aberto e que a data final expirou."
    templates = TemplateAvaliacao.objects.filter(ativa=True,
                                                 data_termino__lte=datetime.datetime.now())
    
    for template in templates:
        template.terminar()
        
@periodic_task(run_every=datetime.timedelta(seconds=INTERVALO_EXEC))
def finalizar_simulados():
    "Termina todas as avaliacoes que estão em aberto e que a data final expirou."
    simulados = Simulado.objects.filter(ativa=True,
                                                 data_termino__lte=datetime.datetime.now())
    
    for simulado in simulados:
        simulado.terminar()