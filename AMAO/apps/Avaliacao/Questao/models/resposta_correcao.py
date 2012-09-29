# -*- coding: utf-8 -*-

from django.db import models    
from django.conf import settings

class Retorno_Correcao(models.Model):
    """Um modelo abstrato que possui informações sobre a resposta da correcao
    para uma questao(ou questao de avaliacao).
    """
    
    
    class Meta:
        abstract = True
        
    