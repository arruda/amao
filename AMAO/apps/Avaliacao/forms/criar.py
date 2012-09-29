#-*- coding:utf-8 -*-
from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from Materia.Turma.models import Turma
from Avaliacao.models import TemplateAvaliacao, Avaliacao
from Avaliacao.Questao.models import QuestaoDeAvaliacao, Questao ,FiltroQuestao

class criarTemplateAvaliacaoForm(forms.ModelForm):
    #titulo=forms.CharField(max_length=100)
    #data_inicio=forms.DateTimeField()
    #data_termino=forms.DateTimeField()
    #turma = forms.ModelChoiceField(queryset = Turma.objects.all(), required=True)
    
    class Meta:
        model = TemplateAvaliacao
        
    def __init__(self, *args, **kwargs):
        super(criarTemplateAvaliacaoForm, self).__init__(*args, **kwargs)
        self.fields['turma'].queryset = Turma.objects.all()    
    
class criarFiltroQuestaoForm(forms.ModelForm):
    
    class Meta:
        model = FiltroQuestao
#        
#    def __init__(self, *args, **kwargs):
#        super(criarFiltroQuestaoForm, self).__init__(*args, **kwargs)
#        self.fields['questaoExata'].queryset = Questao.objects.all()
        
        
    #templateAvaliacao = forms.ModelChoiceField(queryset = TemplateAvaliacao.objects.all(), required=True)   
    # notaBase = forms.DecimalField(u"Nota Base",max_digits=10, decimal_places=2)
    #------- notaLimMinimo = forms.DecimalField(max_digits=10, decimal_places=2)
    #------- notaLimMaximo = forms.DecimalField(max_digits=10, decimal_places=2)
    #--- questaoExata = forms.ModelChoiceField(queryset = Questao.objects.all())