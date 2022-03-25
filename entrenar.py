from juego import TicTacToe
from agente import agente
from agente2 import agente2
from agente3 import agente3
import math
import time

import numpy as np

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from tensorflow.keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory


def entrenar(n):


    inicio = a.iteracion

    tiempo0 = time.time()

    for i in range(n):


        #partida
        ganador,pasos = juego.start(False, a, a2)

       #actualizar tabla q
        a.actualizar(ganador)
        a2.actualizar(ganador)

        print("-------------------")
        print("partida: " + str(a.iteracion))
        print("-------------------")
        print("|||||||||||||||||||")

        if (i%100 == 0):

            tiempo1 = time.time()

            minutos = (tiempo1 - tiempo0 ) / 60

            print("-------------------")
            print("Tiempo por 100 partidas: " + str(minutos))
            print("-------------------")
            print("|||||||||||||||||||")

            tiempo0 = time.time()

        if (a.iteracion == 700000) or (a.iteracion == 800000) or (a.iteracion == 900000) or (a.iteracion == 1000000) or (a.iteracion == 1250000) or (a.iteracion == 1500000) or (a.iteracion == 1750000) or (a.iteracion == 2000000) or (a.iteracion == n + inicio):
            string = "agente3X"
            string += str(a.iteracion)
            a.guardar(string)
            string = "agente3O"
            string += str(a2.iteracion)
            a2.guardar(string)

def partida(ver, a1, a2):

    if a1 != "":
        nombre = "agente2X" + a1
        a = agente2("X",juego)
        a.cargar(nombre)
    else:
        a = False

    if a2 != "":
        nombre = "agenteO" + a2
        aDos = agente("O",juego)
        aDos.cargar(nombre)
    else:
        aDos = False
    
    ganador,pasos = juego.startPVP(ver, a, aDos)

def partidaEstadistica(n,ver, a1, a2):



    if a1 != "":
        nombre = "agente3X" + a1
        a = agente3("X",juego)
        a.cargar(nombre)
    else:
        a = False

    if a2 != "":
        nombre = "agente3O" + a2
        aDos = agente3("O",juego)
        aDos.cargar(nombre)
    else:
        aDos = False

    ganaX = 0
    ganaO = 0
    empate = 0
    fallo = 0
    
    for i in range(n):

        print("-------------------")
        print("partida: " + str(i+1))
        print("-------------------")

        ganador,pasos = juego.startPVPRand(ver, a, aDos)

        if ganador == "X":
            ganaX +=1
        elif ganador == "O":
            ganaO +=1
        elif ganador == "-":
            empate +=1
        else:
            fallo+=1



        
        

    print("X ha ganado: " + str(ganaX) + "partidas")
    print("O ha ganado: " + str(ganaO) + "partidas")
    print("Empates: " + str(empate) + "partidas")
    print("Fallos: " + str(fallo) + "partidas")


def partidaEstadistica2(n,ver, a1, a2):



    if a1 != "":
        nombre = "agente2X" + a1
        a = agente3("X",juego)
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

        ganador,pasos = juego.startPVPRand(ver, a, aDos)

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
a = agente3("X",juego)
a2 = agente3("O",juego)

a.cargar("agente3X600000")
a2.cargar("agente3O600000")


entrenar(1400000)
#partida(True, "100000" , "80000")
#partidaEstadistica(100,False,"10","600000")
#partidaEstadistica2(10000,False,"10","80000")












