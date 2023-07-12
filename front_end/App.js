import { StyleSheet, Text, View,Button,TouchableOpacity} from 'react-native';
import React,{useState,useEffect} from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import {Home,Preditor1,Preditor2,Teste1,Teste2}  from './views';

export default function App() {
  const Stack = createNativeStackNavigator();
  return (

      <NavigationContainer>
      <Stack.Navigator initialRouteName='Home'>
        <Stack.Screen name="Home"  component={Home} />
        <Stack.Screen name="Teste1"  component={Teste1} />
        <Stack.Screen name="Preditor1"  component={Preditor1} />
        <Stack.Screen name="Teste2"  component={Teste2} />
        <Stack.Screen name="Preditor2"  component={Preditor2} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

