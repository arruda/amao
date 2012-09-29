# -*- coding: utf-8 -*-
"""
    Materia.test_models
    ~~~~~~~~~~~~~~

    Testa coisas relacionada ao modelo.

    :copyright: (c) 2011 by Felipe Arruda Pontes.
"""

from django.test import TestCase
from model_mommy import mommy
from Materia.models import Materia

class MateriaTest(TestCase):


    def setUp(self):
        self.materia = mommy.make_one(Materia)

        
    def test_materia_save(self):
        " verifica se consegue salvar um materia "
        self.materia.save()
        
        self.assertEqual(self.materia.id, 1)
    
