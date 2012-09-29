from django.contrib import admin

from Avaliacao.Questao.models import Questao, QuestaoDeAvaliacao, TipoQuestao, Fonte, RespostaMultiplaEscolha, FonteGabarito, EntradaGabarito




class FonteInline(admin.TabularInline):
    model = Fonte
    extra = 4


class FonteGabaritoInline(admin.TabularInline):
    model = FonteGabarito
    extra = 4


class EntradaGabaritoInline(admin.TabularInline):
    model = EntradaGabarito
    extra = 4
    
class RespostaMultiplaEscolhaInline(admin.TabularInline):
    model = RespostaMultiplaEscolha
    extra = 4




class QuestaoAdmin(admin.ModelAdmin):
    fieldsets = [
           ('Questao',               {'fields': ['titulo','enunciado','tipo']}),
    ]

    inlines = [RespostaMultiplaEscolhaInline,FonteGabaritoInline,EntradaGabaritoInline]
    
    list_display = ('titulo','enunciado','slug')

class TipoQuestaoAdmin(admin.ModelAdmin):
    fieldsets = [
           ('TipoQuestao',               {'fields': ['tipo','tipoPai']}),
    ]
    list_display = ('tipo','tipoPai',)
    
class QuestaoDeAvaliacaoAdmin(admin.ModelAdmin):
    fieldsets = [
           ('QuestaoDeAvaliacao',               {'fields': ['avaliacao','questao']}),
    ]
    inlines = [FonteInline]
    
    list_display = ('avaliacao','questao',)



admin.site.register(Questao, QuestaoAdmin)
admin.site.register(TipoQuestao, TipoQuestaoAdmin)
admin.site.register(QuestaoDeAvaliacao, QuestaoDeAvaliacaoAdmin)


