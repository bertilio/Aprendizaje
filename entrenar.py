from juego import TicTacToe
from agente import agente
import math



def entrenar(n):

    inicio = a.iteracion 

    for i in range(n):

        #partida
        ganador,pasos = juego.start(False, a, a2)

       #actualizar tabla q
        a.actualizar(pasos,ganador)
        a2.actualizar(pasos,ganador)


        print("-------------------")
        print("partida: " + str(a.iteracion))
        print("-------------------")
        print("estados: " + str(len(a.estados)))
        print("-------------------")
        print("|||||||||||||||||||")

        if (a.iteracion == 1250000) or (a.iteracion == 1500000) or (a.iteracion == 1750000) or (a.iteracion == inicio + n + 1):
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
    
    ganador,pasos = juego.startPVP(ver, a, aDos)

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

        ganador,pasos = juego.startQvsRand(ver, a, aDos)

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



a.cargar("agenteX1000000")
a2.cargar("agenteO1000000")

entrenar(2)
#partida(True, "" , "500000")
#partidaEstadistica(100,False,"10","1000000")


