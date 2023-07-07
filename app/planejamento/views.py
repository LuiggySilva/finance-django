from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum

from perfil.models import Categoria
from extrato.models import Valor
import json, locale
from datetime import datetime
locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')


def definir_planejamento(request):
    categorias = Categoria.objects.all()
    return render(request, 'planejamento/definir_planejamento.html', {'categorias': categorias})


@csrf_exempt
def atualizar_valor_categoria(request, id):
    valor = json.loads(request.body)['valor']

    if float(valor) >= 0:
        categoria = Categoria.objects.get(id=id)
        categoria.valor_planejamento = valor
        categoria.save()
        return JsonResponse({'status':'Sucesso!'})
    
    return JsonResponse({'status':'Erro!'})


def ver_planejamento(request):
    valores = Valor.objects.filter(tipo='S')
    valores = valores.filter(data__month=datetime.now().month)
    total_gasto_geral = valores.aggregate(Sum('valor'))['valor__sum']

    categorias = Categoria.objects.all()
    planejamento_total_gasto = categorias.aggregate(Sum('valor_planejamento'))['valor_planejamento__sum']
    
    porcentagem_geral = int((total_gasto_geral * 100) / planejamento_total_gasto)
    mes_atual = datetime.now().strftime('%B')

    return render(
        request, 
        'planejamento/ver_planejamento.html', 
        context = {
            'categorias': categorias,
            'mes_atual': mes_atual.capitalize(),
            'total_gasto_geral': total_gasto_geral,
            'planejamento_total_gasto': planejamento_total_gasto,
            'porcentagem_geral': porcentagem_geral
        }
    )