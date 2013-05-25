# -*- coding: utf-8 -*-

from django.db import models
from Corretor.base import CorretorException
from Corretor.base import ExecutorException
from Corretor.base import CompiladorException
from Corretor.base import ComparadorException
from Corretor.base import LockException
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
    msg = models.TextField(u"Mensagem",blank=True,null=True)
    task_id = models.CharField(max_length=350,blank=True,null=True)
    class Meta:
        verbose_name = u'Retorno Correção'
        app_label = 'Corretor'


    def __unicode__(self):
        return "%s: %s" %(self.TIPOS[self.tipo][1],self.msg)

    def altera_dados(self,sucesso=True,erroException=None):
        """
        Altera os dados do retorno atual para pegar os dados de erro ou para por a mensagem
        que foi com sucesso.
        """

        tipo = RetornoCorrecao.TIPOS.correto
        correcao_msg = "Correto!"
        # print ">>altera_dados"
        # print ">>isinstance(erroException,CorretorException)",isinstance(erroException,CorretorException)

        if sucesso == True:
            # print ">>retorno.successful()"
            tipo = RetornoCorrecao.TIPOS.correto
            correcao_msg = "Correto!"
        elif isinstance(erroException,CorretorException):
            # print "erro: %s" % erroException.message
            if isinstance(erroException,ExecutorException):
                correcao_msg = erroException.message
                tipo = RetornoCorrecao.TIPOS.execucao
            if isinstance(erroException,CompiladorException):
                correcao_msg = erroException.message
                tipo = RetornoCorrecao.TIPOS.compilacao
            if isinstance(erroException,ComparadorException):
                correcao_msg = erroException.message
                tipo = RetornoCorrecao.TIPOS.comparacao
            if isinstance(erroException,LockException):
                correcao_msg = erroException.message
                tipo = RetornoCorrecao.TIPOS.lock

        self.tipo = tipo
        self.msg = correcao_msg
