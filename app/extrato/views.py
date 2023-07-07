from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from django.contrib import messages
from django.contrib.messages import constants
from django.db.models import Sum
from django.conf import settings
from django.template.loader import render_to_string

from perfil.models import Conta, Categoria
from . import models

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import os
from io import BytesIO
from weasyprint import HTML

def novo_valor(request):
    if request.method == "GET":
        contas = Conta.objects.all()
        categorias = Categoria.objects.all() 
        return render(request, 'extrato/novo_valor.html', {'contas': contas, 'categorias': categorias})
    elif request.method == "POST":
        valor = request.POST.get('valor')
        categoria = request.POST.get('categoria')
        descricao = request.POST.get('descricao')
        data = request.POST.get('data')
        conta = request.POST.get('conta')
        tipo = request.POST.get('tipo')

        valores = models.Valor(
            valor=valor,
            categoria_id=categoria,
            descricao=descricao,
            data=data,
            conta_id=conta,
            tipo=tipo,
        )
        valores.save()

        conta = Conta.objects.get(id=conta)
        if tipo == 'E':
            conta.valor += int(valor)
        else:
            conta.valor -= int(valor)
        conta.save()

        messages.add_message(request, constants.SUCCESS, 'Categoria cadastrada com sucesso!')
        return redirect('extrato:novo_valor')


def view_extrato(request):
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()
    valores = models.Valor.objects.all()
    periodo_filter_delta = {
        '7d': datetime.now() - timedelta(days=7),
        '1m': datetime.now() - relativedelta(months=1),
        '6m': datetime.now() - relativedelta(months=6),
        '1a': datetime.now() - relativedelta(years=1),
    }

    conta_filter = request.GET.get('conta')
    categoria_filter = request.GET.get('categoria')
    periodo_filter = request.GET.get('periodo')

    if conta_filter and conta_filter != "":
        valores = valores.filter(conta__id=conta_filter)

    if categoria_filter and categoria_filter != "":
        valores = valores.filter(categoria_id=categoria_filter)

    if periodo_filter and periodo_filter != "" and periodo_filter in periodo_filter_delta.keys():
        valores = valores.filter(data__gte=periodo_filter_delta.get(periodo_filter))

    return render(request, 'extrato/view_extrato.html', {'valores': valores, 'contas': contas, 'categorias': categorias})


def exportar_pdf(request):
    valores = models.Valor.objects.filter(data__month= datetime.now().month)

    path_tamplate = os.path.join(settings.BASE_DIR, 'templates/partials/extrato.html')
    template_render = render_to_string(path_tamplate, context={'valores': valores})

    pdf_path = BytesIO()
    HTML(string=template_render).write_pdf(pdf_path)
    pdf_path.seek(0)

    return FileResponse(pdf_path, filename="extrato.pdf")