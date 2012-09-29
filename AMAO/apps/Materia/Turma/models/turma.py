# -*- coding: utf-8 -*-

from django.db import models

from django_extensions.db.fields import AutoSlugField

#from Aluno.models import Aluno
#from Professor.models import Professor
#from Materia.models import Materia


class Turma(models.Model):
    """
    Classe que representa uma turma de uma materia.
    Essa classe que possuim os professores e os alunos da materia em questao.
    """
    nome = models.CharField(u"Nome", max_length=250)
    sigla = models.CharField(u"Sigla",max_length=10)
    professor = models.ForeignKey('Professor.Professor',related_name="turmas")
    materia = models.ForeignKey('Materia.Materia',related_name="turmas")    
    
    alunos = models.ManyToManyField('Aluno.Aluno', related_name="turmas")
    
    slug = AutoSlugField(populate_from='sigla')

    class Meta:
        verbose_name = u'Turma'
        app_label = 'Turma'

    def __unicode__(self):
        return self.nome
        
