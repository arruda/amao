# -*- coding: utf-8 -*-
"""
    Professor.test_models
    ~~~~~~~~~~~~~~

    Testa coisas relacionada ao modelo.

    :copyright: (c) 2011 by Felipe Arruda Pontes.
"""

from django.test import TestCase
from model_mommy import mommy
from Professor.models import Professor, Monitor

class ProfessorTest(TestCase):


    def setUp(self):
        self.professor = mommy.make_one(Professor)

        
    def test_professor_save(self):
        " verifica se consegue salvar um professor "
        self.professor.save()
        
        self.assertEqual(self.professor.id, 1)
    

class MonitorTest(TestCase):


    def setUp(self):
        self.monitor = mommy.make_one(Monitor)

        
    def test_monitor_save(self):
        " verifica se consegue salvar um monitor "
        self.monitor.save()
        
        self.assertEqual(self.monitor.id, 1)
    
