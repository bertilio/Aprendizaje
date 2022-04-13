
from juego import TicTacToe
import math
import pickle
import numpy
from numpy.random import choice
import sys
import random
from mega import Mega

NONE = '.'
FILAS = 3
COLUMNAS = 3

descuento = 0.4
alfa = 0.25
e = 0.000001
t = 1
qinicial = 6
mega = Mega()
m = mega.login("albertovicentedelegido@gmail.com", "USOCw8KsCIO")


class agente:

    def __init__(self, player, juego):

        self.estados = dict()
        self.player = player
        self.juego = juego
        self.iteracion = 0

    def guardar(self, archivo):

        name = archivo
        archivo = open(archivo+'.pickle', 'wb')
        array = [self.player, self.estados, self.iteracion]
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
        print("Agente " + archivostr + " con " + str(len(self.estados)) +
              " estados y que juega con la ficha: " + self.player + " cargado")


    def setEstados(self, pasos):

        propios = [] #Pasos del jugador para devolver

        empieza = False

        if pasos[1].count(self.player)==1: #Si ha hecho el primer movimiento
            empieza = True
        
        indice = 0

        for estado in pasos:

            if empieza and (indice%2!=0): #Si empieza sus estados son los impares
                
                if self.estados.get(estado) == None:

                    self.estados.setdefault(estado, qinicial)
                
                propios.append(estado)

            elif (not empieza) and (indice%2==0) and (indice != 0): #Si no empieza sus estados son los pares

                if self.estados.get(estado) == None:

                    self.estados.setdefault(estado, qinicial)
                
                propios.append(estado)

            indice += 1
        return propios

    
    def politicaAleatoria(self):

        acciones, tableros = self.juego.getTableros(self.player)

        return acciones[random.randint(0, len(acciones)-1)]

    def politica(self):

        acciones, tableros = self.juego.getTableros(self.player)



        # Sacamos las Qs de los tableros

        qs = []

        for tablero in tableros:
            if self.estados.get(tablero) == None:
                qs.append(qinicial)
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

    def politicaVoraz(self):

        acciones, tableros = self.juego.getTableros(self.player)



        # Sacamos las Qs de los tableros

        qs = []

        for tablero in tableros:
            if self.estados.get(tablero) == None:
                qs.append(qinicial)
            else:
                qs.append(self.estados.get(tablero))


        # Elegimos la accion con mayor q

        qmax = max(qs)

        indice = qs.index(qmax)

        return acciones[indice]
    

    def maxQProxima(self,estado):

        hijos = self.juego.getHijosContrario(estado, self.player)#saco los hijos del estado, los que son estados del otro jugador

        nmax = 0

        for hijo in hijos: #por cada hijo 

            nietos = self.juego.getHijosPropios(hijo, self.player) #Saco los nietos, estados del jugador propio
            
           

            for nieto in nietos: #por cada nieto

                qnieto = self.estados.get(nieto) #saco su q y si es mayor que nmax las intercambio

                if qnieto != None:


                    if qnieto > nmax:

                        nmax = qnieto


        return nmax



    def actualizar(self, pasos, ganador):

        #Definimos recompensa del estado final
        recompensa = 0

        if ganador == self.player:

            recompensa = 10

        elif ganador == "-":

            recompensa = 5
        
        elif self.player == "X":

            if ganador == "O": #Si pierde

                recompensa = -5

        elif self.player == "O":

            if ganador == "X": #Si pierde

                recompensa = -5

        # guardamos los pasos
        propios = self.setEstados(pasos)

        primero = True

        indice = len(propios)-1

        while indice >= 0 :

            q = self.estados.get(propios[indice])

            

            if not primero: #Si no es el primero

                #calculo nueva q

                nuevaq = (1-alfa) * q + alfa* (recompensa + descuento * self.maxQProxima(propios[indice]))

                #actualizamos q
                recompensa = 0
                dic = {propios[indice]: nuevaq}
                self.estados.update(dic)
            else:

                #calculo nueva q

                nuevaq = recompensa
                recompensa = 0
                #actualizamos q
                dic = {propios[indice]: nuevaq}
                self.estados.update(dic)

            indice = indice - 1
            primero = False

        self.iteracion += 1