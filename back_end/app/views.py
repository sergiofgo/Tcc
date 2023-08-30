from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.http import JsonResponse
from django.core import serializers
from django.conf import settings
import json
import matplotlib.pyplot as plt
import numpy as np
import investpy as inv
import yfinance as yf
from workadays import workdays as wd
from datetime import timedelta,date,datetime
from .models import Bolsa_de_Valores, Acao, Predicao, Predicao_Atual, Predicao_Teste
from django.views.decorators.csrf import csrf_exempt

#Função que retorna a lista de empresas participantes e seus respectivos simbolos, provenientes de uma bolsa de valores selecionada
@csrf_exempt
def bolsas(request):
    body = json.loads(request.body)
    bolsa = body['exchange']
    return HttpResponse(Bolsa_de_Valores(bolsa).get_acoes())
  
#Função que retorna um dataframe com todas as informações necessárias para exibição do resultado da funcionalidade predição
@csrf_exempt
def resultado1(request):
    body = json.loads(request.body)
    acao = body['stock']
    bolsa = body['exchange']
    action = Acao (acao,bolsa)
    data = date.today() 
    return HttpResponse(Predicao_Atual(action).aux(data))
 
#Função que retorna um dataframe com todas as informações necessárias para exibição do resultado da funcionalidade teste 
@csrf_exempt 
def resultado2(request):
    body = json.loads(request.body)
    acao = body['stock']
    bolsa = body['exchange']
    data= datetime.strptime(body['data'],"%d/%m/%Y").date()
    action = Acao (acao,bolsa)
    return HttpResponse(Predicao_Teste(action,data).aux(data))


    
