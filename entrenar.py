
from juego import partida2, Game , partida3 , partida4 , partidaVer
from itertools import groupby, chain
from agente import agente
from red import red
import math
import random
import time
import os

a = agente('R');
a2 = agente('Y');

def iniciar2agentes():
    a.color='R'
    a2.color ='Y'

def entrenar_singuardar(n):

    victorias = 0
    empates = 0
    inicio = time.time()
    ne=0
    for i in range(n):

        

        print('-------------------')
        print("ITERACION: ",a.iteracion[0])
        print('-------------------')
        g = Game()

        b = len(a.estados)

        partida3(1,g,a,a2)

        ganador = g.ganador
        color = 'R'
        pasos = g.pasos
        
        if ganador == color:
            victorias += 1
        if ganador == '.':
            empates += 1

        r = a.recompensa(ganador)
        a.actualizar(pasos, r)

        r = a2.recompensa(ganador)
        a2.actualizar(pasos, r)

        a.iteracion[0] += 1

        ne = len(a.estados) - b

        print('-------------------')
        print("PASOS: ",len(pasos))
        print('-------------------')
        print('-------------------')
        print("NUEVOS ESTADOS: ",ne)
        print('-------------------')

    final = time.time()  


    tiempo = final - inicio
    print('-------------------')
    print("TIEMPO POR 1000 PARTIDAS: ", tiempo)
    print('-------------------')

    print('-------------------')
    print("VICTORIAS: ",victorias)
    print('-------------------')
    print("EMPATES: ",empates)
    print('-------------------')
    print("ESTADOS: ",len(a.estados))
    print('-------------------')


def entrenar(n):

    victorias = 0
    empates = 0
    inicio = time.time()
    ne=0
    for i in range(n):

        

        print('-------------------')
        print("ITERACION: ",a.iteracion[0])
        print('-------------------')
        g = Game()

        b = len(a.estados)

        partida3(1,g,a,a2)

        ganador = g.ganador
        color = 'R'
        pasos = g.pasos
        
        if ganador == color:
            victorias += 1
        if ganador == '.':
            empates += 1

        r = a.recompensa(ganador)
        a.actualizar(pasos, r)

        r = a2.recompensa(ganador)
        a2.actualizar(pasos, r)



        a.iteracion[0] += 1

        ne = len(a.estados) - b

        print('-------------------')
        print("PASOS: ",len(pasos))
        print('-------------------')
        print('-------------------')
        print("NUEVOS ESTADOS: ",ne)
        print('-------------------')

    final = time.time()  


    tiempo = final - inicio
    print('-------------------')
    print("TIEMPO POR 1000 PARTIDAS: ", tiempo)
    print('-------------------')

    print('-------------------')
    print("VICTORIAS: ",victorias)
    print('-------------------')
    print("EMPATES: ",empates)
    print('-------------------')
    print("ESTADOS: ",len(a.estados))
    print('-------------------')

    a.guardar("agente1")
    a2.guardar("agente2")


def cargar():
    a.cargar("agente1")
    a2.cargar("agente2")    

def ver(red):
    g = Game()
    a.setRed(red)
    partidaVer(1, g, a, a2)

def partidatrucada():
    print(a.color)
    g = Game()

    partida4(1, g, a2)


    ganador = g.ganador
    pasos = g.pasos
    

    r = a.recompensa(ganador)
    a.actualizar(pasos, r)

    """
    for estado in a2.estados:
        estado.imprimir()
    """
    

def partidavsIA():

    g = Game()
    a.setRed(red)
    partida2(1, g, a)

        
    




iniciar2agentes()

#cargar()

entrenar(20000)

#entrenar_singuardar(100)

#partidatrucada()
#partidatrucada()



#print(len(a.estados))

#20000 iteraciones   

#print(len(a.estados))
  



#RED NEURONAL APROXIMAR QS

red = red(1,a)

red.introducir()


red.entrenar(1000)

red.guardar()

#red.cargar()
"""
partida = 0

for i in range(len(a.estados)):

    if partida == 10:
        a.estados[i].imprimir()

    if (a.estados[i].q == -1) or (a.estados[i].q == 1):
        partida = partida +1
       




for e in a.estados:
    e.imprimir()
"""
#estado.imprimir()





#partidavsIA()

#ver(red)