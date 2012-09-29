from django.contrib import admin

from Aluno.models import Aluno





class AlunoAdmin(admin.ModelAdmin):
    fieldsets = [
           ('Aluno',               {'fields': ['usuario','matricula']}),
    ]

    
    list_display = ('usuario','matricula',)



admin.site.register(Aluno, AlunoAdmin)
