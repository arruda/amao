# -*- coding: utf-8 -*-
import csv

from django.contrib.auth.models import User
from Aluno.models import Aluno



def run():
    reader = csv.reader(open('scripts/alunos.csv', 'rb'), delimiter=';')#, quotechar='|'
    print "inserindo alunos"
    for al in reader:
        matricula = al[0]
        nome = al[1]
        email = al[2]
        
        user = User(email=email,first_name=nome)
        user.save()
        user.username=user.id
        user.set_password(matricula)
        user.save()
        al = user.aluno_set.create(matricula=matricula)
        print "  %s %s %s" %(matricula,nome,email)