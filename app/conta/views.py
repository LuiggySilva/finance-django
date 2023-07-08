from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from django.contrib import messages
from django.contrib.messages import constants

from datetime import datetime

from perfil.models import Categoria
from extrato.models import Valor
from . import models

def definir_conta(request):
    if request.method == "GET":
        categorias = Categoria.objects.all() 
        return render(request, 'conta/definir_conta.html', {'categorias': categorias})
    else:
        titulo = request.POST.get('titulo')
        categoria = request.POST.get('categoria')
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
        dia_pagamento = request.POST.get('dia_pagamento')

        conta = models.ContaPagar(
            titulo=titulo,
            categoria_id=categoria,
            descricao=descricao,
            valor=valor,
            dia_pagamento=dia_pagamento
        )
        conta.save()
        
        messages.add_message(request, constants.SUCCESS, 'Conta cadastrada com sucesso!')
        return redirect('conta:definir_conta')


def ver_contas_aux():
    MES_ATUAL = datetime.now().month
    DIA_ATUAL = datetime.now().day

    contas = models.ContaPagar.objects.all()

    contas_pagas = models.ContaPaga.objects.filter(data_pagamento__month=MES_ATUAL).values('conta')

    contas_vencidas = contas.filter(dia_pagamento__lt=DIA_ATUAL).exclude(id__in=contas_pagas)
    
    contas_proximas_vencimento = contas.filter(
        dia_pagamento__lte = DIA_ATUAL + 5
    ).filter(
        dia_pagamento__gte=DIA_ATUAL
    ).exclude(
        id__in=contas_pagas
    )
    
    restantes = contas.exclude(
        id__in=contas_vencidas
    ).exclude(
        id__in=contas_pagas
    ).exclude(
        id__in=contas_proximas_vencimento
    )

    return contas_pagas, contas_proximas_vencimento, contas_vencidas

def ver_contas(request):


    contas_pagas, contas_proximas_vencimento, contas_vencidas = ver_contas_aux()

    contas = models.ContaPagar.objects.all()
    restantes = contas.exclude(
        id__in=contas_vencidas
    ).exclude(
        id__in=contas_pagas
    ).exclude(
        id__in=contas_proximas_vencimento
    )

    return render(
        request, 
        'conta/ver_contas.html', 
        context= {
            'contas_vencidas': contas_vencidas, 
            'contas_proximas_vencimento': contas_proximas_vencimento, 
            'restantes': restantes
        }
    )