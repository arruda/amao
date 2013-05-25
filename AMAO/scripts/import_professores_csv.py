# -*- coding: utf-8 -*-
import csv

from django.contrib.auth.models import User
from Professor.models import Professor



def run():
    reader = csv.reader(open('scripts/professores.csv', 'rb'), delimiter=';')#, quotechar='|'
    print "inserindo professores"
    for al in reader:
        #matricula = al[0]
        nome = al[0]
        email = al[1]
        
        user = User(email=email,first_name=nome)
        user.save()
        user.username=user.id
        user.set_password('12345')
        user.save()
        professor = user.professor_set.create()
        print "  %s %s" %(nome,email) 