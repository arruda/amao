# -*- coding: utf-8 -*-

from django.db import models

from django.contrib.auth.models import User

from django_extensions.db.fields import AutoSlugField


class Aluno(models.Model):
   
    usuario = models.ForeignKey(User, unique=True)
    
    matricula = models.CharField(max_length=250,unique=True)
    
    slug = AutoSlugField(populate_from='matricula')   

    class Meta:
        verbose_name = u'Aluno'
        app_label = 'Aluno'

    def __unicode__(self):
        return self.matricula
    
    def avaliacoes_futuras(self):
        "lista todas os templateAvaliacao que ainda irao acontecer para esse aluno"
        #avaliacoes ja criadas 
        from Avaliacao.models import TemplateAvaliacao
        
        return TemplateAvaliacao.objects.list_templatesAvaliacaoFuturas_aluno(self)
    
    def avaliacoes_iniciar(self):
        "lista todas os templateAvaliacao disponiveis para esse aluno"
        #avaliacoes ja criadas 
        from Avaliacao.models import TemplateAvaliacao
        
        return TemplateAvaliacao.objects.list_templatesAvaliacao_aluno(self)
    
    def avaliacoes_andamento(self):
        "lista as avaliacoes que o aluno tem ativas"
#        return self.avaliacoes.filter()
        return self.avaliacoes.filter(ativa=True,simulado=False)
    
    def avaliacoes_passadas(self):
        "lista todas as avaliacoes que ja terminaram"
        return self.avaliacoes.filter(ativa=False,simulado=True)
    
    def simulados_andamento(self):
        "lista os simulados que o aluno tem ativo"
#        return self.avaliacoes.filter()
        from Avaliacao.models import Simulado        
        return Simulado.objects.filter(aluno=self,ativa=True)
    
    def simulados_passados(self):
        "lista todas os simulados que ja terminaram"
        from Avaliacao.models import Simulado 
        return Simulado.objects.filter(aluno=self,ativa=False)