# -*- coding: utf-8 -*-

from django.db import models

from django_extensions.db.fields import AutoSlugField
from django.contrib.auth.models import User

class Monitor(models.Model):
    
    usuario = models.ForeignKey(User, unique=True)
#    matricula = models.CharField(max_length=250,unique=True)
    materia = models.ForeignKey('Materia.Materia')
    
    class Meta:
        verbose_name = u'Monitor'
        app_label = 'Professor'

    def __unicode__(self):
        return self.usuario.username

    def get_aluno(self):
        "retorna o aluno desse monitor"
        return self.usuario.aluno_set.get()


