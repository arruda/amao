# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.contrib.auth import login
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from Aluno.views.utils import aluno_exist
from annoying.decorators import render_to

from django.contrib.auth.models import User
from Avaliacao.models import *
from Aluno.models import *

@render_to('avaliacao/exibir.html')
@aluno_exist
def exibir(request,template_id): 
    aluno = request.user.aluno_set.get()
    avaliacao=Avaliacao.objects.get(pk=template_id)
    questoes=avaliacao.questoes.all()
    return locals()

