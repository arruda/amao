#-*- coding:utf-8 -*-
from django import forms
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User
from Avaliacao.Questao.models import QuestaoDeAvaliacao

class ResponderQuestaoForm(forms.ModelForm):

    class Meta:
        model = QuestaoDeAvaliacao
        exclude = ('avaliacao','questao')


