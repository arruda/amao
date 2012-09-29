# -*- coding: utf-8 -*-

from django.db import models

from django_extensions.db.fields import AutoSlugField
from django.contrib.auth.models import User

class Professor(models.Model):
    
    usuario = models.ForeignKey(User, unique=True)
    
    #por algum campo de identificacao para professor sem ser usuario?
    #colocar esse campo para popular o slug
    #slug = AutoSlugField(populate_from='matricula')    
    
    class Meta:
        verbose_name = u'Professor'
        app_label = 'Professor'

    def __unicode__(self):
        return self.usuario.username

