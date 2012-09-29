# -*- coding: utf-8 -*-
"""
    Aluno.test_models
    ~~~~~~~~~~~~~~

    Testa coisas relacionada ao modelo.

    :copyright: (c) 2011 by Felipe Arruda Pontes.
"""

from django.test import TestCase
from model_mommy import mommy
from Aluno.models import Aluno

class AlunoTest(TestCase):

#    fixtures = ['estados', 'cidades']

    def setUp(self):
        self.aluno = mommy.make_one(Aluno)



        
    def test_aluno_save(self):
        " verifica se consegue salvar um aluno "
        self.aluno.save()
        
        self.assertEqual(self.aluno.id, 1)
    
