from django.shortcuts import render, redirect
from .models import Conta, Categoria
from django.contrib import messages
from extrato.models import Valores
from django.contrib.messages import constants
from .uteis import calcula_total, calcula_equilibrio_financeiro
from datetime import datetime
from contas.views import quantificar_contas

def home(request):
    contas = Conta.objects.all()
    valores = Valores.objects.filter(data__month = datetime.now().month)
    entradas = valores.filter(tipo = 'E')
    saidas = valores.filter(tipo = 'S')
    
    total_contas = calcula_total(contas, 'valor')
    total_entradas = calcula_total(entradas, 'valor')
    total_saidas = calcula_total(saidas, 'valor')
    
    percentual_gastos_essenciais, percentual_gastos_nao_essenciais = calcula_equilibrio_financeiro()
    t_contas_vencidas, t_contas_proximas_vencimento = quantificar_contas()
    
    return render(request, 'home.html', {'contas' : contas, 'total_contas' : total_contas, 'total_entradas': total_entradas, 'total_saidas': total_saidas,  'percentual_gastos_essenciais': round(percentual_gastos_essenciais), 'percentual_gastos_nao_essenciais': round(percentual_gastos_nao_essenciais), 't_contas_vencidas' : t_contas_vencidas, 't_contas_proximas_vencimento' : t_contas_proximas_vencimento})

def gerenciar(request):
    contas = Conta.objects.all()
    total_contas = 0
    categorias = Categoria.objects.all()
    total_contas = calcula_total(contas, 'valor')
    
    return render(request, 'gerenciar.html', {'contas' : contas, 'total_contas' : total_contas, 'categorias' : categorias})

def cadastrar_banco(request):
    apelido = request.POST.get('apelido')
    banco = request.POST.get('banco')
    tipo = request.POST.get('tipo')
    valor = request.POST.get('valor')
    icone = request.FILES.get('icone')
    
    # Caso o apelido ou valor nao seja preenchido, msg de erro
    if len(apelido.strip()) == 0 or len(banco.strip()) == 0 or len(tipo.strip()) == 0 or len(valor.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'Preencha todos os campos.')
        return redirect('/perfil/gerenciar')
    
    conta = Conta(
        apelido=apelido,
        banco=banco,
        tipo=tipo,
        valor=valor,
        icone=icone
    )
    
    conta.save()
    messages.add_message(request, constants.SUCCESS, 'Conta cadastrada com sucesso.')

    return redirect('/perfil/gerenciar/', {'conta': conta})

def deletar_banco(request, id):
    conta = Conta.objects.get(id=id)
    conta.delete()
    messages.add_message(request, constants.SUCCESS, 'Conta deletada com sucesso.')
    return redirect('/perfil/gerenciar/')

def cadastrar_categoria(request):
    nome = request.POST.get('categoria')
    essencial = bool(request.POST.get('essencial'))
    
    if len(nome.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'Preencha o nome da categoria.')
        return redirect('/perfil/gerenciar/')
    
    categoria = Categoria(
        categoria=nome,
        essencial=essencial
    )
    categoria.save()

    messages.add_message(request, constants.SUCCESS, 'Categoria cadastrada com sucesso')
    return redirect('/perfil/gerenciar/')

def update_categoria(request, id):
    categoria = Categoria.objects.get(id=id)
    categoria.essencial = not categoria.essencial
    categoria.save()
    
    return redirect('/perfil/gerenciar/')

def dashboard(request):
    dados = {}
    
    categorias = Categoria.objects.all()
    
    for categoria in categorias:
        total = 0
        valores = Valores.objects.filter(categoria=categoria)
        for v in valores:
            total += v.valor
            
        dados[categoria.categoria] = total
    
    return render(request, 'dashboard.html',{'labels': list(dados.keys()), 'values': list(dados.values())})