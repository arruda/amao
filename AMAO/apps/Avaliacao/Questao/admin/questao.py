from django.contrib import admin

from Avaliacao.Questao.models import Questao, QuestaoDeAvaliacao, TipoQuestao,\
 Fonte, OpcaoMultiplaEscolha, FonteGabarito, EntradaGabarito




class FonteInline(admin.TabularInline):
    model = Fonte
    extra = 4


class FonteGabaritoInline(admin.TabularInline):
    model = FonteGabarito
    extra = 4


class EntradaGabaritoInline(admin.TabularInline):
    model = EntradaGabarito
    extra = 4
    
class OpcaoMultiplaEscolhaInline(admin.TabularInline):
    model = OpcaoMultiplaEscolha
#    exclude = ('respostasMultiplaEscolha',)
    extra = 4




class QuestaoAdmin(admin.ModelAdmin):
    fieldsets = [
           ('Questao',               {'fields': ['titulo','enunciado','tipo','id_corretor','verificada']}),
           
           ('Notas',               {'fields': ['percentNotaProgramacao','percentNotaMultipla','percentNotaDiscursiva']}),
           
           ('Discursiva',               {'fields': ['respostaDiscursiva',]}),
    ]
    readonly_fields = ('verificada',)
    #retirando resposta multipla escolha do admin para evitar problemas.
    inlines = [OpcaoMultiplaEscolhaInline,FonteGabaritoInline,EntradaGabaritoInline]
    
    list_display = ('titulo','enunciado','slug','verificada',)

class TipoQuestaoAdmin(admin.ModelAdmin):
    fieldsets = [
           ('TipoQuestao',               {'fields': ['tipo','tipoPai']}),
    ]
    list_display = ('tipo','tipoPai',)
    
class QuestaoDeAvaliacaoAdmin(admin.ModelAdmin):
    fieldsets = [
           ('QuestaoDeAvaliacao',               {'fields': ['avaliacao','questao','nota','filtro']}),
    ]
    inlines = [FonteInline]
    
    list_display = ('id',)



admin.site.register(Questao, QuestaoAdmin)
admin.site.register(TipoQuestao, TipoQuestaoAdmin)
admin.site.register(QuestaoDeAvaliacao, QuestaoDeAvaliacaoAdmin)


