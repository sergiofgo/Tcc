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
import talib as ta
import pandas as pd
import skfuzzy as fuzz
from skfuzzy import control
from workadays import workdays as wd
from datetime import timedelta,date,datetime
from django.views.decorators.csrf import csrf_exempt

#Função que retorna a lista de empresas participantes e seus respectivos simbolos, provenientes de uma bolsa de valores selecionada
@csrf_exempt
def bolsas(request):
    body = json.loads(request.body)
    bolsa = body['exchange']
    info = inv.stocks.get_stocks('brazil')
    if (bolsa == '^BVSP'):
        info['symbol'] += '.SA'
    elif (bolsa == '^NYA' or bolsa =="^IXIC"):
        info = inv.stocks.get_stocks('united states')
    info = info.sort_values(by = 'full_name')  
    return HttpResponse(info[['full_name','symbol']].to_json(index= False,orient ='table'))
  
#Função que retorna um dataframe com todas as informações necessárias para exibição do resultado da funcionalidade predição
@csrf_exempt
def resultado1(request):
    body = json.loads(request.body)
    acao = body['stock']
    bolsa = body['exchange']
    data = date.today()
    return HttpResponse(aux(acao,bolsa,data))
 
#Função que retorna um dataframe com todas as informações necessárias para exibição do resultado da funcionalidade teste 
@csrf_exempt 
def resultado2(request):
    body = json.loads(request.body)
    acao = body['stock']
    bolsa = body['exchange']
    data= datetime.strptime(body['data'],"%d/%m/%Y").date()
    return HttpResponse(aux(acao,bolsa,data))

def aux(acao,bolsa,data):
  #criação dos dataframes com os historicos da ação e do indice da bolsa de valores selecionada
    if (data != date.today()):
      df = yf.download(acao, data - timedelta(60), data+timedelta(15))
      exchange = yf.download(bolsa, data- timedelta(60), data+timedelta(15))
    else:
      df = yf.download(acao, data - timedelta(50), data)
      exchange = yf.download(bolsa, data- timedelta(50), data) 
      
    #Criação, com o auxilio da biblioteca ta-lib das series rsi, macd e beta no dataframe, correspondentes aos indicadores técnicos
    indices_historic(df,exchange)
    
    #Criacão do conjunto Fuzzy corresponde a variavel rsi
    rsi = control.Antecedent(np.arange(0,100,0.001),"Rsi")
    rsi["Sobrevenda"] = fuzz.trapmf(rsi.universe, [0,0,30,70])
    rsi["Sobrecompra"] = fuzz.trapmf(rsi.universe, [30,70,100,100])

    #Criação do conjunto Fuzzy corresponde a variavel Beta
    beta = control.Antecedent(np.arange(-2,2,0.001),"Beta")
    beta["Baixo"] = fuzz.trimf(beta.universe, [-2,-1.25,-0.5])
    beta["Neutro"] = fuzz.trimf(beta.universe,[-1,0,1])
    beta["Alto"] = fuzz.trimf(beta.universe,[0.5,1.25,2])

    #Criação do conjunto Fuzzy corresponde a variavel Macd
    macd = control.Antecedent(np.arange(-4,4,0.001),"Macd")
    macd["Baixo"] = fuzz.trimf(macd.universe, [-4,-1.5,1])
    macd["Alto"] = fuzz.trimf(macd.universe,[-1,1.5,4])

    #Criação do conjunto Fuzzy corresponde a variavel de saida Predicao
    predicao = control.Consequent(np.arange(-3,3,0.001),'Predicao')
    predicao["Vender"] = fuzz.trimf(predicao.universe, [-3,-1.65,-0.3])
    predicao["Manter"] = fuzz.trimf(predicao.universe,[-1,0,1])
    predicao["Comprar"] = fuzz.trimf(predicao.universe,[0.3,1.65,3])

    #Definição das Regras Fuzzy que serão utilizadas na Inferência Fuzzy
    regra1 = control.Rule (rsi['Sobrevenda']&macd['Baixo']&beta['Baixo'],predicao['Vender'])
    regra2 = control.Rule (rsi['Sobrecompra']&macd['Baixo']&beta['Baixo'],predicao['Vender'])
    regra3 = control.Rule (rsi['Sobrecompra']&macd['Baixo']&beta['Neutro'],predicao['Vender'])
    regra4 = control.Rule (rsi['Sobrevenda']&macd['Baixo']&beta['Neutro'],predicao['Manter'])
    regra5 = control.Rule (rsi['Sobrevenda']&macd['Baixo']&beta['Alto'],predicao['Manter'])
    regra6 = control.Rule (rsi['Sobrecompra']&macd['Baixo']&beta['Alto'],predicao['Manter'])
    regra7 = control.Rule (rsi['Sobrevenda']&macd['Alto']&beta['Baixo'],predicao['Manter'])
    regra8 = control.Rule (rsi['Sobrecompra']&macd['Alto']&beta['Baixo'],predicao['Manter'])
    regra9 = control.Rule (rsi['Sobrecompra']&macd['Alto']&beta['Neutro'],predicao['Manter'])
    regra10 = control.Rule (rsi['Sobrevenda']&macd['Alto']&beta['Neutro'],predicao['Comprar'])
    regra11 = control.Rule (rsi['Sobrevenda']&macd['Alto']&beta['Alto'],predicao['Comprar'])
    regra12 = control.Rule (rsi['Sobrecompra']&macd['Alto']&beta['Alto'],predicao['Comprar'])
    
    #Inserção das regras Fuzzy no Controle do Sistema Fuzzy
    system = control.ControlSystem([regra1,regra2,regra3,regra4,regra5,regra6,regra7,regra8,regra9,regra10,regra11,regra12])
    
    #Criação do Controle de Sistema Fuzzy
    sim = control.ControlSystemSimulation(system)
    
    #Definição da data de referência
    data_ref = data_final(data,df)
    #Inserção dos dados discretos para realização da Fuzzificação
    sim.input['Rsi'] = df.loc[[data_ref]].Rsi.values[0]
    sim.input['Macd'] = df.loc[[data_ref]].Macd.values[0]
    sim.input['Beta'] = df.loc[[data_ref]].Beta.values[0]
    
    #calcula o sistema de controle fuzzy
    sim.compute()
    
    #Obtenção do subconjunto do Dataframe com periodo de 15 dias
    if (data != date.today()):
      df_aux = df[data_ref:data_ref + timedelta(10)]
    else:
      df_aux = df[data_ref - timedelta(10):data_ref]
      df_aux = df_aux[::-1]  
    
    #Criação do DataFrame om as informações que serão exibidas no Front End 
    list_index = [df_aux.index[i].strftime('%d/%m/%Y') for i in range (len(df_aux.index))]
    list_close = np.round(df_aux.Close.values,decimals =2)
    n = len(list_close)
    dr = pd.DataFrame({'Ação':[acao]+[0]*(n-1),'Resultado_Crisp': [np.round(sim.output['Predicao'],decimals = 2)]+[0]*(n-1),'Img_Pert':[np.round(fuzz.interp_membership(predicao.universe,predicao[resultado(sim.output['Predicao'],predicao)].mf,sim.output['Predicao']),decimals = 2)]+[0]*(n-1),'Resultado_Fuzzy':[resultado(sim.output['Predicao'],predicao)]+[0]*(n-1),'Data': list_index, 'Close': list_close,'Rsi':[np.round(df[data_ref:data_ref].Rsi.values[0],decimals = 2)]+[0]*(n-1),'Macd':[np.round(df[data_ref:data_ref].Macd.values[0], decimals = 2)]+[0]*(n-1), 'Beta':[np.round(df[data_ref:data_ref].Beta.values[0],decimals = 2)]+[0]*(n-1),'Tam':[n]+[0]*(n-1)})
    print(dr)
    #plotar(rsi, macd, beta,predicao,sim)
    return dr.to_json(index= False,orient ='table')
 
#Cria as séries Rsi, Macd e Beta no Data Frame 
def indices_historic (df,exchange):
  df["Rsi"] = ta.RSI(df.Close, timeperiod = 14)
  MACD,sinal,df["Macd"]= ta.MACD(df.Close, fastperiod=12, slowperiod=26, signalperiod=9)
  df["Beta"] = ta.BETA(exchange.Close, df.Close, timeperiod =30)

#Obtendo o valor linguistico correspondente ao resultado obtido na defuzzificação 
def resultado(val_out,predicao):
  img_predicao = ['Vender','Manter','Comprar']
  conj_img=[fuzz.interp_membership(predicao.universe,predicao["Vender"].mf,val_out), fuzz.interp_membership(predicao.universe, predicao["Manter"].mf,val_out),fuzz.interp_membership(predicao.universe,predicao["Comprar"].mf,val_out)] 
  max_index= conj_img.index(max(conj_img))
  return img_predicao[max_index]

#Definir data final de referencia
def data_final(data,df):
  data_ref = data
  if (data_ref == date.today()):
    return df.index[len(df.index)-1]
  
#biblioteca workdays verifica se é dia util
  else:
    while (data_ref.strftime('%Y-%m-%d') not in df.index):
      data_ref = data_ref - timedelta(1)
    return data_ref

#obter graficos dos testes
def plotar(rsi,macd,beta,predicao,sim):
  rsi.view(sim = sim)
  plt.savefig('C:\\Users\\Lenovo\Desktop\\rsi.png', format='png')
  macd.view(sim = sim)
  plt.savefig('C:\\Users\\Lenovo\\Desktop\\macd.png', format='png')
  beta.view(sim = sim)
  plt.savefig('C:\\Users\Lenovo\\Desktop\\besta.png')