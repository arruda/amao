# -*- coding: utf-8 -*-
"""
Termina todas as avaliacoes que estão em aberto e que a data final expirou.
"""

from django_extensions.management.jobs import HourlyJob
import datetime

class Job(HourlyJob):
    help = "Terminar avaliacoes expiradas"

    def execute(self):
        from Avaliacao.models import Avaliacao, TemplateAvaliacao
        templates = TemplateAvaliacao.objects.filter(ativa=True,
                                                     data_termino__lte=datetime.datetime.now())
        
        for template in templates:
            template.terminar()