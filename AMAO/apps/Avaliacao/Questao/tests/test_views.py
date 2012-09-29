# -*- coding: utf-8 -*-
"""
    Questao.test_views
    ~~~~~~~~~~~~~~

    Testa coisas relacionada as views.

    :copyright: (c) 2011 by Sparkit.
"""
import os
from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from model_mommy import mommy
from Avaliacao.Questao.models import Questao, TipoQuestao

class QuestaoUploadTest(TestCase):

    fixtures = ['user_test_upload', 'tipoQuestao_test_upload']

    def setUp(self):
        self.c = Client(enforce_csrf_checks=False)
        self.tipoQuestao = TipoQuestao.objects.all()[0]
        self.usuario = User.objects.all()[0]
        self.fonte = 'apps/Avaliacao/Questao/tests/fontes/hello_world/hello_world.c'
        self.entrada = 'apps/Avaliacao/Questao/tests/entradas/hello_world/entrada_gabarito.txt'
        self.final_fonte = 'media/titulo/fontes/hello_world.c'
        self.final_entrada = 'media/titulo/entradas/entrada_gabarito.txt'


    def test_expected_fixtures(self):
        "verifica se as fixtures possuem os valores esperados para que sejam usadas nos testes"
        self.assertEqual(self.usuario.username, 'root')
        self.assertEqual(self.tipoQuestao.tipo, 'C')
        #verificar tambem se tem os arquivos de upload
        self.assertTrue(os.path.exists(self.fonte))
        self.assertTrue(os.path.exists(self.entrada))
        
    def test_upload_paths(self):
        "Vefica se esta sendo salvo nos locais corretos os arquivos de upload"
        fonte = open(self.fonte)
        entrada = open(self.entrada)

        #logar como root para usar o admin
#        self.c.login(username='root', password='root')
#        infos = {
#        'csrfmiddlewaretoken': '6f69d58f330c59c458661ebbea9b1ead',
#        'titulo':'titulo',
#        'enunciado':'Enunciado',
#        'tipo': '1',
#        'fontesGabarito-0-arquivo': fonte,
#        'entradasGabarito-0-arquivo': entrada,
#        '_save': 'Salvar'

#        }
#        r = self.c.get('/admin/Questao')
##        r = self.c.post('/admin/Questao/questao/add/',infos)
#        fonte.close()
#        entrada.close()
#    
#        questao = Questao.objects.get(pk=1)
#        for f in questao.fontesGabarito.all():
#            self.assertEqual(self.final_fonte,f.arquivo)
#        
        
