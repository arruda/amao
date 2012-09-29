# -*- coding: utf-8 -*-
"""
    Corretor.test_questao_avaliacao_erro
    ~~~~~~~~~~~~~~

    Testa coisas relacionada ao corretor de C++
   com relação a questoes feitas por um aluno, porem de forma errada.
   Justamente para testar se quando feito de forma incorreta as questoes sao corrigidas e o resultado
    é que deu incorreto.

    :copyright: (c) 2011 by Felipe Arruda Pontes.
"""
import os
#from django.test import TestCase
from decimal import Decimal
from django.conf import settings
from libs.test_utils.test_cases import TestCaseMedia
#from model_mommy import mommy
from Corretor.corretor.corretor_cpp import CorretorCPP
from Avaliacao.Questao.models import Questao, QuestaoDeAvaliacao
from Avaliacao.models import TemplateAvaliacao
from Aluno.models import Aluno
from Corretor.base import ComparadorException, CompiladorException, ExecutorException

class Base_Erro_Test(TestCaseMedia):
    fixtures = ['test_alunos','test_avaliacao','test_questao']

    def setUp(self):
        self.corretor = CorretorCPP()
        self.aluno = Aluno.objects.get(pk=1)
        self.templateAvaliacao = TemplateAvaliacao.objects.get(pk=1)
        self.avaliacao = self.templateAvaliacao.gerarAvaliacao(self.aluno)
        
    def test_fixtures(self):
        "testar as fixtures e se os arquivos carregaram corretamente"
        #verifica se é o helloworld
        self.assertEquals(QuestaoDeAvaliacao.objects.get(pk=1).questao.slug,'hello-world')
        self.assertEquals(QuestaoDeAvaliacao.objects.get(pk=2).questao.slug,'multiplos-fontes')
        self.assertEquals(Aluno.objects.get(pk=1).slug,'123456')
        
class Compilar_Erro_Test(Base_Erro_Test):

    def test_compila_questao(self):
        "testar se compilou incorretamente a questao de avaliacao hello world, q tem um unico fonte."
        self.questao = QuestaoDeAvaliacao.objects.get(pk=1)
        self.questao.fontes.create(arquivo='123456/avaliacao-correta/hello-world/fontes/hello_world_erro_compilacao.cpp')
        try:
#            self.fail("Deveria dar erro na compilação e não deu1.")
            self.corretor.corrigir(questao=self.questao,limitar=["prog"])
            self.fail("Deveria dar erro na compilação e não deu.")
        except CompiladorException:
            pass
        self.assertEquals(QuestaoDeAvaliacao.objects.get(pk=1).nota, Decimal('0'))
        
class Executa_Erro_Test(Base_Erro_Test):

    def test_executa_questao(self):
        "testar se executou incorretamente a questao de avaliacao hello world, q tem um unico fonte."
        self.questao = QuestaoDeAvaliacao.objects.get(pk=1)
        self.questao.fontes.create(arquivo='123456/avaliacao-correta/hello-world/fontes/hello_world_erro_execucao.cpp')
        try:
#            self.fail("Deveria dar erro na compilação e não deu1.")
            self.corretor.corrigir(questao=self.questao,limitar=["prog"])
            self.fail("Deveria dar erro na execucao e não deu.")
        except ExecutorException:
            pass

        self.assertEquals(QuestaoDeAvaliacao.objects.get(pk=1).nota, Decimal('0'))


class Comparar_Erro_Test(Base_Erro_Test):
    "Compara uma questao que tem a resposta errada basicamente."
    
    def test_comparar_questao(self):
        "testar se compara incorretamente a questao hello-world."
        self.questao = QuestaoDeAvaliacao.objects.get(pk=1)
        self.questao.fontes.create(arquivo='123456/avaliacao-correta/hello-world/fontes/hello_world_erro_comparacao.cpp')
        try:
            self.corretor.corrigir(questao=self.questao,limitar=["prog"])
            self.fail("Deveria dar erro na comparacao e não deu.")
        except ComparadorException:
            pass
        self.assertEquals(QuestaoDeAvaliacao.objects.get(pk=1).nota, Decimal('0'))
        