from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.messages import constants
from django.db.models import Sum

from datetime import datetime

from . import models
from extrato.models import Valor
from conta.views import ver_contas_aux


def calcula_equilibrio_financeiro():
    gastos_essenciais = Valor.objects.filter(data__month=datetime.now().month).filter(tipo='S').filter(categoria__essencial=True)
    gastos_nao_essenciais = Valor.objects.filter(data__month=datetime.now().month).filter(tipo='S').filter(categoria__essencial=False)

    total_gastos_essenciais = gastos_essenciais.aggregate(Sum('valor'))['valor__sum']
    total_gastos_nao_essenciais = gastos_nao_essenciais.aggregate(Sum('valor'))['valor__sum']

    total = total_gastos_essenciais + total_gastos_nao_essenciais
    try:
        percentual_gastos_essenciais = total_gastos_essenciais * 100 / total
        percentual_gastos_nao_essenciais = total_gastos_nao_essenciais * 100 / total

        return percentual_gastos_essenciais, percentual_gastos_nao_essenciais
    except:
        return 0, 0


def home(request):
    contas = models.Conta.objects.all()
    total = contas.aggregate(Sum('valor'))['valor__sum']

    valores = Valor.objects.filter(data__month=datetime.now().month)
    entradas = valores.filter(tipo='E')
    saidas = valores.filter(tipo='S')

    total_entradas = entradas.aggregate(Sum('valor'))['valor__sum']
    total_saidas = saidas.aggregate(Sum('valor'))['valor__sum']
    total_livre = total_entradas - total_saidas
    percentual_gastos_essenciais, percentual_gastos_nao_essenciais = calcula_equilibrio_financeiro()


    _, contas_proximas_vencimento, contas_vencidas = ver_contas_aux()

    return render(
        request, 
        "perfil/home.html", 
        context= {
            'contas':contas, 
            'total':total,
            'total_entradas':total_entradas,
            'total_saidas':total_saidas,
            'total_livre':total_livre,
            'percentual_gastos_essenciais':int(percentual_gastos_essenciais),
            'percentual_gastos_nao_essenciais':int(percentual_gastos_nao_essenciais),
            'contas_proximas_vencimento':contas_proximas_vencimento, 
            'contas_vencidas':contas_vencidas
        }
    )


def gerenciar(request):
    contas = models.Conta.objects.all()
    categorias = models.Categoria.objects.all()
    total = contas.aggregate(Sum('valor'))['valor__sum']
    return render(request, "perfil/gerenciar.html", context={'contas':contas, 'categorias':categorias, 'total':total})


def remover_banco(request, id):
    conta = models.Conta.objects.get(id= id)
    conta.delete()
    messages.add_message(request, constants.SUCCESS, "Conta removida com sucesso!")
    return redirect('perfil:gerenciar')


def cadastrar_banco(request):
    apelido = request.POST.get('apelido')
    banco = request.POST.get('banco')
    tipo = request.POST.get('tipo')
    valor = request.POST.get('valor')
    icone = request.FILES.get('icone')

    if (len(apelido.strip()) == 0 or len(banco.strip()) == 0 or 
        len(tipo.strip()) == 0 or len(valor.strip()) == 0):
        messages.add_message(request, constants.ERROR, "Preencha todos os campos!")
        return redirect('perfil:gerenciar')

    conta = models.Conta(apelido=apelido, banco=banco, tipo=tipo, valor=valor)
    conta.save()
    messages.add_message(request, constants.SUCCESS, "Conta cadastrada com sucesso!")
    return redirect('perfil:gerenciar')


def cadastrar_categoria(request):
    categoria = request.POST.get('categoria')
    essencial = bool(request.POST.get('essencial'))
    print(request.POST)
    if categoria and len(categoria.strip()) == 0:
        messages.add_message(request, constants.ERROR, "Preencha todos os campos!")
        return redirect('perfil:gerenciar')
    
    categoria = models.Categoria(categoria=categoria, essencial=essencial)
    categoria.save()
    messages.add_message(request, constants.SUCCESS, "Categoria cadastrada com sucesso!")
    return redirect('perfil:gerenciar')


def atualizar_categoria(request, id):
    categoria = models.Categoria.objects.get(id= id)
    categoria.essencial = not categoria.essencial
    categoria.save()
    return redirect('perfil:gerenciar')


def dashboard(request):
    dados = {}
    categorias = models.Categoria.objects.all()

    for categoria in categorias:
        dados[categoria.categoria] = Valor.objects.filter(categoria=categoria).aggregate(Sum('valor'))['valor__sum']

    return render(request, 'perfil/dashboard.html', {'labels': list(dados.keys()), 'values': list(dados.values())})