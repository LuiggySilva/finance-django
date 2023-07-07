from django.contrib import admin
from . import models

admin.site.register(models.Conta)

@admin.register(models.Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('categoria', 'essencial', 'valor_planejamento')
    list_filter = ('essencial',)