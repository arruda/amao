#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
DOC_DIR = "docs"
AMAO_DIR = "AMAO"
def generate_rst_for_app(app,excludes=None):
    command_template = "sphinx-apidoc -f -o %(APP_DOC_DIR)s %(APP)s %(EXCLUDES)s"
    app_doc_dir = os.path.abspath(os.path.join(DOC_DIR,app))
    abs_app_dir = os.path.abspath(os.path.join(AMAO_DIR,app))

    abs_exclude = [os.path.abspath(os.path.join(AMAO_DIR,d)) for d in excludes]
    excludes_str = " ".join(abs_exclude)
    command = command_template % { 'APP_DOC_DIR' : app_doc_dir, 'APP' : abs_app_dir, 'EXCLUDES' : excludes_str}
    print command
    os.system(command)


if __name__ == '__main__':
    generate_rst_for_app(
        'apps/Avaliacao',
        excludes=[
        # 'apps/Avaliacao/Questao',
        ]
    )
    # generate_rst_for_app(
    #     'apps/Aluno',
    #     excludes=[
    #     # 'apps/Avaliacao/Questao',
    #     ]
    # )
