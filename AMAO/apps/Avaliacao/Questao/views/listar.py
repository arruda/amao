# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, redirect
from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required

from Professor.views.utils import prof_monit_exist
from Professor.models import Professor, Monitor
from Avaliacao.Questao.forms import FiltroQuestaoForm
from Avaliacao.Questao.models import Questao

@prof_monit_exist
@login_required
@render_to('avaliacao/questao/listar.html')
def listar_questoes(request):
    # autor = request.user
    # questoes_validas = Questao.objects.filter(verificada=True)
    # questoes_invalidas = Questao.objects.filter(verificada=False)
    # import pdb; pdb.set_trace()

    filter_form = FiltroQuestaoForm(request.user,request.GET)

    if filter_form.is_valid():
        questoes = filter_form.get_questoes()

    return locals()
