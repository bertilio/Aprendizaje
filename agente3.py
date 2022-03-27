
from juego import TicTacToe
import math
import pickle
import numpy as np
import random
from numpy.random import choice
import sys
from mega import Mega

from tensorflow.keras import Model, Sequential
from tensorflow.keras.layers import Dense, Flatten, Activation
from tensorflow.keras.optimizers import Adam

NONE = '.'
FILAS = 3
COLUMNAS = 3

mega = Mega()
m = mega.login("albertovicentedelegido@gmail.com", "USOCw8KsCIO")

descuento = 0.68
alfa = 0.25
e = 1
emax = 1
emin = 0.1
decay = 0.001
t = 1



class agente3:

    def __init__(self, player, juego):

        self.replay = []
        self.partida = []
        self.player = player
        self.juego = juego
        self.iteracion = 0

        array = np.array([1,1,1,1,1,1,1,1,1])

        self.model = Sequential()
        self.model.add(Flatten(input_shape= array.shape))
        self.model.add(Dense(5))
        self.model.add(Activation('relu'))
        self.model.add(Dense(9))
        self.model.add(Activation('linear'))
        optimizer = Adam(learning_rate=0.01)
        self.model.compile(loss='mse', optimizer=optimizer)

        self.model2 = Sequential()
        self.model2.add(Flatten(input_shape= array.shape))
        self.model2.add(Dense(5))
        self.model2.add(Activation('relu'))
        self.model2.add(Dense(9))
        self.model2.add(Activation('linear'))
        self.model2.compile(loss='mse', optimizer=optimizer)

    def guardar(self, archivo):
        name = archivo
        archivo = open(archivo+'.pickle', 'wb')
        array = self.iteracion
        #sys.setrecursionlimit(100000)
        #pickle.dump(array, archivo)
        #archivo.close()
        self.model.save_weights(name+'.h5')
        file = m.upload(name+'.h5')
        print(m.get_upload_link(file))

    def cargar(self, archivostr):
        archivo = open(archivostr+'.pickle', 'rb')
        array = pickle.load(archivo)
        #self.player = array[0]
        #self.replay = array[1]
        self.iteracion = array
        self.model.load_weights(archivostr+'.h5')
        self.model2.load_weights(archivostr+'.h5')
        print("Agente " + archivostr + " con " + str(len(self.replay)) +
              " estados y que juega con la ficha: " + self.player + " cargado")


    def politicaAleatoria(self):

        acciones, tableros = self.juego.getTableros(self.player)

        return acciones[random.randint(0, len(acciones)-1)]

    def politica(self):

        tablero = self.juego.getEstado()

        if (random.random() < e):

            accion = random.randint(0, 8)

        else:

            # Sacamos las Qs de los tableros
            qs = self.model.predict([[tablero]])


            accion = np.argmax(qs)

        row = accion // 3

        col = (accion % 3) 

        reward = 0

        nuevo = [tablero,accion,reward,[]]

        self.partida.append(nuevo)

        return [row,col]

    def politicaVoraz(self):
        # Sacamos las Qs de los tableros
        tablero = self.juego.getEstado()
        qs = self.model.predict([[tablero]])
        q = np.argmax(qs)

        row = q // 3

        col = (q % 3) 

        return [row,col]
    
    def maxQProxima(self,estado):

        estado = self.juego.getEstadoReverse(estado)

        hijos = self.juego.getHijosContrario(estado, self.player)#saco los hijos del estado, los que son estados del otro jugador

        nmax = 0

        for hijo in hijos: #por cada hijo 

            x = self.juego.convertir(hijo)
            qs = self.model.predict([x])

            qhijo = np.max(qs)

            if qhijo> nmax:

                nmax = qhijo


        return nmax



    def actualizar(self, ganador):

        e = emin + (emax-emin) * np.exp(-decay * self.iteracion)

        #Definimos recompensa del estado final
        recompensa = 0

        if ganador == self.player:

            recompensa = 10

        elif ganador == "-":

            recompensa = 5

        elif ganador == (self.player + "error"):

            recompensa = -10

        primero = True

        indice = len(self.partida)-1

        while indice >= 0 :

            if recompensa == -10 : #Si ha habido fallo
                #Guardamos la recompensa
                if primero:

                    self.partida[indice][2] = recompensa
            else:
                
                self.partida[indice][2] = recompensa

            nuevo = True

            self.replay.append(self.partida[indice])

            indice = indice - 1
            primero = False


        self.partida = []

        self.iteracion += 1

        if self.iteracion%4==0:

            self.train(32)

        if self.iteracion%100==0:

            print("-------------------------")
            print("Pesos copiados")
            print("-------------------------")

            self.model2.set_weights(self.model.get_weights())
    

    def train(self,batch):

        inputs = []
        outputs = []
        

        if len(self.replay) < batch:

            for jugada in self.replay:

                x = jugada[0] #estado

                qs = self.model.predict([x])[0] #Predecir qs de las acciones desde el estado

                qFutura = jugada[2] + descuento * self.maxQProxima(x) #Valor q futuro

                qs[jugada[1]] = (1-alfa) * qs[jugada[1]] + alfa * qFutura #Actualizamos la q

                inputs.append(x) #Añadimos el estado convertido a los inputs

                outputs.append(qs)

            self.model.fit(np.array(inputs),np.array(outputs),batch_size=batch,verbose=0, shuffle=True)
        else:
        
            indices = np.random.randint(len(self.replay), size=batch)
    


            for indice in indices:

                jugada = self.replay[indice]

                x = jugada[0] #estado

                qs = self.model.predict([x])[0] #Predecir qs de las acciones desde el estado

                qFutura = jugada[2] + descuento * self.maxQProxima(x) #Valor q futuro

                qs[jugada[1]] = (1-alfa) * qs[jugada[1]] + alfa * qFutura #Actualizamos la q

                inputs.append(x) #Añadimos el estado convertido a los inputs

                outputs.append(qs)
          


            self.model.fit(np.array(inputs),np.array(outputs),batch_size=batch,verbose=0, shuffle=True)

        
