# -*- coding: utf-8 -*-

from django.db import models    
        
from django_extensions.db.fields import AutoSlugField 
import mptt

class TipoQuestao(models.Model):
    """
    Classe que representa o tipo de uma questao.
    """
    #fazer ligacao recursiva para a propria classe
    #para representar grupos e subgrupos.
    
    tipo = models.CharField(u"Tipo", max_length=250)
    tipoPai = models.ForeignKey('self',related_name="tipoFilhos",null=True,blank=True)
    
    class Meta:
        verbose_name = u'Tipo de Questão'
        app_label = 'Questao'

    def verificarGrupo(self,tipoVerificador):
        """
        Metodo responsavel por dizer se esse tipoQuestao tem como algum pai/avo/similar o tipoVerificador
        subindo a hierarquia de tipoPai.
        """
        tp = self.tipoPai
        while(tp != None):
            #se o tipo sendo verificado atualmente for igual ao tipoVerificador
            #entao retorna verdadeiro
            if(tp == tipoVerificador):
                return True
            
            #caso nao seja igual, entao tenta pegar o pai do atual
            tp = tp.tipoPai
            #caso o tipo atual nao tenha pai(seja um agrupador geral)
            #quer dizer que tp vai ser None nesse ponto, logo sai do while

        #saindo do while significa que nao existe um tipoVerificador parente(subindo a arvore) do tipo(self)
        return False
    
    def __unicode__(self):
        return self.tipo

mptt.register(TipoQuestao, parent_attr='tipoPai', order_insertion_by=['tipo'])
