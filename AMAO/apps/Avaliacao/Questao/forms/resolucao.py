#-*- coding:utf-8 -*-
from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from Avaliacao.Questao.models import QuestaoDeAvaliacao

class ResolucaoQuestaoAvaliacaoForm(forms.ModelForm):
    
    class Meta:
        model = QuestaoDeAvaliacao
        fields = ('opcoesMultiplaEscolha','respostaDiscursiva')
        widgets = {'opcoesMultiplaEscolha': CheckboxSelectMultiple}
    

    def __init__(self, *args, **kwargs):
        super(ResolucaoQuestaoAvaliacaoForm, self).__init__(*args, **kwargs)
        self.fields['opcoesMultiplaEscolha'].queryset = self.instance.questao.multiplaEscolhas.all()
        
#    def __init__(self, *args, **kwargs):
#        super(MultiplaEscolhaForm, self).__init__(*args, **kwargs)
#        self.fields["opcoesMultiplaEscolha"].widget = CheckboxSelectMultiple