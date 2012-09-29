# -*- coding: utf-8 -*-
"""
    Turma.test_models
    ~~~~~~~~~~~~~~

    Testa coisas relacionada ao modelo.

    :copyright: (c) 2011 by Felipe Arruda Pontes.
"""

from django.test import TestCase
from model_mommy import mommy
from Materia.Turma.models import Turma

class TurmaTest(TestCase):


    def setUp(self):
        self.turma = mommy.make_one(Turma)

        
    def test_turma_save(self):
        " verifica se consegue salvar um turma "
        self.turma.save()
        
        self.assertEqual(self.turma.id, 1)
    
