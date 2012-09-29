from django.contrib import admin

from Materia.models import Materia
from Materia.Turma.models import Turma






class MateriaAdmin(admin.ModelAdmin):
    fieldsets = [
           ('Materia',               {'fields': ['nome','sigla']}),
    ]

    
    list_display = ('nome','sigla',)

class TurmaAdmin(admin.ModelAdmin):
    pass

admin.site.register(Materia, MateriaAdmin)
admin.site.register(Turma, TurmaAdmin)
