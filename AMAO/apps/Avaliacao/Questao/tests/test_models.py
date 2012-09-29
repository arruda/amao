# -*- coding: utf-8 -*-
"""
    Questao.test_models
    ~~~~~~~~~~~~~~

    Testa coisas relacionada ao modelo.

    :copyright: (c) 2011 by Felipe Arruda Pontes.
"""

from django.test import TestCase
from model_mommy import mommy
from Avaliacao.Questao.models import Questao

class QuestaoTest(TestCase):


    def setUp(self):
        self.questao = mommy.make_one(Questao)

        
    def test_avaliacao_save(self):
        " verifica se consegue salvar um questao "
        self.questao.verificada = True
        self.questao.save(verificar=False)
        
        self.assertEqual(self.questao.id, 1)
        self.assertEqual(self.questao.verificada, True)
    
