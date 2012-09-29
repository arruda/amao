from django.contrib import admin

from Professor.models import Professor






class ProfessorAdmin(admin.ModelAdmin):
    fieldsets = [
           ('Professor',               {'fields': ['usuario']}),
    ]

    
    list_display = ('usuario',)



admin.site.register(Professor, ProfessorAdmin)
