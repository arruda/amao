# -*- coding: utf-8 -*-
import os
from django.conf import settings
class CorretorException(Exception):

    def _limitar_texto_msg(self, msg, questao=None):
        """
        Dado o texto de msg de erro e uma questao(de avaliacao),

        remove o começo das paths para impedir que os usuarios possam se usar disso.

        Assim o texto:

            /home/arruda/projetos/amao/AMAO/media/123456/avaliacao-slug/questao-slug/fontes/main.c

        se torna isso:

            .../123456/avaliacao-slug/questao-slug/fontes/main.c


        """
        # from Avaliacao.Questao.models import path_base
        # base = path_base(questao=questao.questao,aluno=questao.avaliacao.aluno,avaliacao=questao.avaliacao)
        base_abs = settings.MEDIA_ROOT
        # os.path.join(settings.MEDIA_ROOT,base)
        return msg.replace(base_abs,'...')

    def __init__(self,msg, questao=None):
        self.message =self._limitar_texto_msg(msg,questao=questao)

class LockException(CorretorException):
    pass

class CompiladorException(CorretorException):
    pass

class ExecutorException(CorretorException):
    pass

class ComparadorException(CorretorException):
    pass


class Corretor(object):
    """
    Uma classe que representa um corretor, e seu metodos.
    """

    def __init__(self):
        pass
#        self.nome = "Corretor"
#        self.descricao = "Corretor de Base"

#    class Meta:
#        app_label = 'Corretor'
#        abstract = True

    def pre_compilar(self,**kwargs):
        """Metodo chamado antes de se compilar
        """
        return

    def compilar(self, **kwargs):
        """Metodo chamado quando se precisa compilar os arquivos
        """
        return

    def pos_compilar(self,**kwargs):
        """Metodo chamado depois de se compilar
        """
        return

    def compilar_completo(self,**kwargs):
        """Chama todos os metodos de compilar na ordem correta
        """
        return self.pre_compilar(**kwargs),self.compilar(**kwargs),self.pos_compilar(**kwargs)

    def pre_executar(self,**kwargs):
        """Metodo chamado antes de se executar
        """
        return

    def executar(self, **kwargs):
        """Metodo chamado quando se precisa executar um programa
        """
        return

    def pos_executar(self,**kwargs):
        """Metodo chamado depois de se executar
        """
        return

    def executar_completo(self,**kwargs):
        """Chama todos os metodos de executar na ordem correta
        """
        return self.pre_executar(**kwargs),self.executar(**kwargs),self.pos_executar(**kwargs)

    def pre_comparar(self,**kwargs):
        """Metodo chamado antes de se comparar
        """
        return

    def comparar(self, **kwargs):
        """Metodo chamado quando se precisa comparar o resultado com um gabarito
        """
        return

    def pos_comparar(self,**kwargs):
        """Metodo chamado depois de se comparar
        """
        return

    def comparar_completo(self,**kwargs):
        """Chama todos os metodos de comparar na ordem correta
        """
        return self.pre_comparar(**kwargs),self.comparar(**kwargs),self.pos_comparar(**kwargs)

    def avaliar(self, **kwargs):
        """Metodo chamado quando se precisa fazer alguma avaliacao alem da comparacao
        """
        return

    def corrigir(self, **kwargs):
        """Metodo chamado para fazer a correçao.
        Este metodo chama os outros metodos necessarios para fazer a mesma, e usa uma questao de avaliacao como parametros principais.
        """
        return

    def nota(self,**kwargs):
        """Metodo chamado para fazer dar a nota de uma questao.
        """
        return

