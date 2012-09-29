# -*- coding: utf-8 -*-

from django.db import models    
from model_utils import Choices


class RetornoCorrecao(models.Model):
    """Um modelo que possui informacoes sobre o retorno da correcao de uma questao(ou questao de avaliacao).
    """
    TIPOS = Choices(
                       (0,'loading',u'Loading'),
                       (1,'compilacao',u'Compilação'),
                       (2,'execucao',u'Execução'),
                       (3,'comparacao',u'Comparação'),
                       (4,'lock',u'Lock'),
                       (5,'correto',u'Correto'),
                   )
    tipo =  models.SmallIntegerField(u"Tipo",choices=TIPOS, default=TIPOS.loading)
    msg = models.CharField(u"Mensagem",max_length=128,blank=True,null=True)
    task_id = models.CharField(max_length=350,blank=True,null=True)
    class Meta:
        verbose_name = u'Retorno Correção'
        app_label = 'Corretor'
        
    
    def __unicode__(self):
        return "%s: %s" %(self.TIPOS[self.tipo][1],self.msg)