# -*- coding: utf-8 -*-
"""
    Corretor.test_gabarito
    ~~~~~~~~~~~~~~

    Testa coisas relacionada ao corretor de C++ usado em questoes de gabarito.

    :copyright: (c) 2011 by Felipe Arruda Pontes.
"""
import os
#from django.test import TestCase
from libs.test_utils.test_cases import TestCaseMedia
#from model_mommy import mommy
from Corretor.corretor.corretor_cpp import CorretorCPP
from Avaliacao.Questao.models import Questao

from django.conf import settings

class Compilar_Test(TestCaseMedia):
    fixtures = ['test_questao']

    def setUp(self):
        self.corretor = CorretorCPP()
        
    def test_fixtures(self):
        "testar as fixtures e se os arquivos carregaram corretamente"
        #verifica se é o helloworld
        self.assertEquals(Questao.objects.get(pk=1).slug,'hello-world')
        

    def test_questao(self):
        "testar se compilou corretamente a questao hello world, q tem um unico fonte."
        self.questao = Questao.objects.get(pk=1)
        #verifica se compilou com sucesso(0)
        self.assertEquals(self.corretor.compilar(questao=self.questao),0)

    def test_questao_fontes(self):
        "testar se compilou corretamente a questao multiplos-fontes, q tem ++ fontes."
        self.questao = Questao.objects.get(slug='multiplos-fontes')
        #verifica se compilou com sucesso(0)
        self.assertEquals(self.corretor.compilar(questao=self.questao),0)

class Executar_Test(Compilar_Test):
    "Fazendo como herdando de compilar, já que para o cenario funcionar, deve ter que compilar tambem."

    def test_executar_questao(self):
        "testar se executa corretamente a questao hello-world. e se a saida dos arquivos é para o local correto."
        self.questao = Questao.objects.get(slug='hello-world')
        #verifica se compilou com sucesso(0)
        self.assertEquals(self.corretor.compilar(questao=self.questao),0)
        #escolhe o arquivo de entrada
        self.entrada = os.path.join(settings.MEDIA_ROOT,str(self.questao.entradasGabarito.all()[0]))
        self.assertEquals(self.corretor.executar(questao=self.questao,entrada_gabarito=self.entrada),0)
        
        saida = os.path.join(settings.MEDIA_ROOT,'gabarito/hello-world/saidas/hello-world')
        self.assertTrue(os.path.exists(saida))

    def test_executar_questao_fontes(self):
        "testar se executa corretamente a questao  multiplos-fontes. e se a saida dos arquivos é para o local correto."
        self.questao = Questao.objects.get(slug='multiplos-fontes')
        #verifica se compilou com sucesso(0)
        self.assertEquals(self.corretor.compilar(questao=self.questao),0)
        #escolhe o arquivo de entrada
        self.entrada = os.path.join(settings.MEDIA_ROOT,str(self.questao.entradasGabarito.all()[0]))
        self.assertEquals(self.corretor.executar(questao=self.questao,entrada_gabarito=self.entrada),0)
        
        saida = os.path.join(settings.MEDIA_ROOT,'gabarito/multiplos-fontes/saidas/multiplos-fontes')
        self.assertTrue(os.path.exists(saida))


