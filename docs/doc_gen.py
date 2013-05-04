#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import shutil

DOC_DIR = "."
AMAO_DIR = "../AMAO"
def generate_rst_for_app(app,excludes=None):
    "Cria os arquivos .rst para a app em questao usando o sphinx-apidoc"
    command_template = "sphinx-apidoc -f -o %(APP_DOC_DIR)s %(APP)s %(EXCLUDES)s"
    app_doc_dir = os.path.abspath(os.path.join(DOC_DIR,app))
    abs_app_dir = os.path.abspath(os.path.join(AMAO_DIR,app))

    abs_exclude = [os.path.abspath(os.path.join(AMAO_DIR,d)) for d in excludes]
    excludes_str = " ".join(abs_exclude)
    command = command_template % { 'APP_DOC_DIR' : app_doc_dir, 'APP' : abs_app_dir, 'EXCLUDES' : excludes_str}
    print command
    os.system(command)

def clean_rsts():
    "limpa todos os rsts menos o index.rst"
    shutil.rmtree('apps',ignore_errors=True)
    shutil.rmtree('libs',ignore_errors=True)
    shutil.rmtree('settings',ignore_errors=True)
    pass

def generate_rsts():
    "Gera todos os rsts necessarios para a doc"
    generate_rst_for_app(
        'apps/Aluno',
        excludes=[
        # 'apps/Avaliacao/Questao',
        ]
    )
    generate_rst_for_app(
        'apps/Avaliacao',
        excludes=[
        ]
    )
    generate_rst_for_app(
        'apps/Core',
        excludes=[
        ]
    )
    generate_rst_for_app(
        'apps/Corretor',
        excludes=[
        ]
    )
    generate_rst_for_app(
        'apps/Materia',
        excludes=[
        ]
    )
    generate_rst_for_app(
        'apps/Professor',
        excludes=[
        ]
    )
    generate_rst_for_app(
        'libs/abs_models',
        excludes=[
        ]
    )
    generate_rst_for_app(
        'libs/context_processors',
        excludes=[
        ]
    )
    generate_rst_for_app(
        'libs/htmlt_boilerplate',
        excludes=[
        ]
    )
    generate_rst_for_app(
        'libs/test_utils',
        excludes=[
        ]
    )
    generate_rst_for_app(
        'libs/user_backends',
        excludes=[
        ]
    )

def clean_docs():
    command = "make clean"
    print command
    os.system(command)

def generate_html():
    print "Generate HTML"
    clean_docs()
    command = "make html"
    print command
    os.system(command)

if __name__ == '__main__':
    doc_type = sys.argv[1] if len(sys.argv) > 1 else "html"
    gen = globals()['generate_'+doc_type]
    clean_rsts()
    generate_rsts()
    gen()
