from django.contrib import admin

from Avaliacao.models import  TemplateAvaliacao
from Avaliacao.Questao.models import FiltroQuestao

class FiltroQuestaoInline(admin.TabularInline):
    model = FiltroQuestao
    extra = 4


class TemplateAvaliacaoAdmin(admin.ModelAdmin):
    fieldsets = [
           ('Template de Avaliacao',               {'fields': ['titulo','turma','ativa','data_inicio','data_termino','permite_simulado']}),
    ]

    readonly_fields = ('ativa',)
    inlines = [FiltroQuestaoInline]
    
    list_display = ('titulo',)



admin.site.register(TemplateAvaliacao, TemplateAvaliacaoAdmin)
