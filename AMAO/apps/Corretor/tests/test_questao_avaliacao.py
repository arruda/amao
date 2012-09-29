# -*- coding: utf-8 -*-
"""
    Corretor.test_questao_avaliacao
    ~~~~~~~~~~~~~~

    Testa coisas relacionada ao corretor de C++
   com relação a questoes feitas por um aluno.

    :copyright: (c) 2011 by Felipe Arruda Pontes.
"""
import os
#from django.test import TestCase
from decimal import Decimal
from django.conf import settings
from libs.test_utils.test_cases import TestCaseMedia
#from model_mommy import mommy
from Corretor.corretor.corretor_cpp import CorretorCPP
from Avaliacao.models import TemplateAvaliacao
from Avaliacao.Questao.models import Questao, QuestaoDeAvaliacao
from Aluno.models import Aluno

#class Compilar_Test(TestCaseMedia):
#    fixtures = ['test_alunos','test_avaliacao','test_questao']

#    def setUp(self):
#        self.corretor = CorretorCPP()
#        
#    def test_fixtures(self):
#        "testar as fixtures e se os arquivos carregaram corretamente"
#        #verifica se é o helloworld
#        self.assertEquals(QuestaoDeAvaliacao.objects.get(pk=1).questao.slug,'hello-world')
#        self.assertEquals(QuestaoDeAvaliacao.objects.get(pk=2).questao.slug,'multiplos-fontes')
#        self.assertEquals(Aluno.objects.get(pk=1).slug,'123456')
#        

#    def test_questao(self):
#        "testar se compilou corretamente a questao de avaliacao hello world, q tem um unico fonte."
#        self.questao = QuestaoDeAvaliacao.objects.get(pk=1)
#        #verifica se compilou com sucesso(0)
#        self.assertEquals(self.corretor.compilar(questao=self.questao),0)
#        mkfile = os.path.join(settings.MEDIA_ROOT,'123456/avaliacao-correta/hello-world/mkfiles/hello-world')

#    def test_questao_fontes(self):
#        "testar se compilou corretamente a questao de avaliacao  multiplos-fontes, q tem ++ fontes."
#        self.questao = QuestaoDeAvaliacao.objects.get(pk=2)
#        #verifica se compilou com sucesso(0)
#        self.assertEquals(self.corretor.compilar(questao=self.questao),0)
#        mkfile = os.path.join(settings.MEDIA_ROOT,'123456/avaliacao-correta-2/multiplos-fontes/mkfiles/multiplos-fontes')

#class Executar_Test(Compilar_Test):
#    "Fazendo como herdando de compilar, já que para o cenario funcionar, deve ter que compilar tambem."

#    def test_executar_questao(self):
#        "testar se executa corretamente a questao de avaliacao hello-world. e se a saida dos arquivos é para o local correto."
#        self.questao = QuestaoDeAvaliacao.objects.get(pk=1)#hello-world
#        self.assertEquals(self.questao.avaliacao.pk,1)
#        #verifica se compilou com sucesso(0)
#        self.assertEquals(self.corretor.compilar(questao=self.questao),0)
#        #escolhe o arquivo de entrada
#        self.entrada = os.path.join(settings.MEDIA_ROOT,str(self.questao.questao.entradasGabarito.all()[0]))
#        self.assertEquals(self.corretor.executar(questao=self.questao,entrada_gabarito=self.entrada),0)
#        
#        saida = os.path.join(settings.MEDIA_ROOT,'123456/avaliacao-correta/hello-world/saidas/hello-world')
#        self.assertTrue(os.path.exists(saida))

#    def test_executar_questao_fontes(self):
#        "testar se executa corretamente a questao de avaliacao multiplos-fontes. e se a saida dos arquivos é para o local correto."
#        self.questao = QuestaoDeAvaliacao.objects.get(pk=2)#multiplos-fontes
#        #verifica se compilou com sucesso(0)
#        self.assertEquals(self.corretor.compilar(questao=self.questao),0)
#        #escolhe o arquivo de entrada
#        self.entrada = os.path.join(settings.MEDIA_ROOT,str(self.questao.questao.entradasGabarito.all()[0]))
#        self.assertEquals(self.corretor.executar(questao=self.questao,entrada_gabarito=self.entrada),0)
#        
#        saida = os.path.join(settings.MEDIA_ROOT,'123456/avaliacao-correta-2/multiplos-fontes/saidas/multiplos-fontes')
#        self.assertTrue(os.path.exists(saida))

#class Comparar_Test(Executar_Test):
#    "Fazendo como herdando de executar, já que para o cenario funcionar, deve ter que executar tambem."

#    def test_comparar_questao(self):
#        "testar se compara corretamente a questao hello-world."
#        self.questao = QuestaoDeAvaliacao.objects.get(pk=1)
#        
#        #verifica se os arquivos de saida existem
#        saida_gabarito = os.path.join(settings.MEDIA_ROOT,'gabarito/hello-world/saidas/hello-world')
#        saida = os.path.join(settings.MEDIA_ROOT,'123456/avaliacao-correta/hello-world/saidas/hello-world')
#        self.assertTrue(os.path.exists(saida_gabarito))
#        self.assertTrue(os.path.exists(saida))

#        self.assertEquals(self.corretor.comparar(questao=self.questao,gabarito=self.questao.questao),0)
#        
#    def test_comparar_questao_fontes(self):
#        "testar se compara corretamente a questao multiplos-fontes."
#        self.questao = QuestaoDeAvaliacao.objects.get(pk=2)
#        
#        #verifica se os arquivos de saida existem
#        saida_gabarito = os.path.join(settings.MEDIA_ROOT,'gabarito/multiplos-fontes/saidas/multiplos-fontes')
#        saida = os.path.join(settings.MEDIA_ROOT,'123456/avaliacao-correta-2/multiplos-fontes/saidas/multiplos-fontes')

#        self.assertEquals(self.corretor.comparar(questao=self.questao,gabarito=self.questao.questao),0)


class Corrigir_Test(TestCaseMedia):
    "Fazendo como herdando de comparar, já que para o cenario funcionar, deve ter que comparar tambem."

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
        

    def test_corrigir_questao(self):
        "testar se corrige corretamente a questao hello-world."
        self.questao = QuestaoDeAvaliacao.objects.get(pk=1)
        self.questao.fontes.create(arquivo='123456/avaliacao-correta/hello-world/fontes/hello_world.cpp')
        self.assertEquals(self.corretor.corrigir(questao=self.questao,limitar=["prog"]),Decimal('5'))
        self.assertEquals(QuestaoDeAvaliacao.objects.get(pk=1).nota, Decimal('5'))

    def test_corrigir_questao_fontes(self):
        "testar se corrige corretamente a questao multiplos-fontes."
        self.questao = QuestaoDeAvaliacao.objects.get(pk=2)
        self.questao.fontes.create(arquivo='123456/avaliacao-correta/multiplos-fontes/fontes/hello_world.h')
        self.questao.fontes.create(arquivo='123456/avaliacao-correta/multiplos-fontes/fontes/main.cpp')
        self.assertEquals(self.corretor.corrigir(questao=self.questao,limitar=["prog"]),Decimal('5'))
        self.assertEquals(QuestaoDeAvaliacao.objects.get(pk=2).nota, Decimal('5'))

    def test_corrigir_questao_parcial(self):
        "testar se corrige corretamente a questao parcial."
        self.templateAvaliacao = TemplateAvaliacao.objects.get(pk=2)
        self.avaliacao = self.templateAvaliacao.gerarAvaliacao(self.aluno)
        self.assertEquals(QuestaoDeAvaliacao.objects.get(pk=3).questao.slug,'questao-parcial')
        self.questao = QuestaoDeAvaliacao.objects.get(pk=3)
        self.questao.fontes.create(arquivo='123456/avaliacao-parcial/questao-parcial/fontes/hello_world.h')
        self.assertEquals(self.corretor.corrigir(questao=self.questao,limitar=["prog"]),Decimal('10'))
        self.assertEquals(QuestaoDeAvaliacao.objects.get(pk=3).nota, Decimal('10'))
        