# -*- coding: utf-8 -*-

from django.db import models

from django_extensions.db.fields import AutoSlugField
from abs_models import Abs_titulado_slugfy
#from Materia.models import Materia
from Corretor.base import CorretorException,ComparadorException,CompiladorException, ExecutorException
from template_avaliacao import TemplateAvaliacao
import threading
import datetime


class Avaliacao(Abs_titulado_slugfy):
    """
    Classe que representa a avaliacao feita/sendo feita por um aluno
    ou um simulado
    """
    aluno = models.ForeignKey('Aluno.Aluno', related_name="avaliacoes")
    #template de avaliacao que gerou essa avaliacao
    templateAvaliacao = models.ForeignKey(TemplateAvaliacao,related_name="avaliacoes")
    ativa = models.BooleanField(u"Ativa",default=True)
    #:indica se essa avaliacao é um simulado ou uma avaliacao oficial
    simulado = models.BooleanField(u"Simulado?",default=False)
    data_inicio = models.DateTimeField(u"Data de Inicio")
    data_termino = models.DateTimeField(u"Data de Termino")
    class Meta:
        verbose_name = u'Avaliação'
        app_label = 'Avaliacao'

        
    def add_questao(self,questao,filtro):
        kwargs={filtro:filtro,nota:"0.00"}
        if questao.__class__.__name__ == "Questao":
            kwargs['questao']=questao
        else:
            kwargs['pk']=questao
            
        q = self.questoes.create(questao=questao,filtro=filtro,nota="0.00")
#        print q
#        for fonte in q.questao.fontesGabarito.filter(usarNaResolucao=True):
#            fonte.copiar_para_aluno(q)

    @property
    def get_nota(self):
        "retorna o quanto o aluno fez nessa avaliacao"
        res =0
        for questao in self.questoes.all():
            res += questao.nota
        return res
    
    def __corrigir_questao(self,**kwargs):
        "metodo carregado em cada thread de terminar"
        questao = kwargs.get('questao',None)
        corretor = questao.questao.corretor()
        try:
            corretor.corrigir(**kwargs)
        except CorretorException as erro:
            pass
        
    def terminar(self):
        "termina essa avaliacao, ao terminar é executado uma correção geral, cada questao é corrigina em uma thread diferente."
        self.ativa=False
        self.save()
        for questao in self.questoes.all():
            t = threading.Thread(target=self.__corrigir_questao,
                                 args=[],
                                 kwargs={'questao':questao})
            t.setDaemon(True)
            t.start()
    
    @classmethod
    def get_or_create(cls,templateAvaliacao,aluno,simulado=False):
        """recupera uma avaliacao se ja houver(evitando ter mais de uma avaliacao/simulado ao mesmo tempo
            para o mesmo templateAvaliacao, se nao houver então cria e retorna o mesmo.
        """
        #verifica se ja existe uma avaliacao/simulado para esse aluno nesse template.
        try:
            #se existir pega a mesma
            avaliacao = cls.objects.get(templateAvaliacao=templateAvaliacao,aluno=aluno,simulado=simulado)
        except cls.DoesNotExist:
            #caso nao exista cria uma 
            avaliacao = templateAvaliacao.gerarAvaliacao(aluno,simulado=simulado)

        return avaliacao
    
    @property
    def terminada(self):
        """
        retorna True se não estiver ativa e
         se não for um simulado e o template estiver terminado
         se for um simulado deve ser considerado se o tempo de termino é coerente. 
        """
        if self.ativa:
            return False
        
        if not self.simulado:
            return self.templateAvaliacao.terminada
        else:
            return self.data_termino >= datetime.datetime.now()
                
            
