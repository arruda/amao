# -*- coding: utf-8 -*-
"""
Inicia todas as avaliacoes que estão inativas e estao dentro da data.
"""

from django_extensions.management.jobs import HourlyJob
from Avaliacao.models import Avaliacao, TemplateAvaliacao
import datetime

class Job(HourlyJob):
    help = "Terminar avaliacoes expiradas"

    def execute(self):
        templates = TemplateAvaliacao.objects.filter(ativa=False,
                                                     data_inicio__lte=datetime.datetime.now(),
                                                     data_termino__gte=datetime.datetime.now())
                                                     
        for template in templates:
            template.ativa=True
            template.save()