# -*- coding: utf-8 -*-

from decimal import Decimal
from django.db import models 
from django.conf import settings   

from django_extensions.db.fields import AutoSlugField
from model_utils import Choices
from abs_models import Abs_titulado_slugfy
from Corretor.utils import get_corretor_choices, get_corretor_por_id
from Corretor.base import CorretorException
from tipo_questao import TipoQuestao
from lockable import Lockable



class Questao(Abs_titulado_slugfy,Lockable):
    """
    Representa uma Questao, isso é um problema que esta ligado a uma avaliacao que esta por sua vez ligada
    a um aluno.
    """

    CORRETORES = Choices(*get_corretor_choices())
#    CORRETORES = Choices((0,'base','Base'))

    enunciado = models.TextField(u"Enunciado")
    respostaDiscursiva = models.TextField(u"Resposta Discursiva",blank=True, null=True)
    #:Representa o percentual que a programacao tem nessa questao.
    percentNotaProgramacao = models.DecimalField(u"Percentual da Nota de Programação",max_digits=10, decimal_places=2,default=Decimal("100"))
    #:Representa o percentual que a multipla escolha tem nessa questao.
    percentNotaMultipla = models.DecimalField(u"Percentual da Nota das Multiplas Escolhas",max_digits=10, decimal_places=2,default=Decimal("0"))
    #:Representa o percentual que a discursiva tem nessa questao.
    percentNotaDiscursiva = models.DecimalField(u"Percentual da Nota da Discursiva",max_digits=10, decimal_places=2,default=Decimal("0"))
    
    #:indica se uma questão está pronta ou não para ser usada num template avaliacao.
    verificada = models.BooleanField(u"Verificada",default=False)
    
    #:o autor(usuario) dessa questao
    autor = models.ForeignKey('auth.User',blank=True,null=True, related_name='questoes_autor')
    
    
    id_corretor = models.SmallIntegerField(u"Corretor",choices=CORRETORES)#, default=CORRETORES.c)
    
    
    #tipo que da questao, usado para filtragem
    tipo = models.ManyToManyField(TipoQuestao, related_name="questoes")    
    
    retorno_correcao = models.ForeignKey('Corretor.RetornoCorrecao',blank=True,null=True, on_delete=models.SET_NULL)
    @property
    def corretor(self):
        "recupera um corretor dado o id_corretor"
        return get_corretor_por_id(self.id_corretor)

    
    class Meta:
        verbose_name = u'Questão'
        app_label = 'Questao'

    def __unicode__(self):
        return self.slug    
    
    def get_rand_entrada(self):
        "retorna uma entrada randomica"        
        import random
        count = self.entradasGabarito.all().count()
        rand_entrada_num = 0
        if count >= 1:
            rand_entrada_num = random.randint(0,count -1)
            return self.entradasGabarito.all()[rand_entrada_num]
        else:
            return None
#        print rand_entrada_num
    
    def verificar_questao(self):
        """verifica se uma questão esta pronta para ser usada em uma avaliacao
            Ou seja, pode ser compilada e executada.
        """
        import os
        self.verificada = False
        
        def res_incorreta(ret):
            for res in ret:
                if res != 0 and res != None:
                    return True
            return False
        #se nao for uma questao com programacao nao faz essa verificacao
        if not self.percentNotaProgramacao > 0:
             self.verificada=True
             return
        try:
            corretor = self.corretor()
            ret_compilar_gabarito = corretor.compilar_completo(questao=self)
            entrada_gabarito=os.path.join(settings.MEDIA_ROOT,str(self.get_rand_entrada()))
            ret_executar_gabarito = corretor.executar_completo(questao=self,entrada_gabarito=entrada_gabarito)
            if not res_incorreta(ret_compilar_gabarito) and not res_incorreta(ret_executar_gabarito): 
                self.verificada = True
                
        except CorretorException:
            self.verificada = False
            
    @property
    def is_programacao(self):
        "retorna true se essa for uma questao de programação"
        return self.percentNotaProgramacao > Decimal("0")
        
    
    def save(self, *args, **kwargs):
        #Antes de salvar deve verificar se a questão é propria para ser usada em uma avaliacao
        #ou seja, da para compilar e executar sem erro.
        verificar = kwargs.get('verificar',True)
        if self.slug != "" and self.slug != None and verificar == True:
            self.verificar_questao()
        
        if not verificar:
            kwargs.pop('verificar')
        super(Questao, self).save(*args, **kwargs)
        
      
      