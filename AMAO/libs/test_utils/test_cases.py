# -*- coding: utf-8 -*-
"""
    test_utils.test_cases
    ~~~~~~~~~~~~~~

    Alguns test cases ja com configurações pre-definidas

    :copyright: (c) 2011 by Felipe Arruda Pontes.
"""
import os
from django.test import TestCase
from django.conf import settings

class TestCaseMedia(TestCase):

    def test_media_root(self):
        " verifica se o media root esta corretamente setado para usar media de teste "
        self.assertEqual(os.path.split(settings.MEDIA_ROOT)[1],'teste')
        
