import React,{useState,useEffect} from 'react';
import {View,Text,TouchableOpacity,Button,StyleSheet,SafeAreaView,KeyboardAvoidingView,Dimensions,Picker,TextInput,Platform,ScrollView} from 'react-native';
import {css} from '../assets/Css/css';
import {Table, TableWrapper, Row, Rows, Col, Cols, Cell} from 'react-native-table-component';
import {LineChart,BarChart} from 'react-native-chart-kit';

export default function Preditor2 ({route}) {
    const date = [];
    const close = [];
    const tam = route.params?.transf.data[0].Tam;
    for(var i = tam-1; i >=0; i--){
        date.push(route.params?.transf.data[i].Data);
    }
    for(var i = tam-1; i >=0; i--){
        close.push(route.params?.transf.data[i].Close);
    }
    const Valores = {
      tableHead : ['Data','Ativo','Rsi(0-100)','Macd','Beta (%)','Grau de Pertinência (μ)','Recomendação'],
      tableBody : [route.params?.transf.data[0].Data,route.params?.transf.data[0].Ação,route.params?.transf.data[0].Rsi,route.params?.transf.data[0].Macd,route.params?.transf.data[0].Beta ,route.params?.transf.data[0].Img_Pert,route.params?.transf.data[0].Resultado_Fuzzy]
  }
  return (
    <SafeAreaView style = {css.fundo}>
        <View  style = {css.table}>
              <Table borderStyle = {{borderWidth: 1, borderColor: '#000000'}}>
                        <Row data = {Valores.tableHead} style={css.TableStyle} textStyle={css.TableText}/>
                        <Row data = {Valores.tableBody} style={css.TableStyle} textStyle={css.TableText}/>
              </Table>
            </View>
      <ScrollView>
        <View style={css.container}>
          <View>
          <Text style={css.header}>Line Chart</Text>
      <LineChart 
        data={{labels: date, datasets: [{data: close,strokeWidth: 1,},],}}
        width={Dimensions.get('window').width - 16}
        height={220}
        chartConfig={{
          //backgroundColor: '#2e2e2e',
          backgroundGradientFrom: 'skyblue',
          backgroundGradientTo: 'lightblue',
          decimalPlaces: 1,
          color: (opacity = 255) => `rgba(0, 0, 0, ${opacity})`,
          style: {
            borderRadius: 16,
          },
        }}
        bezier style={{
          marginVertical: 8,
          borderRadius: 16,
        }}
      />
          </View>
          
        </View>
      </ScrollView>

    </SafeAreaView>
  );
};