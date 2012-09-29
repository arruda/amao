# -*- coding: utf-8 -*-

from decimal import Decimal
from django.db import models    


from django.conf import settings
from lockable import Lockable
from multipla_escolha import OpcaoMultiplaEscolha
from questao import Questao
from filtro_questao import FiltroQuestao
from Corretor.models import RetornoCorrecao
        
class QuestaoDeAvaliacao(Lockable):
    """
    Classe que representa a ligacao entre avaliacao e questao, que tambem esta ligado de forma indireta a Fonte
    (sendo referenciado por FK)
    """
    avaliacao =  models.ForeignKey('Avaliacao.Avaliacao', related_name='questoes')    
    questao = models.ForeignKey(Questao, related_name='avaliacoes')    
    nota = models.DecimalField(u'Nota',max_digits=10, decimal_places=2,default=Decimal("0.0"))
    perc_prog = models.DecimalField(u'Percentual de Acerto de Programação',max_digits=10, decimal_places=2,default=Decimal("0.0"))
    perc_mult = models.DecimalField(u'Percentual de Acerto de Multipla Escolha',max_digits=10, decimal_places=2,default=Decimal("0.0"))
    perc_disc = models.DecimalField(u'Percentual de Acerto de Discursiva',max_digits=10, decimal_places=2,default=Decimal("0.0"))
    #filtro que gerou essa questao
    filtro = models.ForeignKey(FiltroQuestao,related_name="questoesGeradas")
    
    revisao = models.TextField(null=True, blank=True)
    
    retorno_correcao = models.ForeignKey('Corretor.RetornoCorrecao',blank=True,null=True, on_delete=models.SET_NULL)
    
#    retorno_correcao = models.CharField(max_length=350,blank=True,null=True)
    
    opcoesMultiplaEscolha = models.ManyToManyField(OpcaoMultiplaEscolha,related_name='respostasMultiplaEscolha',blank=True,null=True)
    respostaDiscursiva = models.TextField(u"Resposta Discursiva",blank=True, null=True)
    
    class Meta:
        verbose_name = u'Questão de Avaliação'
        app_label = 'Questao'

            
    def __unicode__(self):
        return  self.avaliacao.titulo + "." + self.questao.titulo
        
    def verifica_aluno(self,aluno):
        "verifica se o aluno em questao pode fazer essa questao"
        if self.avaliacao.simulado:
            return (self.avaliacao.templateAvaliacao.verifica_simulado_aluno(aluno) and self.avaliacao.ativa==True)  
        
        return (self.avaliacao.templateAvaliacao.verifica_aluno(aluno) and self.avaliacao.ativa==True)  
    
    @property
    def get_nota_minima(self):
        """retorna a nota minima que pode ser tirada nessa questao,
        basicamente pega o atributo de nota limite minimo do  filtro dessa questao"""
        
        return self.filtro.notaLimMinimo
    
    @property
    def get_nota_maxima(self):
        """retorna a nota maxima que pode ser tirada nessa questao,
        basicamente pega o atributo de nota limite maximo do  filtro dessa questao"""
        
        return self.filtro.notaLimMaximo
    
    @property
    def get_nota_prog_max(self):
        "retona a nota maxima de programacao"
        return self.filtro.notaBase * self.questao.percentNotaProgramacao/100
    
    @property
    def get_nota_prog(self):
        "retona a nota de programacao"
        return self.get_nota_prog_max * self.perc_prog
    
    @property
    def get_nota_mult_max(self):
        "retona a nota maxima de multipla escolha"
        return self.filtro.notaBase * self.questao.percentNotaMultipla/100
    
    @property
    def get_nota_mult(self):
        "retona a nota de multipla escolha"
        return self.get_nota_mult_max * self.perc_mult
    
    @property
    def get_nota_disc_max(self):
        "retona a nota maxima de discursiva"
        return self.filtro.notaBase * self.questao.percentNotaDiscursiva/100
    
    @property
    def get_nota_disc(self):
        "retona a nota de discursiva"
        return self.get_nota_disc_max * self.perc_disc
    
    
    @property
    def get_opcao_anuladora(self):
        """retorna a opcao anuladora caso o aluno a tenha marcado
        se o aluno marcar mais de uma é considerada a que tem menor valor.
        se nao tiver nenhuma retorna None
        """
        opcao = self.opcoesMultiplaEscolha.filter(anular=True)
        return opcao.order_by('-correta')[0] if opcao.count() != 0 else None
    
    @property
    def get_retorno_or_create(self):
        
        retorno = self.retorno_correcao
        if not self.retorno_correcao:
            retorno = RetornoCorrecao()
            retorno.save()
            self.retorno_correcao = retorno
            
        return retorno
#    def set_retorno_correcao(self,**kwargs):
#        "cria ou altera o retorno atual para ficar com as informacoes de kwargs"
#        if self.retorno_correcao = 
#    def dar_nota(self,nota_corretor):
#        "dada uma nota do corretor é feita uma conta(verificando o filtro da questao) para dizer quanto o aluno ficou nessa questao"
#        nota = Decimal(nota_corretor * self.filtro)