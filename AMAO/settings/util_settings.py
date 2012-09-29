#coding: utf-8
#from path import path
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_ROOT =os.path.dirname(PROJECT_ROOT)
sys.path.append(SITE_ROOT)

sys.path.append(os.path.join(PROJECT_ROOT,'apps'))
sys.path.append(os.path.join(PROJECT_ROOT,PROJECT_ROOT, 'libs'))

LOCAL = lambda x: os.path.join(
                '/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-1]), x)
