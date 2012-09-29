#!/bin/bash
./manage.py loaddata fixtures/admin_user.yaml
./manage.py loaddata apps/Aluno/fixtures/test_alunos.yaml
./manage.py loaddata apps/Professor/fixtures/test_professor.yaml 
./manage.py loaddata apps/Materia/fixtures/test_materias.yaml
./manage.py loaddata apps/Materia/Turma/fixtures/test_turma.yaml 
./manage.py loaddata apps/Avaliacao/fixtures/test_avaliacao.yaml
./manage.py loaddata apps/Avaliacao/Questao/fixtures/test_questao.yaml 
