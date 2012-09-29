from django.contrib import admin

from Avaliacao.models import Avaliacao



class AvaliacaoAdmin(admin.ModelAdmin):
    fieldsets = [
           ('Avaliacao',               {'fields': ['titulo','templateAvaliacao','aluno','ativa']}),
    ]

    readonly_fields = ('ativa',)
    
    list_display = ('titulo',)


admin.site.register(Avaliacao, AvaliacaoAdmin)
