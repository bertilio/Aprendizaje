
from itertools import groupby, chain
from juego import TicTacToe
import math
import pickle
import random
import numpy
from numpy.random import choice
import sys
from mega import Mega

NONE = '.'
FILAS = 3
COLUMNAS = 3

r = 0.8
v = 0.5
e = 0.3
t = 1

mega = Mega()
m = mega.login("albertovicentedelegido@gmail.com", "USOCw8KsCIO")

class agente:

    def __init__(self, player, juego):

        self.estados = dict()
        self.player = player
        self.juego = juego
        self.iteracion = 0

    def guardar(self, name):

        archivo = open(name+'.pickle', 'wb')
        array = [self.player, self.estados,self.iteracion]
        sys.setrecursionlimit(100000)
        pickle.dump(array, archivo)
        file = m.upload(name+'.pickle')
        print(m.get_upload_link(file))
        archivo.close()

    def cargar(self, archivostr):

        archivo = open(archivostr+'.pickle', 'rb')
        array = pickle.load(archivo)
        self.player = array[0]
        self.estados = array[1]
        self.iteracion = array[2]
        print("Agente " + archivostr + "cargado")
        print(self.iteracion)

    def setEstados(self, pasos, ganador):
        indice = 1
        for estado in pasos:

            if indice == len(pasos):
                if self.estados.get(estado) == None:
                    if ganador == self.player:
                        self.estados.setdefault(estado, 10)
                    elif ganador == "-":
                        self.estados.setdefault(estado, 0)
                    else:
                        self.estados.setdefault(estado, -10)
            else:
                if self.estados.get(estado) == None:
                    self.estados.setdefault(estado, 0)

            indice += 1

    def politica(self):

        acciones, tableros = self.juego.getTableros(self.player)

        # Sacamos las Qs de los tableros

        qs = []

        for tablero in tableros:
            if self.estados.get(tablero) == None:
                qs.append(0)
            else:
                qs.append(self.estados.get(tablero))

        # Calculo de probabilidades

        qtotal = 0

        for q in qs:
            qtotal += math.exp(q*e*t)

        probabilidades = []

        for q in qs:
            probabilidades.append(math.exp(q*e*t)/qtotal)

        # Elegimos aleatoriamente la accion

        indice = choice(len(acciones), 1, p=probabilidades)

        return acciones[indice[0]]

    
    def actualizar(self, pasos, ganador):

        # guardamos los pasos
        self.setEstados(pasos, ganador)

        primero = True

        pasos.reverse()

        indice = 0

        for paso in pasos:

            q = self.estados.get(paso)

            if not primero:

                #calculo nueva q

                nuevaq = (1-v) * q + v * r * self.estados.get(pasos[indice-1])

                #actualizamos q

                dic = {paso: nuevaq}
                self.estados.update(dic)
            
            indice = indice + 1
            primero = False

        self.iteracion += 1





        
        
            
