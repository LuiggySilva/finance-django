from django.db import models
from django.db.models import Sum
from datetime import datetime

class Categoria(models.Model):
    categoria = models.CharField(max_length=50)
    essencial = models.BooleanField(default=False)
    valor_planejamento = models.FloatField(default=0)

    def __str__(self):
        return self.categoria

    def total_gasto(self):
        from extrato.models import Valor
        valores = Valor.objects.filter(categoria__id=self.id, tipo='S')
        valores = valores.filter(data__month=datetime.now().month)
        total = valores.aggregate(Sum('valor'))['valor__sum']
        return total if total else 0
    
    def percentual_gasto_total(self):
        return int((self.total_gasto() * 100) / self.valor_planejamento) if self.valor_planejamento != 0 else 100


class Conta(models.Model):
    banco_choices = (
        ('NU', 'Nubank'),
        ('CE', 'Caixa Economica'),
    )
    tipo_choices = (
        ('PF', 'Pessoa Fisica'),
        ('PJ', 'Pessoa Juridica'),
    )

    apelido = models.CharField(max_length=50)
    banco = models.CharField(max_length=2, choices=banco_choices)
    tipo = models.CharField(max_length=2, choices=tipo_choices)
    valor = models.FloatField()
    icone = models.ImageField(upload_to="icones")

    def __str__(self):
        return self.apelido