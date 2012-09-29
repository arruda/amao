#-*- coding:utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from Avaliacao.Questao.models import QuestaoDeAvaliacao

class AlterarNotaQuestaoForm(forms.ModelForm):

    class Meta:
        model = QuestaoDeAvaliacao
        fields = ('nota','revisao',)


