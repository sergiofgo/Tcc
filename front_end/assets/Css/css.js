import { StyleSheet } from "react-native";
import React from "react";
const css = StyleSheet.create({
    titulo_home:{
      color:'#ffffff',
      fontSize: 40,
      textAlign : 'center'
    },
    titulo_1:{
      color:'#ffffff',
      fontSize: 35,
      textAlign : 'center',
      marginTop: -150,
    },
    titulo_2:{
      color:'#ffffff',
      fontSize: 35,
      textAlign : 'center',
    },
    fundo: {
      flex: 1,
      backgroundColor: '#2e2e2e',
      justifyContent: 'center',
      alignItems: 'center'
    },
    container: {
      flex: 1,
      //backgroundColor: 'white',
      justifyContent: 'center',
      alignItems: 'center',
      textAlign: 'center',
      padding: 10,
    },
    header: {
      textAlign: 'center',
      color:'#ffffff',
      fontSize: 18,
      padding: 16,
      marginTop: 16,
    },
    pick1:{
      height: 50, 
      width: 180,
      marginRight: 150,
    },
    pick2:{
      height: 50, 
      width: 400,
      marginRight: 50 
    },
    table:{
      flex:1, 
      padding:10
    },
    container1:{
      flex:1,
      //backgroundColor: '  ',
      flexDirection: 'row',
      justifyContent: 'center',
      alignItems: 'center'
    },
    button1:{
      backgroundColor:'#084d6e',
      marginRight: 50,
      padding: 30,
      color: '#ffffff'
    },
    button2:{
      backgroundColor:'#084d6e',
      marginLeft: 50,
      padding: 30,
      color: '#ffffff'
    },
    dark_bg:{
      backgroundColor:'#333'
    },
    login__msg:(val='none')=>({
      fontWeight: "bold",
      fontSize: 22,
      color:'red',
      marginTop:10,
      marginBottom:15,
      display:val,
    }),
    login_form:{
      width:'80%',
      marginTop: 10,
      flexDirection: 'row',
      justifyContent: 'center',
      alignItems: 'center'
    },
    login_input:{
      backgroundColor: '#fff',
      height:47,
      width:170,
      fontSize: 19,
      padding: 7,
      marginLeft: 50,
    },
    login_button:{
      padding: 12,
      backgroundColor:'#f58634',
      alignSelf: 'center',
      borderRadius: 5,
      marginTop: 100,
    },
    login_buttonText:{
      fontWeight: 'bold',
      fontSize: 22,
      color: '#333',
    },
    TableStyle: { 
      height: 60,
      width: 1200,
      alignContent: "center",
      backgroundColor: '#ffffff'
    },
    TableText: { 
      textAlign : 'center'
    },
  });
  export {css};
