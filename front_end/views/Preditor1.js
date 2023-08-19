import React,{useState,useEffect} from 'react';
import {View,Text,TouchableOpacity,Button,SafeAreaView,KeyboardAvoidingView,Picker,TextInput,Platform,ScrollView} from 'react-native';
import {css} from '../assets/Css/css';
import { TextInputMask } from 'react-native-masked-text';
import config from "../config/config.json";

export default function Preditor1 (props ) {
    const[bolsas,setBolsas] = useState("^BVSP" )
    const[acao,setAcao] = useState('ABCB4.SA')
    const[transf,setTransf] = useState(null)
    const [vetAcoes,setVetAcoes] = useState(null);
    useEffect(()=>{bolsa();},[bolsas]);
    useEffect(()=>{resultado1();},[acao])
    async function bolsa(){
        let reqs = await fetch(config.urlRootPhython +'bolsas/', {method:'POST', headers: {'Accept':'application/json','Content-Type':'application/json'},body: JSON.stringify({exchange: bolsas})});
        let resp = await reqs.json();
        setVetAcoes(resp.data);
    }
    async function resultado1(){
        let reqs = await fetch(config.urlRootPhython +'resultado1/', {method:'POST', headers: {'Accept':'application/json','Content-Type':'application/json'},body: JSON.stringify({stock: acao, exchange: bolsas})});
        let resp = await reqs.json();
        setTransf(resp);
    }
    return (
        <SafeAreaView style = {css.fundo}>
          <KeyboardAvoidingView behavior = {Platform.OS == 'ios'?'padding':'height'} style = {css.fundo}>
            <View><Text style = {css.titulo_1}>Preditor de Ações</Text></View>
            <View style = {css.login_form}>
                <Picker  style={css.pick1} selectedValue = {bolsas} onValueChange ={(item,itemIndex) => {setBolsas(item)}}>   
                    <Picker.Item label="B3" value="^BVSP" />
                    <Picker.Item label="Bolsa de Nova York" value="^NYA" />
                    <Picker.Item label="NASDAQ" value="^IXIC" />
                </Picker>
                <Picker  style={css.pick2} selectedValue = {acao} onValueChange ={(item,itemIndex) =>{setAcao(item)}}>
                    { vetAcoes && (vetAcoes.map((item,index)=><Picker.Item label = {item.full_name} value = {item.symbol}/>))}
                </Picker>
            </View>
            <View>
                <TouchableOpacity title = "Preditor1"  onPress={()=>{props.navigation.navigate('Preditor2',{transf})}} style = {css.login_button}><Text style = {css.login_buttonText}>Preditor2</Text> </TouchableOpacity>
            </View>
            </KeyboardAvoidingView>
        </SafeAreaView>
    );   
}
