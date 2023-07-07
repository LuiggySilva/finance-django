from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.messages import constants
from django.db.models import Sum

from . import models


def home(request):
    contas = models.Conta.objects.all()
    total = contas.aggregate(Sum('valor'))['valor__sum']
    return render(request, "perfil/home.html", context={'contas':contas, 'total':total})


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

    if len(categoria.strip()) == 0:
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