from django.shortcuts import render, redirect
from perfil.models import Categoria, Conta
from django.http import HttpResponse
from .models import Valores
from django.contrib import messages
from django.contrib.messages import constants

def novo_valor(request):
    if request.method == 'GET':
        contas = Conta.objects.all()
        categorias = Categoria.objects.all()
        return render(request, 'novo_valor.html', {'contas' : contas, 'categorias' : categorias})
    elif request.method == 'POST':
        valor = request.POST.get('valor')
        categoria = request.POST.get('categoria')
        descricao = request.POST.get('descricao')
        data = request.POST.get('data')
        conta = request.POST.get('conta')
        tipo = request.POST.get('tipo')
        
        valores = Valores(
            valor = valor,
            categoria_id = categoria,
            descricao = descricao,
            data = data,
            conta_id = conta,
            tipo = tipo,
        )
        
        valores.save()
        
        conta = Conta.objects.get(id=conta)
        
        if tipo == 'S':
            conta.valor -= int(valor)
            messages.add_message(request, constants.SUCCESS, 'Saída cadastrada com sucesso!')
        else:
            conta.valor += int(valor)
            messages.add_message(request, constants.SUCCESS, 'Entrada cadastrada com sucesso!')
            
        conta.save()
        
        return redirect('/extrato/novo_valor/')