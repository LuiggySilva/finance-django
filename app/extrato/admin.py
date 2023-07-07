from django.contrib import admin
from . import models

@admin.register(models.Valor)
class ValorAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'categoria', 'data', 'conta', 'tipo', 'valor')
    list_filter = ('conta', 'categoria', 'tipo')
