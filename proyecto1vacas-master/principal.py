# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 00:17:09 2020

@author: moino
"""

import gramatica2 as g
import ts as TS
from expresiones import *
from instrucciones import *

def procesar_imprimir(instr, ts) :
    print('> ', resolver_expresion_aritmetica(instr.cad, ts))

def procesar_borrar(instr,ts):
    #print("procesar borrar: ")
    ts.borrar(instr.cad.id)
    

def procesar_definicion(instr, ts) :
    simbolo = TS.Simbolo(instr.id, TS.TIPO_DATO.NUMERO, 0)      # inicializamos con 0 como valor por defecto
    ts.agregar(simbolo)

def procesar_asignacion(instr, ts) :
    val = resolver_expresion_aritmetica(instr.expNumerica, ts)
    if instr.expNumerica.tipo == 9 :
        #print("error de tipos")
        simbolo = TS.Simbolo(instr.id, instr.expNumerica.tipo, val)
        ts.agregar(simbolo)
    else:
        
        #print("tipo expresion: ",instr.expNumerica.tipo)
        #print("procesar asignacion :",instr.id,"=",val)
        if ts.existe(instr) :
           # print("existe solo se actualiza")
            simbolo = TS.Simbolo(instr.id, instr.expNumerica.tipo, val)
            ts.actualizar(simbolo)
        else:
           # print("no existe se guarda en ts")
            simbolo = TS.Simbolo(instr.id, instr.expNumerica.tipo, val)
            ts.agregar(simbolo)

def procesar_asignacion_arreglo(instr,ts):
    ind = resolver_expresion_aritmetica(instr.expNumerica, ts)
    val = resolver_expresion_aritmetica(instr.expNumerica2, ts)
    #print("procesar asignacion en arreglo",instr.id,"indice:",ind,"valor: ", val)
    if ts.existe(instr) :
           # print("existe solo se actualiza", )
            arreglo = ts.obtener(instr.id).valor
            tipo = ts.obtener(instr.id).tipo
            #print("tamaño arreglo: ",len(arreglo))
            if len(arreglo) == 0:
               # print("tamaño es igual a 0")
              #  print("rango:", range(0,ind))
                for x in range(0,ind+1):
                    
                    if x == ind:
                        
                        arreglo.append(0)                
                        arreglo[ind] = val
                        
                    else:
                        
                        arreglo.append(0)
                        
            elif len(arreglo) <= ind:
               # print("indice mayor al tamaño del arreglo")
                new_tam = ind - len(arreglo) 
               # print("indices agregar: ",new_tam+1)
                for x in range(0,new_tam+1):
                    if x == new_tam:
                        
                        arreglo.append(0)                
                        arreglo[ind] = val
                        
                    else:
                        
                        arreglo.append(0)
            elif len(arreglo) > ind:
                arreglo[ind] = val
                
            simbolo = TS.Simbolo(instr.id, ts.obtener(instr.id).tipo, arreglo)
            ts.actualizar(simbolo)
    else:
          #  print("no existe se guarda en ts")
            arreglo = []
            tipo = TS.TIPO_DATO.ARREGLO
           # print("tamaño arreglo: ",len(arreglo))
            if len(arreglo) == 0:
               # print("tamaño es igual a 0")
                #print("rango::", range(0,ind))
                
                for x in range(0,ind+1):
                    #print("estro trae la x:",x)
                    if x == ind:
                        
                        arreglo.append(0)                
                        arreglo[ind] = val
                        
                    else:
                        
                        arreglo.append(0)
                        
            elif len(arreglo) <= ind:
                #print("indice mayor al tamaño del arreglo")
                new_tam = ind - len(arreglo) 
                #print("indices agregar: ",new_tam+1)
                for x in range(0,new_tam+1):
                    if x == new_tam:
                        
                        arreglo.append(0)                
                        arreglo[ind] = val
                        
                    else:
                        
                        arreglo.append(0)
            elif len(arreglo) > ind:
                arreglo[ind] = val
                
            simbolo = TS.Simbolo(instr.id, TS.TIPO_DATO.ARREGLO, arreglo)
            ts.agregar(simbolo)
            
        
def procesar_asignacion_arreglo_mul(instr, ts):
    #print("lista dimensiones:",instr.expNumerica,"expresion:",instr.expNumerica2)
    if ts.existe(instr):
        #print("existe",instr.id)
        #print("esto trae el diccionario de la ts: ",ts.obtener(instr.id).valor)
        diccionario = ts.obtener(instr.id).valor
        contador = 0
        contador_acc = len(instr.expNumerica)
        aux1 = diccionario
        for dim in range(len(instr.expNumerica)):
           # print("entro al for")
            ind = instr.expNumerica[dim].val
           # print("indice",ind)
            if dim == contador_acc-1:
                #print("es el ultimo")
                aux1[ind] = instr.expNumerica2.val
            else:
               # print("primer else")
                aux = aux1.get(ind)
                #print("auxiliar",aux)
                if aux == None:
                    aux1[ind]={}
                  #  print("if none",aux1)
                    aux1=aux1.get(ind)
                    #print("auxiliar 1:",aux1)
                else:
                    aux1 = aux1.get(ind)
       #print("print diccionario:",diccionario)
        simbolo = TS.Simbolo(instr.id,ts.obtener(instr.id).tipo,diccionario)
        ts.actualizar(simbolo)
    else:
       # print("no existe se guarda en ts",instr.id)
        tipo = TS.TIPO_DATO.ARREGLO
            
        diccionario = {}
        contador = 0
        contador_acc = len(instr.expNumerica)
        aux1 = diccionario
        for dim in range(len(instr.expNumerica)):
           # print("entro al for")
            ind = instr.expNumerica[dim].val
          #  print("indice",ind)
            if dim == contador_acc-1:
              #  print("es el ultimo")
                aux1[ind] = resolver_expresion_aritmetica(instr.expNumerica2,ts)
            else:
               # print("primer else")
                aux = aux1.get(ind)
               # print("auxiliar",aux)
                if aux == None:
                    aux1[ind]={}
                   # print("if none",aux1)
                    aux1=aux1.get(ind)
                   # print("auxiliar 1:",aux1)
                else:
                    aux1 = aux1.get(ind)
        #print("print diccionario:",diccionario)
        simbolo = TS.Simbolo(instr.id, TS.TIPO_DATO.ARREGLO,diccionario)
        ts.agregar(simbolo)
        #print("simbolo",simbolo)
       
            


def procesar_if(instr,instrucciones, ts) :
    #print("procesando if exp1:",instr.expNumerica," exp2:", instr.expNumerica2)
    val = resolver_expresion_aritmetica(instr.expNumerica,ts)
    if val == 1:
        #print("expresion relacional es 1:")
        #print("ahora el goto",instr.expNumerica2)
        procesar_goto(instr.expNumerica2,instrucciones,ts)
        return 1
    else:
        return 0

        
        
def procesar_metodo(instr, ts):
    #print("procesando metodo",instr.id)
    simbolo = TS.Simbolo(instr.id, TS.TIPO_DATO.CADENA, 0)      # inicializamos con 0 como valor por defecto
    ts.agregar(simbolo)

    #ts_local = TS.TablaDeSimbolos(ts.simbolos)
    #procesar_instrucciones(instr.instrucciones, ts_local)
    
def procesar_goto(instr,instrucciones,ts):
    #print("procesando goto",instr.metodo.id)
    #print("instrucciones  globales:",instrucciones)
    instr_restantes = []
    contador = 0
    for instruccion in instrucciones:
        #print("contador instrucciones en goto",contador)
        if isinstance(instruccion, Definicion_Metodo):
            #print("es un metodo:", instruccion.id, " ",instr.metodo.id)
            if instr.metodo.id == instruccion.id:
                instr_restantes = instrucciones[contador+1:]
                #print("instrucciones restantes",instr_restantes)
                procesar_instrucciones_metodo(instr_restantes,instrucciones,ts)
                return
                #print("metodo no existe")
        contador +=1
    
    
def resolver_cadena(expCad, ts) :
    if isinstance(expCad, ExpresionConcatenar) :
        exp1 = resolver_cadena(expCad.exp1, ts)
        exp2 = resolver_cadena(expCad.exp2, ts)
        return exp1 + exp2
    elif isinstance(expCad, ExpresionEntero) :
        return expCad.val
    elif isinstance(expCad, ExpresionCadenaNumerico) :
        return str(resolver_expresion_aritmetica(expCad.exp, ts))
    else :
        print('Error: Expresión cadena no válida')


def resolver_expreision_logica(expLog, ts) :
    exp1 = resolver_expresion_aritmetica(expLog.exp1, ts)
    exp2 = resolver_expresion_aritmetica(expLog.exp2, ts)
    if expLog.operador == OPERACION_LOGICA.MAYOR_QUE : return exp1 > exp2
    if expLog.operador == OPERACION_LOGICA.MENOR_QUE : return exp1 < exp2
    if expLog.operador == OPERACION_LOGICA.IGUAL : return exp1 == exp2
    if expLog.operador == OPERACION_LOGICA.DIFERENTE : return exp1 != exp2

def resolver_expresion_aritmetica(expNum, ts) :
    #print("esta es la expresion ",expNum)
    if isinstance(expNum, ExpresionBinaria) :
        #print("resolver expresion binaria: ")
        exp1 = resolver_expresion_aritmetica(expNum.exp1, ts)
        exp2 = resolver_expresion_aritmetica(expNum.exp2, ts)
        #print("tipo exp1 :",expNum.exp1.tipo)
        #print("tipo exp2 :",expNum.exp2.tipo)
        if expNum.exp1.tipo == expNum.exp2.tipo and expNum.operador == OPERACION_ARITMETICA.MAS:
                        
            expNum.val = exp1 + exp2
            expNum.tipo = expNum.exp1.tipo
            return expNum.val
        
        elif expNum.exp1.tipo == expNum.exp2.tipo and expNum.operador == OPERACION_ARITMETICA.MENOS:
            expNum.val = exp1 - exp2
            expNum.tipo = expNum.exp1.tipo
            return expNum.val 
        elif expNum.exp1.tipo == expNum.exp2.tipo and expNum.operador == OPERACION_ARITMETICA.POR:
            expNum.val = exp1 * exp2
            expNum.tipo = expNum.exp1.tipo
            return expNum.val
        elif expNum.exp1.tipo == expNum.exp2.tipo and expNum.operador == OPERACION_ARITMETICA.DIVIDIDO:
            expNum.val = exp1 / exp2
            expNum.tipo = expNum.exp1.tipo
            return expNum.val
        elif expNum.exp1.tipo == expNum.exp2.tipo and expNum.operador == OPERACION_ARITMETICA.RESIDUO:
            expNum.val = exp1 % exp2
            expNum.tipo = expNum.exp1.tipo
            return expNum.val
        elif (str(expNum.exp1.tipo) == "TIPO_DATO.FLOAT" and str(expNum.exp2.tipo) == "TIPO_DATO.NUMERO" and expNum.operador == OPERACION_ARITMETICA.RESIDUO) or (str(expNum.exp1.tipo) == "TIPO_DATO.NUMERO" and str(expNum.exp2.tipo) == "TIPO_DATO.FLOAT" and expNum.operador == OPERACION_ARITMETICA.RESIDUO):
            expNum.val = exp1 % exp2
            expNum.tipo = expNum.exp1.tipo
            return expNum.val
        elif str(expNum.exp1.tipo) == "TIPO_DATO.NUMERO" and str(expNum.exp2.tipo) == "TIPO_DATO.CADENA":
                expNum.val = 0
                expNum.tipo = 9
                #print("error no se puede sumar numero con cadena")
        elif str(expNum.exp1.tipo) == "TIPO_DATO.CADENA" and str(expNum.exp2.tipo) == "TIPO_DATO.NUMERO":
                expNum.val = 0
                expNum.tipo = 9
                #print("error no se puede sumar cadena con numero")
        #expresion relacionales        
        elif expNum.exp1.tipo == expNum.exp2.tipo and expNum.operador == OPERACION_RELACIONAL.IGUAL:
            if exp1 == exp2 :
                #print("expresion relacional es igual ")
                expNum.val = 1
                expNum.tipo = expNum.exp1.tipo
            else:
                #print("expresion relacional no es igual ")
                expNum.val = 0
                expNum.tipo = expNum.exp1.tipo
            return expNum.val
        elif expNum.exp1.tipo == expNum.exp2.tipo and expNum.operador == OPERACION_RELACIONAL.DIFERENTE:
            if exp1 != exp2 :
                #print("expresion relacional es not igual ")
                expNum.val = 1
                expNum.tipo = expNum.exp1.tipo
            else:
                #print("expresion relacional no es not igual ")
                expNum.val = 0
                expNum.tipo = expNum.exp1.tipo
            return expNum.val
        elif expNum.exp1.tipo == expNum.exp2.tipo and expNum.operador == OPERACION_RELACIONAL.MAYORIGUAL:
            if exp1 >= exp2 :
                #print("expresion relacional es mayor igual ")
                expNum.val = 1
                expNum.tipo = expNum.exp1.tipo
            else:
                #print("expresion relacional no es mayor igual ")
                expNum.val = 0
                expNum.tipo = expNum.exp1.tipo
            return expNum.val
        elif expNum.exp1.tipo == expNum.exp2.tipo and expNum.operador == OPERACION_RELACIONAL.MENORIGUAL:
            if exp1 <= exp2 :
                #print("expresion relacional es menor igual ")
                expNum.val = 1
                expNum.tipo = expNum.exp1.tipo
            else:
                #print("expresion relacional no es menor igual ")
                expNum.val = 0
                expNum.tipo = expNum.exp1.tipo
            return expNum.val
        elif expNum.exp1.tipo == expNum.exp2.tipo and expNum.operador == OPERACION_RELACIONAL.MAYOR_QUE:
            if exp1 > exp2 :
                #print("expresion relacional es mayor ")
                expNum.val = 1
                expNum.tipo = expNum.exp1.tipo
            else:
                #print("expresion relacional no es mayor ")
                expNum.val = 0
                expNum.tipo = expNum.exp1.tipo
            return expNum.val
        elif expNum.exp1.tipo == expNum.exp2.tipo and expNum.operador == OPERACION_RELACIONAL.MENOR_QUE:
            if exp1 < exp2 :
                #print("expresion relacional es menor ")
                expNum.val = 1
                expNum.tipo = expNum.exp1.tipo
            else:
                #print("expresion relacional no es menor ")
                expNum.val = 0
                expNum.tipo = expNum.exp1.tipo
            return expNum.val
        # expresiones logicas
        elif expNum.exp1.tipo == expNum.exp2.tipo and expNum.operador == OPERACION_LOGICA.AND:
            if exp1 * exp2 == 1 :
                #print("expresion logica and verdadera ")
                expNum.val = 1
                expNum.tipo = expNum.exp1.tipo
            else:
                #print("expresion logica and falsa ")
                expNum.val = 0
                expNum.tipo = expNum.exp1.tipo
            return expNum.val
        elif expNum.exp1.tipo == expNum.exp2.tipo and expNum.operador == OPERACION_LOGICA.OR:
            if exp1 + exp2 >= 1 :
                #print("expresion logica or verdadera ")
                expNum.val = 1
                expNum.tipo = expNum.exp1.tipo
            else:
                #print("expresion logica or falsa ")
                expNum.val = 0
                expNum.tipo = expNum.exp1.tipo
            return expNum.val 
        # XOR
        elif expNum.exp1.tipo == expNum.exp2.tipo and expNum.operador == OPERACION_LOGICA.XOR:
            if exp1 + exp2 == 1 :
                #print("expresion logica xor verdadera ")
                expNum.val = 1
                expNum.tipo = expNum.exp1.tipo
            else:
                #print("expresion logica or falsa ")
                expNum.val = 0
                expNum.tipo = expNum.exp1.tipo
            return expNum.val 
        # LOGICAS BITS
        elif expNum.exp1.tipo == expNum.exp2.tipo and expNum.operador == OPERACION_LOGICA.ANDBIT:
            #print("expresion logica and bit")
            expNum.val = exp1 & exp2
            expNum.tipo = expNum.exp1.tipo
            return expNum.val
        elif expNum.exp1.tipo == expNum.exp2.tipo and expNum.operador == OPERACION_LOGICA.ORBIT:
            #print("expresion logica OR bit")
            expNum.val = exp1 | exp2
            expNum.tipo = expNum.exp1.tipo
            return expNum.val
        elif expNum.exp1.tipo == expNum.exp2.tipo and expNum.operador == OPERACION_LOGICA.XORBIT:
            #print("expresion logica XOR bit")
            expNum.val = exp1 ^ exp2
            expNum.tipo = expNum.exp1.tipo
            return expNum.val
        elif expNum.exp1.tipo == expNum.exp2.tipo and expNum.operador == OPERACION_LOGICA.MENORBIT:
            #print("expresion logica << bit")
            expNum.val = exp1 << exp2
            expNum.tipo = expNum.exp1.tipo
            return expNum.val
        elif expNum.exp1.tipo == expNum.exp2.tipo and expNum.operador == OPERACION_LOGICA.MAYORBIT:
            #print("expresion logica >> bit")
            expNum.val = exp1 >> exp2
            expNum.tipo = expNum.exp1.tipo
            return expNum.val
    elif isinstance(expNum, ExpresionNegativo) :
        expNum.val = resolver_expresion_aritmetica(expNum.val, ts)
        expNum.tipo = expNum.tipo
        return expNum.val * -1
    elif isinstance(expNum, ExpresionEntero) :
        #print("expresion entero:", expNum.tipo)
        expNum.val = expNum.val
        expNum.tipo = expNum.tipo
        return expNum.val
    elif isinstance(expNum, ExpresionIdentificador) :
        #print("resolver expresion temporal: ",ts.obtener(expNum.id).valor)
        expNum.val = ts.obtener(expNum.id).valor
        expNum.tipo = ts.obtener(expNum.id).tipo
        return expNum.val
    elif isinstance(expNum, ExpresionAbsoluto):
        #print("resolver expresion absoluto: ",ts.obtener(expNum.id.id).valor)
        expNum.val = ts.obtener(expNum.id.id).valor
        expNum.tipo = ts.obtener(expNum.id.id).tipo
        if expNum.val < 0 :
            return expNum.val * -1
        else:
            return expNum.val
    elif isinstance(expNum, ExpresionConversionInt):
        #print("resolver expresion conversion int: ", ts.obtener(expNum.id.id).tipo)
        if isinstance(ts.obtener(expNum.id.id).valor, float):
            #print("es float")
            expNum.val = int(ts.obtener(expNum.id.id).valor)
            expNum.tipo = TS.TIPO_DATO.NUMERO
        elif ts.obtener(expNum.id.id).tipo == TS.TIPO_DATO.CARACTER:
            #print("es char: ",ts.obtener(expNum.id.id).tipo)
            expNum.val = ord(ts.obtener(expNum.id.id).valor)
            expNum.tipo = TS.TIPO_DATO.NUMERO#ts.obtener(expNum.id.id).tipo
        elif ts.obtener(expNum.id.id).tipo == TS.TIPO_DATO.ARREGLO:
            #print("es ARREGLO: ",ts.obtener(expNum.id.id).tipo)
            expNum.val = ord(ts.obtener(expNum.id.id).valor[0][0])
            expNum.tipo = TS.TIPO_DATO.NUMERO#ts.obtener(expNum.id.id).tipo
        elif isinstance(ts.obtener(expNum.id.id).valor, str):
            #print("es cadena: ",ts.obtener(expNum.id.id).tipo)
            expNum.val = ord(ts.obtener(expNum.id.id).valor[0])
            expNum.tipo = TS.TIPO_DATO.NUMERO#ts.obtener(expNum.id.id).tipo
        
        return expNum.val
    elif isinstance(expNum, ExpresionConversionFloat):
        #print("resolver expresion conversion float: ", ts.obtener(expNum.id.id).valor)
        if isinstance(ts.obtener(expNum.id.id).valor, int):
            #print("es int")
            expNum.val = float(ts.obtener(expNum.id.id).valor)
            expNum.tipo = TS.TIPO_DATO.FLOAT#ts.obtener(expNum.id.id).tipo
        elif ts.obtener(expNum.id.id).tipo == TS.TIPO_DATO.CARACTER:
            #print("es char: ",ts.obtener(expNum.id.id).tipo)
            expNum.val = float(ord(ts.obtener(expNum.id.id).valor))
            expNum.tipo = TS.TIPO_DATO.FLOAT#ts.obtener(expNum.id.id).tipo
        elif ts.obtener(expNum.id.id).tipo == TS.TIPO_DATO.ARREGLO:
            #print("es char: ",ts.obtener(expNum.id.id).tipo)
            expNum.val = float(ord(ts.obtener(expNum.id.id).valor[0][0]))
            expNum.tipo = TS.TIPO_DATO.FLOAT#ts.obtener(expNum.id.id).tipo
        elif isinstance(ts.obtener(expNum.id.id).valor, str):
            #print("es cadena: ",ts.obtener(expNum.id.id).tipo)
            expNum.val = float(ord(ts.obtener(expNum.id.id).valor[0]))
            expNum.tipo = TS.TIPO_DATO.FLOAT#ts.obtener(expNum.id.id).tipo
        return expNum.val
    elif isinstance(expNum, ExpresionConversionChar):
        print("resolver expresion conversion char: ", ts.obtener(expNum.id.id).valor)
        if (isinstance(ts.obtener(expNum.id.id).valor, int) and ts.obtener(expNum.id.id).valor <= 255 ):
            #print("es int y menor a 255")
            expNum.val = chr(ts.obtener(expNum.id.id).valor)
            expNum.tipo = TS.TIPO_DATO.CARACTER#ts.obtener(expNum.id.id).tipo
        elif (isinstance(ts.obtener(expNum.id.id).valor, int) and ts.obtener(expNum.id.id).valor > 255 ):
            #print("es int y mayor a 255")
            expNum.val = chr(ts.obtener(expNum.id.id).valor % 256)
            expNum.tipo = TS.TIPO_DATO.CARACTER#ts.obtener(expNum.id.id).tipo
        elif isinstance(ts.obtener(expNum.id.id).valor, float):
            print("es float")
            expNum.val = int(ts.obtener(expNum.id.id).valor)
            print(expNum.val)
            if expNum.val <= 255:
                expNum.val = chr(expNum.val)
                expNum.tipo = TS.TIPO_DATO.CARACTER#ts.obtener(expNum.id.id).tipo
            else:
                expNum.val = chr(ts.obtener(expNum.id.id).valor % 256)
                expNum.tipo = TS.TIPO_DATO.CARACTER#ts.obtener(expNum.id.id).tipo               
                                
        elif isinstance(ts.obtener(expNum.id.id).valor, str):
            #print("es cadena: ",ts.obtener(expNum.id.id).tipo)
            expNum.val = ts.obtener(expNum.id.id).valor[0]
            expNum.tipo = TS.TIPO_DATO.CARACTER#ts.obtener(expNum.id.id).tipo
            
        elif ts.obtener(expNum.id.id).tipo == TS.TIPO_DATO.ARREGLO:
            #print("es char: ",ts.obtener(expNum.id.id).tipo)
            expNum.val = ts.obtener(expNum.id.id).valor[0][0]
            expNum.tipo = TS.TIPO_DATO.CARACTER#ts.obtener(expNum.id.id).tipo
        return expNum.val 
    elif isinstance(expNum, ExpresionNot):
        #print("resolver expresion not: ", ts.obtener(expNum.id.id).valor)
        if ts.obtener(expNum.id.id).valor == 1:
            expNum.val = 0
            expNum.tipo = ts.obtener(expNum.id.id).tipo
        else:
            expNum.val = 1
            expNum.tipo = ts.obtener(expNum.id.id).tipo
        return expNum.val
    elif isinstance(expNum, ExpresionNotBit):
        #print("resolver expresion not bit: ", ts.obtener(expNum.id.id).valor)
        expNum.val = ~ ts.obtener(expNum.id.id).valor
        expNum.tipo = ts.obtener(expNum.id.id).tipo
        return expNum.val
    elif isinstance(expNum, ExpresionArreglo):
        #print("expresion arreglo:", expNum.tipo)
        expNum.val = []
        expNum.tipo = expNum.tipo
        return expNum.val
    elif isinstance(expNum, AccesoArreglo):
        #print("expresion acceso arreglo:", expNum.expNumerica)
        aux = ts.obtener(expNum.id).valor
        aux1 = aux
        cantidad_acc = len(expNum.expNumerica)
        #print("aux",aux)
        for i in range(len(expNum.expNumerica)):
            if isinstance(expNum.expNumerica[i],ExpresionIdentificador):
                #print("es exp ident",ts.obtener(expNum.expNumerica[i].id).valor)
                indice = ts.obtener(expNum.expNumerica[i].id).valor
            else:
                
                indice = expNum.expNumerica[i].val
            #print("indice",indice)
            if i == cantidad_acc -1:
                aux1 = aux1.get(indice)
                #print("ultimo",aux1)
            else:
                aux = aux1.get(indice)
                if aux ==None:
                    print("indice no existe")
                else:
                    aux1 = aux1.get(indice)
        #print("esto trae el aux1",aux1)
        expNum.val = aux1
        return expNum.val



def procesar_instrucciones_main( instrucciones, ts):
    #print("procesar main")    
    if instrucciones[0].id == "main":
        nuevo_arr = instrucciones[1:]
        for instr in nuevo_arr :
            #print("instruccion:", instr)            
            if isinstance(instr, Imprimir) : procesar_imprimir(instr, ts)
            elif isinstance(instr, Definicion_Asignacion) : procesar_asignacion(instr, ts)    
            elif isinstance(instr, Definicion_Asignacion_Arreglo) : procesar_asignacion_arreglo(instr, ts)    
            elif isinstance(instr, Definicion_Asignacion_Arreglo_Multiple) : procesar_asignacion_arreglo_mul(instr, ts)    
            elif isinstance(instr, If) : 
                if procesar_if(instr,instrucciones, ts) == 1:
                    return
            elif isinstance(instr, Borrar) : procesar_borrar(instr,ts)
            #elif isinstance(instr, Definicion_Metodo) : break
            elif isinstance(instr, Goto) : 
                procesar_goto(instr,instrucciones,ts) 
                return
            elif isinstance(instr, Exit) : 
                #print("exit")            
                return             
            else : print('Error: instruccion no valida en main')
    else:
        print("metodo principal no esta al inicio o no existe")
             
def procesar_instrucciones_metodo(instrucciones,instr_globales, ts) :
    ## lista de instrucciones recolectadas
    #print("procesar metodo")
    for instr in instrucciones :
        
            
        if isinstance(instr, Imprimir) : procesar_imprimir(instr, ts)
        elif isinstance(instr, Definicion_Asignacion) : procesar_asignacion(instr, ts)    
        elif isinstance(instr, Definicion_Asignacion_Arreglo) : procesar_asignacion_arreglo(instr, ts)
        elif isinstance(instr, If) : 
            if procesar_if(instr,instr_globales, ts) == 1:
                return
            
        elif isinstance(instr, Borrar) : procesar_borrar(instr,ts)
        #elif isinstance(instr, Definicion_Metodo) : break
        elif isinstance(instr, Goto) : 
            #print("entro al goto")
            procesar_goto(instr,instr_globales,ts)
            return
        elif isinstance(instr, Exit) : 
            #print("exit")            
            break                      
        else : print('Error: instruccion no valida')
        

f = open("./entrada.txt", "r")
input = f.read()

instrucciones = g.parse(input)
#print("primer print:",instrucciones)
ts_global = TS.TablaDeSimbolos()

procesar_instrucciones_main(instrucciones, ts_global)