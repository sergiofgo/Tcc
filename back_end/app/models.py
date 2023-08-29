from django.db import models
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

class Acao():
    def __init__(self,acao,bolsa):
        self.acao= acao
        self.bolsa = bolsa
    def get_acao(self):
        return self.acao
    def get_bolsa(self):
        return self.bolsa

class Bolsa_de_Valores():
    def __init__(self,bolsa):
        self.bolsa = bolsa
    def get_acoes(self):
        info = inv.stocks.get_stocks('brazil')
        if (self.bolsa == '^BVSP'):
            info['symbol'] += '.SA'
        elif (self.bolsa == '^NYA' or self.bolsa =="^IXIC"):
            info = inv.stocks.get_stocks('united states')
        info = info.sort_values(by = 'full_name')  
        return info[['full_name','symbol']].to_json(index= False,orient ='table')
    
class Predicao ():
    def __init__(self,action):
        self.bolsa = action.bolsa
        self.acao = action.acao
    def aux(self, data):
        #criação dos dataframes com os historicos da ação e do indice da bolsa de valores selecionada
        if (data != date.today()):
            df = yf.download(self.acao, data - timedelta(60), data+timedelta(15))
            exchange = yf.download(self.bolsa, data- timedelta(60), data+timedelta(15))
        else:
            df = yf.download(self.acao, data - timedelta(50), data)
            exchange = yf.download(self.bolsa, data- timedelta(50), data) 
        
        #Criação, com o auxilio da biblioteca ta-lib das series rsi, macd e beta no dataframe, correspondentes aos indicadores técnicos
        self.indices_historic(df,exchange)
    
        #Criacão do conjunto Fuzzy corresponde a variavel rsi
        Rsi = control.Antecedent(np.arange(0,100,0.001),"Rsi")
        Rsi["Sobrevenda"] = fuzz.trapmf(Rsi.universe, [0,0,30,70])
        Rsi["Sobrecompra"] = fuzz.trapmf(Rsi.universe, [30,70,100,100])

        #Criação do conjunto Fuzzy corresponde a variavel Beta
        Beta = control.Antecedent(np.arange(-2,2,0.001),"Beta")
        Beta["Baixo"] = fuzz.trimf(Beta.universe, [-2,-1.25,-0.5])
        Beta["Neutro"] = fuzz.trimf(Beta.universe,[-1,0,1])
        Beta["Alto"] = fuzz.trimf(Beta.universe,[0.5,1.25,2])

        #Criação do conjunto Fuzzy corresponde a variavel Macd
        Macd = control.Antecedent(np.arange(-4,4,0.001),"Macd")
        Macd["Baixo"] = fuzz.trimf(Macd.universe, [-4,-1.5,1])
        Macd["Alto"] = fuzz.trimf(Macd.universe,[-1,1.5,4])

        #Criação do conjunto Fuzzy corresponde a variavel de saida Predicao
        Predicao = control.Consequent(np.arange(-3,3,0.01),'Predicao')
        Predicao["Vender"] = fuzz.trimf(Predicao.universe, [-3,-1.65,-0.3])
        Predicao["Manter"] = fuzz.trimf(Predicao.universe,[-1,0,1])
        Predicao["Comprar"] = fuzz.trimf(Predicao.universe,[0.3,1.65,3])

        #Definição das Regras Fuzzy que serão utilizadas na Inferência Fuzzy
        regra1 = control.Rule (Rsi['Sobrevenda']&Macd['Baixo']&Beta['Baixo'],Predicao['Vender'])
        regra2 = control.Rule (Rsi['Sobrecompra']&Macd['Baixo']&Beta['Baixo'],Predicao['Vender'])
        regra3 = control.Rule (Rsi['Sobrecompra']&Macd['Baixo']&Beta['Neutro'],Predicao['Vender'])
        regra4 = control.Rule (Rsi['Sobrevenda']&Macd['Baixo']&Beta['Neutro'],Predicao['Manter'])
        regra5 = control.Rule (Rsi['Sobrevenda']&Macd['Baixo']&Beta['Alto'],Predicao['Manter'])
        regra6 = control.Rule (Rsi['Sobrecompra']&Macd['Baixo']&Beta['Alto'],Predicao['Manter'])
        regra7 = control.Rule (Rsi['Sobrevenda']&Macd['Alto']&Beta['Baixo'],Predicao['Manter'])
        regra8 = control.Rule (Rsi['Sobrecompra']&Macd['Alto']&Beta['Baixo'],Predicao['Manter'])
        regra9 = control.Rule (Rsi['Sobrecompra']&Macd['Alto']&Beta['Neutro'],Predicao['Manter'])
        regra10 = control.Rule (Rsi['Sobrevenda']&Macd['Alto']&Beta['Neutro'],Predicao['Comprar'])
        regra11 = control.Rule (Rsi['Sobrevenda']&Macd['Alto']&Beta['Alto'],Predicao['Comprar'])
        regra12 = control.Rule (Rsi['Sobrecompra']&Macd['Alto']&Beta['Alto'],Predicao['Comprar'])
        
        #Inserção das regras Fuzzy no Controle do Sistema Fuzzy
        system = control.ControlSystem([regra1,regra2,regra3,regra4,regra5,regra6,regra7,regra8,regra9,regra10,regra11,regra12])
        
        #Criação do Controle de Sistema Fuzzy
        sim = control.ControlSystemSimulation(system)
        #Definição da data de referência
        data_ref = self.data_final(data,df)
 
        
        #Inserção dos dados discretos para realização da Fuzzificação
        sim.input['Rsi'] = df.loc[[data_ref]].Rsi.values[0]
        sim.input['Macd'] = df.loc[[data_ref]].Macd.values[0]
        sim.input['Beta'] = df.loc[[data_ref]].Beta.values[0]
        
        #calcula o sistema de controle fuzzy
        sim.compute()
        #Obtenção do subconjunto do Dataframe com periodo de 10 dias
        if (data != date.today()):
            df_aux = df[data_ref:data_ref + timedelta(10)]
        else:
            df_aux = df[data_ref - timedelta(10):data_ref]
            df_aux = df_aux[::-1]  
        
        
        #Criação do DataFrame om as informações que serão exibidas no Front End 
        list_index = [df_aux.index[i].strftime('%d/%m/%Y') for i in range (len(df_aux.index))]
        list_close = np.round(df_aux.Close.values,decimals =2)
        n = len(list_close)
        dr = pd.DataFrame({'Ação':[self.acao]+[0]*(n-1),'Resultado_Crisp': [np.round(sim.output['Predicao'],decimals = 2)]+[0]*(n-1),'Img_Pert':[np.round(fuzz.interp_membership(Predicao.universe,Predicao[self.resultado(sim.output['Predicao'],Predicao)].mf,sim.output['Predicao']),decimals = 2)]+[0]*(n-1),'Resultado_Fuzzy':[self.resultado(sim.output['Predicao'],Predicao)]+[0]*(n-1),'Data': list_index, 'Close': list_close,'Rsi':[np.round(df[data_ref:data_ref].Rsi.values[0],decimals = 2)]+[0]*(n-1),'Macd':[np.round(df[data_ref:data_ref].Macd.values[0], decimals = 2)]+[0]*(n-1), 'Beta':[np.round(df[data_ref:data_ref].Beta.values[0],decimals = 2)]+[0]*(n-1),'Tam':[n]+[0]*(n-1)})
        print(dr)
        #plotar(rsi, macd, beta,predicao,sim)
        return dr.to_json(index= False,orient ='table')
    #Cria as séries Rsi, Macd e Beta no Data Frame 
    def indices_historic (self, df,exchange):
        df["Rsi"] = ta.RSI(df.Close, timeperiod = 14)
        MACD,sinal,df["Macd"]= ta.MACD(df.Close, fastperiod=12, slowperiod=26, signalperiod=9)
        df["Beta"] = ta.BETA(exchange.Close, df.Close, timeperiod =30)

    #Obtendo o valor linguistico correspondente ao resultado obtido na defuzzificação 
    def resultado(self,val_out,predicao):
        img_predicao = ['Vender','Manter','Comprar']
        conj_img=[fuzz.interp_membership(predicao.universe,predicao["Vender"].mf,val_out), fuzz.interp_membership(predicao.universe, predicao["Manter"].mf,val_out),fuzz.interp_membership(predicao.universe,predicao["Comprar"].mf,val_out)] 
        max_index= conj_img.index(max(conj_img))
        return img_predicao[max_index]

    #Definir data final de referencia
    def data_final (self,data,df):
        data_ref = data
        if (data_ref == date.today()):
            return df.index[len(df.index)-1]
        #biblioteca workdays verifica se é dia util
        else:
            while (data_ref.strftime('%Y-%m-%d') not in df.index):
                data_ref = data_ref - timedelta(1)
            return data_ref

    
class Predicao_Atual(Predicao):
    def __init__(self,action):
         super().__init__(action)
class Predicao_Teste(Predicao):
    def __init__(self,action, data):
         super().__init__(action)
         self.data = data
    
