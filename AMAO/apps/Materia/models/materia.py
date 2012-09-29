# -*- coding: utf-8 -*-

from django.db import models

from django_extensions.db.fields import AutoSlugField


class Materia(models.Model):
    """
    Classe que representa uma materia 
    """
    nome = models.CharField(u"Nome", max_length=250)
    sigla = models.CharField(u"Sigla",max_length=10)

    slug = AutoSlugField(populate_from='sigla')
    

    class Meta:
        verbose_name = u'Materia'
        app_label = 'Materia'

    def __unicode__(self):
        return self.nome
        
