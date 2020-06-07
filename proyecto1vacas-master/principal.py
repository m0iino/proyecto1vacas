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
    print('> ', resolver_cadena(instr.cad, ts))

def procesar_borrar(instr,ts):
    print("procesar borrar: ")
    ts.borrar(instr.cad.id)

def procesar_definicion(instr, ts) :
    simbolo = TS.Simbolo(instr.id, TS.TIPO_DATO.NUMERO, 0)      # inicializamos con 0 como valor por defecto
    ts.agregar(simbolo)

def procesar_asignacion(instr, ts) :
    val = resolver_expresion_aritmetica(instr.expNumerica, ts)
    if instr.expNumerica.tipo == 9 :
        print("error de tipos")
        simbolo = TS.Simbolo(instr.id, instr.expNumerica.tipo, val)
        ts.agregar(simbolo)
    else:
        
        print("tipo expresion: ",instr.expNumerica.tipo)
        print("procesar asignacion :",instr.id,"=",val)
        if ts.existe(instr) :
            print("existe solo se actualiza")
            simbolo = TS.Simbolo(instr.id, instr.expNumerica.tipo, val)
            ts.actualizar(simbolo)
        else:
            print("no existe se guarda en ts")
            simbolo = TS.Simbolo(instr.id, instr.expNumerica.tipo, val)
            ts.agregar(simbolo)
        


def procesar_mientras(instr, ts) :
    while resolver_expreision_logica(instr.expLogica, ts) :
        ts_local = TS.TablaDeSimbolos(ts.simbolos)
        procesar_instrucciones(instr.instrucciones, ts_local)

def procesar_if(instr, ts) :
    val = resolver_expreision_logica(instr.expLogica, ts)
    if val :
        ts_local = TS.TablaDeSimbolos(ts.simbolos)
        procesar_instrucciones(instr.instrucciones, ts_local)

def procesar_if_else(instr, ts) :
    val = resolver_expreision_logica(instr.expLogica, ts)
    if val :
        ts_local = TS.TablaDeSimbolos(ts.simbolos)
        procesar_instrucciones(instr.instrIfVerdadero, ts_local)
    else :
        ts_local = TS.TablaDeSimbolos(ts.simbolos)
        procesar_instrucciones(instr.instrIfFalso, ts_local)

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
    if isinstance(expNum, ExpresionBinaria) :
        print("resolver expresion binaria: ")
        exp1 = resolver_expresion_aritmetica(expNum.exp1, ts)
        exp2 = resolver_expresion_aritmetica(expNum.exp2, ts)
        print("tipo exp1 :",expNum.exp1.tipo)
        print("tipo exp2 :",expNum.exp2.tipo)
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
                print("error no se puede sumar numero con cadena")
        elif str(expNum.exp1.tipo) == "TIPO_DATO.CADENA" and str(expNum.exp2.tipo) == "TIPO_DATO.NUMERO":
                expNum.val = 0
                expNum.tipo = 9
                print("error no se puede sumar cadena con numero")
        #expresion relacionales        
        elif expNum.exp1.tipo == expNum.exp2.tipo and expNum.operador == OPERACION_RELACIONAL.IGUAL:
            if exp1 == exp2 :
                print("expresion relacional es igual ")
                expNum.val = 1
                expNum.tipo = expNum.exp1.tipo
            else:
                print("expresion relacional no es igual ")
                expNum.val = 0
                expNum.tipo = expNum.exp1.tipo
            return expNum.val
        elif expNum.exp1.tipo == expNum.exp2.tipo and expNum.operador == OPERACION_RELACIONAL.DIFERENTE:
            if exp1 != exp2 :
                print("expresion relacional es not igual ")
                expNum.val = 1
                expNum.tipo = expNum.exp1.tipo
            else:
                print("expresion relacional no es not igual ")
                expNum.val = 0
                expNum.tipo = expNum.exp1.tipo
            return expNum.val
        elif expNum.exp1.tipo == expNum.exp2.tipo and expNum.operador == OPERACION_RELACIONAL.MAYORIGUAL:
            if exp1 >= exp2 :
                print("expresion relacional es mayor igual ")
                expNum.val = 1
                expNum.tipo = expNum.exp1.tipo
            else:
                print("expresion relacional no es mayor igual ")
                expNum.val = 0
                expNum.tipo = expNum.exp1.tipo
            return expNum.val
        elif expNum.exp1.tipo == expNum.exp2.tipo and expNum.operador == OPERACION_RELACIONAL.MENORIGUAL:
            if exp1 <= exp2 :
                print("expresion relacional es menor igual ")
                expNum.val = 1
                expNum.tipo = expNum.exp1.tipo
            else:
                print("expresion relacional no es menor igual ")
                expNum.val = 0
                expNum.tipo = expNum.exp1.tipo
            return expNum.val
        elif expNum.exp1.tipo == expNum.exp2.tipo and expNum.operador == OPERACION_RELACIONAL.MAYOR_QUE:
            if exp1 > exp2 :
                print("expresion relacional es mayor ")
                expNum.val = 1
                expNum.tipo = expNum.exp1.tipo
            else:
                print("expresion relacional no es mayor ")
                expNum.val = 0
                expNum.tipo = expNum.exp1.tipo
            return expNum.val
        elif expNum.exp1.tipo == expNum.exp2.tipo and expNum.operador == OPERACION_RELACIONAL.MENOR_QUE:
            if exp1 < exp2 :
                print("expresion relacional es menor ")
                expNum.val = 1
                expNum.tipo = expNum.exp1.tipo
            else:
                print("expresion relacional no es menor ")
                expNum.val = 0
                expNum.tipo = expNum.exp1.tipo
            return expNum.val
        # expresiones logicas
        elif expNum.exp1.tipo == expNum.exp2.tipo and expNum.operador == OPERACION_LOGICA.AND:
            if exp1 * exp2 == 1 :
                print("expresion logica and verdadera ")
                expNum.val = 1
                expNum.tipo = expNum.exp1.tipo
            else:
                print("expresion logica and falsa ")
                expNum.val = 0
                expNum.tipo = expNum.exp1.tipo
            return expNum.val
        elif expNum.exp1.tipo == expNum.exp2.tipo and expNum.operador == OPERACION_LOGICA.OR:
            if exp1 + exp2 >= 1 :
                print("expresion logica or verdadera ")
                expNum.val = 1
                expNum.tipo = expNum.exp1.tipo
            else:
                print("expresion logica or falsa ")
                expNum.val = 0
                expNum.tipo = expNum.exp1.tipo
            return expNum.val 
        # falta hacer el xor y las logicas por bit   
    elif isinstance(expNum, ExpresionNegativo) :
        expNum.val = resolver_expresion_aritmetica(expNum.val, ts)
        expNum.tipo = expNum.tipo
        return expNum.val * -1
    elif isinstance(expNum, ExpresionEntero) :
        print("expresion entero:", expNum.tipo)
        expNum.val = expNum.val
        expNum.tipo = expNum.tipo
        return expNum.val
    elif isinstance(expNum, ExpresionIdentificador) :
        print("resolver expresion temporal: ",ts.obtener(expNum.id).valor)
        expNum.val = ts.obtener(expNum.id).valor
        expNum.tipo = ts.obtener(expNum.id).tipo
        return expNum.val
    elif isinstance(expNum, ExpresionAbsoluto):
        print("resolver expresion absoluto: ",ts.obtener(expNum.id.id).valor)
        expNum.val = ts.obtener(expNum.id.id).valor
        expNum.tipo = ts.obtener(expNum.id.id).tipo
        if expNum.val < 0 :
            return expNum.val * -1
        else:
            return expNum.val
    elif isinstance(expNum, ExpresionConversionInt):
        print("resolver expresion conversion int: ", ts.obtener(expNum.id.id).valor)
        if isinstance(ts.obtener(expNum.id.id).valor, float):
            print("es float")
            expNum.val = int(ts.obtener(expNum.id.id).valor)
            expNum.tipo = ts.obtener(expNum.id.id).tipo
        elif ts.obtener(expNum.id.id).tipo == TS.TIPO_DATO.CARACTER:
            print("es char: ",ts.obtener(expNum.id.id).tipo)
            expNum.val = ord(ts.obtener(expNum.id.id).valor)
            expNum.tipo = ts.obtener(expNum.id.id).tipo
        elif isinstance(ts.obtener(expNum.id.id).valor, str):
            print("es cadena: ",ts.obtener(expNum.id.id).tipo)
            expNum.val = ord(ts.obtener(expNum.id.id).valor[0])
            expNum.tipo = ts.obtener(expNum.id.id).tipo
        return expNum.val
    elif isinstance(expNum, ExpresionConversionFloat):
        print("resolver expresion conversion float: ", ts.obtener(expNum.id.id).valor)
        if isinstance(ts.obtener(expNum.id.id).valor, int):
            print("es int")
            expNum.val = float(ts.obtener(expNum.id.id).valor)
            expNum.tipo = ts.obtener(expNum.id.id).tipo
        elif ts.obtener(expNum.id.id).tipo == TS.TIPO_DATO.CARACTER:
            print("es char: ",ts.obtener(expNum.id.id).tipo)
            expNum.val = float(ord(ts.obtener(expNum.id.id).valor))
            expNum.tipo = ts.obtener(expNum.id.id).tipo
        elif isinstance(ts.obtener(expNum.id.id).valor, str):
            print("es cadena: ",ts.obtener(expNum.id.id).tipo)
            expNum.val = float(ord(ts.obtener(expNum.id.id).valor[0]))
            expNum.tipo = ts.obtener(expNum.id.id).tipo
        return expNum.val
    elif isinstance(expNum, ExpresionConversionChar):
        print("resolver expresion conversion char: ", ts.obtener(expNum.id.id).valor)
        if (isinstance(ts.obtener(expNum.id.id).valor, int) and ts.obtener(expNum.id.id).valor <= 255 ):
            print("es int y menor a 255")
            expNum.val = chr(ts.obtener(expNum.id.id).valor)
            expNum.tipo = ts.obtener(expNum.id.id).tipo
        else:
            print("es int y mayor a 255")
            expNum.val = chr(ts.obtener(expNum.id.id).valor % 256)
            expNum.tipo = ts.obtener(expNum.id.id).tipo
        return expNum.val 
    elif isinstance(expNum, ExpresionNot):
        print("resolver expresion not: ", ts.obtener(expNum.id.id).valor)
        if ts.obtener(expNum.id.id).valor == 1:
            expNum.val = 0
            expNum.tipo = ts.obtener(expNum.id.id).tipo
        else:
            expNum.val = 1
            expNum.tipo = ts.obtener(expNum.id.id).tipo
        return expNum.val

def procesar_instrucciones(instrucciones, ts) :
    ## lista de instrucciones recolectadas
    for instr in instrucciones :
        if isinstance(instr, Imprimir) : procesar_imprimir(instr, ts)
        elif isinstance(instr, Definicion_Asignacion) : procesar_asignacion(instr, ts)    
        elif isinstance(instr, Mientras) : procesar_mientras(instr, ts)
        elif isinstance(instr, If) : procesar_if(instr, ts)
        elif isinstance(instr, IfElse) : procesar_if_else(instr, ts)
        elif isinstance(instr, Borrar) : procesar_borrar(instr,ts)
        else : print('Error: instruccion no valida')

f = open("./entrada.txt", "r")
input = f.read()

instrucciones = g.parse(input)
ts_global = TS.TablaDeSimbolos()

procesar_instrucciones(instrucciones, ts_global)