
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
e = 0.5
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

        acciones, tableros = self.juego.getTableros("X")

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

    
    def actualizarPadres(self,paso):

        # sacamos los padres del paso final
        padres = self.juego.getPadres(paso)


        for padre in padres: #A cada padre

            # Hay que ver si esta guardado, en caso contrario no se sigue por ese camino

            q = self.estados.get(padre)

            if q != None: #Verificamos si existe el padre en la lista estados

                hijos = self.juego.getHijos(padre)
                
                qs = []

                # guardamos la q de cada hijo

                for hijo in hijos:

                    qhijo = self.estados.get(hijo)
                    
                    if qhijo != None:

                        qs.append(qhijo)
                # sacamos la Q maxima de los hijos

                qmax = max(qs)
                # sacamos la nueva q del estado

                nuevaq = (1-v) * q + v * r * qmax


                # actualizamos la q del padre actual

                dic = {padre : nuevaq}
                self.estados.update(dic)
    def actualizar(self, pasos,ganador):

        # guardamos los pasos
        self.setEstados(pasos,ganador)

        #actualizamos los padres del paso final
        self.actualizarPadres(pasos[len(pasos)-1])

        #sacamos los padres
        padres = self.juego.getPadres(pasos[len(pasos)-1])

        for i in range(len(pasos)-1): #por cada nivel de profundidad por encima del paso final
            #aqui guardaremos la siguiente generacion
            abuelos = []



            for padre in padres:

                q = self.estados.get(padre)

                if q != None: #Verificamos si existe el padre en la lista estados


                    #actualizamos sus padres
                    self.actualizarPadres(padre)

                    #guardamos sus padres en abuelos
                    abuelos+=self.juego.getPadres(padre)

            
            padres = abuelos

        self.iteracion +=1





        
        
            
