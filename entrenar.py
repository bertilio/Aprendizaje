from itertools import groupby, chain
from juego import TicTacToe
from agente import agente
import math
import random
import time
import os



def entrenar(n):

    for i in range(n):

        #partida
        ganador,pasos = juego.start(False, a, a2)

       #actualizar tabla q
        a.actualizar(pasos,ganador)
        a2.actualizar(pasos,ganador)

        if(a.iteracion%10000 == 0):
            
            print("-------------------")
            print("partida: " + str(a.iteracion))
            print("-------------------")
            print("estados: " + str(len(a.estados)))
            print("-------------------")
            print("|||||||||||||||||||")


        if (a.iteracion == 10) or (a.iteracion == 100) or (a.iteracion == 1000) or (a.iteracion == 10000) or (a.iteracion == 50000) or (a.iteracion == 500000) or (a.iteracion == n):
            string = "agenteX"
            string += str(a.iteracion)
            a.guardar(string)
            string = "agenteO"
            string += str(a2.iteracion)
            a2.guardar(string)

def partida(ver, a1, a2):

    if a1 != "":
        nombre = "agenteX" + a1
        a = agente("X",juego)
        a.cargar(nombre)
    else:
        a = False

    if a2 != "":
        nombre = "agenteO" + a2
        aDos = agente("O",juego)
        aDos.cargar(nombre)
    else:
        aDos = False
    
    ganador,pasos = juego.start(ver, a, aDos)

def partidaEstadistica(n,ver, a1, a2):



    if a1 != "":
        nombre = "agenteX" + a1
        a = agente("X",juego)
        a.cargar(nombre)
    else:
        a = False

    if a2 != "":
        nombre = "agenteO" + a2
        aDos = agente("O",juego)
        aDos.cargar(nombre)
    else:
        aDos = False

    ganaX = 0
    ganaO = 0
    empate = 0
    
    for i in range(n):

        print("-------------------")
        print("partida: " + str(i+1))
        print("-------------------")

        ganador,pasos = juego.start(ver, a, aDos)

        if ganador == "X":
            ganaX +=1
        elif ganador == "O":
            ganaO +=1
        else:
            empate +=1

    print("X ha ganado: " + str(ganaX) + "partidas")
    print("O ha ganado: " + str(ganaO) + "partidas")
    print("Empates: " + str(empate) + "partidas")


juego = TicTacToe()
a = agente("X",juego)
a2 = agente("O",juego)

#a.cargar("agenteX100000")
#a2.cargar("agenteO100000")

entrenar(1000000)
#partida(True, "100000", "")
#partidaEstadistica(1000,False,"100000","10")

