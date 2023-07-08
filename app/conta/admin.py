from django.contrib import admin
from . import models


@admin.register(models.ContaPagar)
class ContaPagarAdmin(admin.ModelAdmin):
    list_display = ('titulo','categoria','valor',)
    list_filter = ('categoria',)

@admin.register(models.ContaPaga)
class ContaPagaAdmin(admin.ModelAdmin):
    list_display = ('conta','data_pagamento',)