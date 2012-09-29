from django.contrib import admin

from Teste.models import TesteQuestao, Fontes




class FontesInline(admin.TabularInline):
    model = Fontes
    extra = 4



class TesteQuestaoAdmin(admin.ModelAdmin):
    fieldsets = [
           ('Questao',               {'fields': ['titulo','enunciado','user','entrada','saidaRef','saida']}),
    ]

    inlines = [FontesInline]
    
    list_display = ('titulo','enunciado','user','entrada','saidaRef','saida',)



admin.site.register(TesteQuestao, TesteQuestaoAdmin)
