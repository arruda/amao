# -*- coding: utf-8 -*-

from django.db import models    

from questao import Questao

class OpcaoMultiplaEscolha(models.Model):
    """
    Representa uma opcao multipla escolha, caso esse seja o caso da questao.
    É uma ligação de Muitas respostas para Uma questao.
    Essa classe permite a questao, mais de uma opcao correta, se for o caso, ou apenas uma correta.
    Tem uma lista de respostasMultiplaEscolha(ligacoes de QuestaoDeAvaliacao) que representam as respostas
    dos alunos(que também podem selecionar mais de uma opcao de resposta).
    """
    
    #por campo representando letra?
    #exemplo A, B, C...
    opcao = models.CharField(u"Opção",blank=False, null=False, max_length=250)
    #se essa resposta eh correta ou nao
    correta = models.DecimalField( max_digits=10, decimal_places=2,default="0.00")
    
    questao = models.ForeignKey(Questao,related_name="multiplaEscolhas")
    
    #se marcada essa opcao anula qualquer outra respondida e apenas sua nota é valida
    anular = models.BooleanField(u"Anular Todas?", default=True)
#    respostasMultiplaEscolha = models.ManyToManyField(QuestaoDeAvaliacao,related_name='opcoesMultiplaEscolha')
    
    class Meta:
        verbose_name = u'Opção Multipla Escolha'
        app_label = 'Questao'
    
    def __unicode__(self):
        return self.opcao
    
    @property
    def perc_nota(self):
        "retonar o percentual que essa opcao tem na nota total"
        return (self.questao.percentNotaMultipla/100 * self.correta/100)
    
    def get_nota(self,nota_questao_avaliacao):
        "retorna o quanto essa opcao vale da nota da questao de avaliacao passada por parametro"
        print nota_questao_avaliacao 
        print self.perc_nota 
        return nota_questao_avaliacao * self.perc_nota 
        
