import React,{useState,useEffect} from 'react';
import {View,Text,TouchableOpacity,Button,SafeAreaView,KeyboardAvoidingView,Picker,TextInput,Platform,ScrollView} from 'react-native';
import {css} from '../assets/Css/css';
import { TextInputMask } from 'react-native-masked-text';
import config from "../config/config.json";

export default function Teste1 (props ) {
    const[bolsas,setBolsas] = useState("^BVSP" )
    const[acao,setAcao] = useState('ABCB4.SA')
    const[date,setDate] = useState('01/01/2023')
    const[transf,setTransf] = useState(null)
    const [vetAcoes,setVetAcoes] = useState(null);
    useEffect(()=>{bolsa();},[bolsas])
    useEffect(()=>{resultado2();},[acao])
    async function bolsa(){
        let reqs = await fetch(config.urlRootPhython +'bolsas/', {method:'POST', headers: {'Accept':'application/json','Content-Type':'application/json'},body: JSON.stringify({exchange: bolsas})});
        let resp = await reqs.json();
        setVetAcoes(resp.data);
    }
    async function resultado2(){
        let reqs = await fetch(config.urlRootPhython +'resultado2/', {method:'POST', headers: {'Accept':'application/json','Content-Type':'application/json'},body: JSON.stringify({stock: acao, exchange: bolsas, data: date})});
        let resp = await reqs.json();
        setTransf(resp);
    }
    return (
        <SafeAreaView style = {css.fundo}>
          <KeyboardAvoidingView behavior = {Platform.OS == 'ios'?'padding':'height'} style = {css.fundo}>
            <View><Text style = {css.titulo_1}>Teste com o Sistema de Predição</Text></View>
            <View style = {css.login_form}>
                <Picker  style={css.pick1} selectedValue = {bolsas} onValueChange ={(item,itemIndex) => {setBolsas(item)}}>   
                    <Picker.Item label="B3" value="^BVSP" />
                    <Picker.Item label="Bolsa de Nova York" value="^NYA" />
                    <Picker.Item label="NASDAQ" value="^IXIC" />
                </Picker>
                <Picker  style={css.pick2} selectedValue = {acao} onValueChange ={(item,itemIndex) =>{setAcao(item)}}>
                    {vetAcoes && (vetAcoes.map((item,index)=><Picker.Item label = {item.full_name} value = {item.symbol}/>))}
                </Picker>
                <TextInputMask type={'datetime'} style = {css.login_input} options={{format: 'DD/MM/YYYY'}}  placeholder = 'DD/MM/YYYY' value={date} onChangeText={(text) => {setDate(text)}}/>
            </View>
            <View>
                <TouchableOpacity title = "Teste2" onPress={()=>props.navigation.navigate('Teste2',{transf})} style = {css.login_button}><Text style = {css.login_buttonText}>Teste2</Text> </TouchableOpacity>
            </View>
            </KeyboardAvoidingView>
        </SafeAreaView>
    );   
}
