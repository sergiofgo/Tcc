import React from 'react';
import {View,Text,TouchableOpacity,Button,SafeAreaView} from 'react-native';
import {css} from '../assets/Css/css';

export default function Home (props) {
   
    return (
        <SafeAreaView style = {css.fundo}>
            <View>
                <Text style = {css.titulo_home}>Sistema de Predição de Ações</Text>
            </View>
            <View  style = {css.container1}>
                <TouchableOpacity title = "Ir para Preditor1" onPress={()=>props.navigation.navigate('Preditor1')} style = {css.button1}>Preditor</TouchableOpacity>
                <TouchableOpacity title = "Ir para Teste1" onPress={()=>props.navigation.navigate('Teste1')} style = {css.button2}>Teste</TouchableOpacity>
            </View>
        </SafeAreaView>
    );
    
}
