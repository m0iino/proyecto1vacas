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

def procesar_definicion(instr, ts) :
    simbolo = TS.Simbolo(instr.id, TS.TIPO_DATO.NUMERO, 0)      # inicializamos con 0 como valor por defecto
    ts.agregar(simbolo)

def procesar_asignacion(instr, ts) :
    
    print("procesar_asignacion> "+str(instr.expNumerica))
    if isinstance (instr.expNumerica, ExpresionDobleComilla):
        procesar_definicion(instr,ts)    
        val = resolver_expresion_aritmetica(instr.expNumerica, ts)              
        simbolo = TS.Simbolo(instr.id, TS.TIPO_DATO.CARACTER, val)
       
    else:
        procesar_definicion(instr,ts)    
        val = resolver_expresion_aritmetica(instr.expNumerica, ts)              
        simbolo = TS.Simbolo(instr.id, TS.TIPO_DATO.NUMERO, val)
    print("tipo : " + str(simbolo.tipo))
    ts.actualizar(simbolo)

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
    elif isinstance(expCad, ExpresionDobleComilla) :
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
        exp1 = resolver_expresion_aritmetica(expNum.exp1, ts)
        exp2 = resolver_expresion_aritmetica(expNum.exp2, ts)
        if expNum.operador == OPERACION_ARITMETICA.MAS : return exp1 + exp2
        if expNum.operador == OPERACION_ARITMETICA.MENOS : return exp1 - exp2
        if expNum.operador == OPERACION_ARITMETICA.POR : return exp1 * exp2
        if expNum.operador == OPERACION_ARITMETICA.DIVIDIDO : return exp1 / exp2
        if expNum.operador == OPERACION_ARITMETICA.RESIDUO : return exp1 % exp2
    elif isinstance(expNum, ExpresionNegativo) :
        exp = resolver_expresion_aritmetica(expNum.exp, ts)
        return exp * -1
    elif isinstance(expNum, ExpresionNumero) :
        return expNum.val
    elif isinstance(expNum, ExpresionDobleComilla):
        return expNum.val
    elif isinstance(expNum, ExpresionIdentificador) :
        return ts.obtener(expNum.id).valor
    elif isinstance(expNum, ExpresionAbsoluto):
        if ts.obtener(expNum.id).valor < 0: return ts.obtener(expNum.id).valor * -1
        elif ts.obtener(expNum.id).valor > 0: return ts.obtener(expNum.id).valor

def procesar_instrucciones(instrucciones, ts) :
    ## lista de instrucciones recolectadas
    for instr in instrucciones :
        if isinstance(instr, Imprimir) : procesar_imprimir(instr, ts)
        elif isinstance(instr, Definicion_Asignacion) : procesar_asignacion(instr, ts)
        elif isinstance(instr, Definicion_Asignacion_Cadena) : procesar_asignacion_cadena(instr, ts)    
        elif isinstance(instr, Mientras) : procesar_mientras(instr, ts)
        elif isinstance(instr, If) : procesar_if(instr, ts)
        elif isinstance(instr, IfElse) : procesar_if_else(instr, ts)
        else : print('Error: instrucción no válida')

f = open("./entrada.txt", "r")
input = f.read()

instrucciones = g.parse(input)
ts_global = TS.TablaDeSimbolos()

procesar_instrucciones(instrucciones, ts_global)