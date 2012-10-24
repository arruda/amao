# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, redirect
from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required

from Aluno.views.utils import aluno_exist
from Avaliacao.Questao.models import QuestaoDeAvaliacao, Fonte, OpcaoMultiplaEscolha



@aluno_exist
@login_required  
@render_to('aluno/avaliacao/listar.html')
def listar_avaliacoes(request):    
    aluno = request.user.aluno_set.get()    
    
    avaliacoes_comecar = aluno.avaliacoes_iniciar()
    avaliacoes_andamento = aluno.avaliacoes_andamento()
    avaliacoes_passadas =  aluno.avaliacoes_passadas()
    avaliacoes_futuras = aluno.avaliacoes_futuras()
    
    return locals()