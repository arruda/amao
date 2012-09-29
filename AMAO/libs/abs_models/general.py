# -*- coding: utf-8 -*-
"""
    abs_models
    ~~~~~~~~~~~~~~

    Here are located all the abstract models
    
    :copyright: (c) 2012 by Arruda.
"""
from django.db import models
from django_extensions.db.fields import AutoSlugField


class Abs_titulado(models.Model):
    "um modelo que possui campode titulo que nao pode ser deixado em branco"
    
    titulo = models.CharField(u"Titulo",blank=False, null=False, max_length=250)
    
    class Meta:
        abstract = True
        
    def __unicode__(self):
        return self.titulo

class Abs_titulado_slugfy(Abs_titulado):
    "um modelo que possui campo de titulo que deve ser preenchido, e um campo slug que é populado do titulo"
    
    slug = AutoSlugField(populate_from='titulo')
    
    class Meta:
        abstract = True
        
    def __unicode__(self):
        return self.titulo
