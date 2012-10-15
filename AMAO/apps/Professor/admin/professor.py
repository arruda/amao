from django.contrib import admin

from Professor.models import Professor
from Professor.models import Monitor






class ProfessorAdmin(admin.ModelAdmin):
    fieldsets = [
           ('Professor',               {'fields': ['usuario']}),
    ]

    
    list_display = ('usuario',)



admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Monitor, admin.ModelAdmin)
