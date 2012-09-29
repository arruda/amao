#-*- coding:utf-8 -*-
from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from Avaliacao.Questao.models import Questao , TipoQuestao



class criarQuestaoForm(forms.ModelForm):
    class Meta:
        model = Questao
        exclude= ('autor',)
        
      
class criarTipoQuestaoForm(forms.ModelForm):
    class Meta:
        model = TipoQuestao
        
    def __init__(self, *args, **kwargs):
        super(criarTipoQuestaoForm, self).__init__(*args, **kwargs)