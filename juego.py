#! /usr/bin/env python3
from itertools import groupby, chain
import time
import os

NONE = '.'
RED = 'R'
YELLOW = 'Y'


def diagonalsPos(matrix, cols, rows):
    """Get positive diagonals, going from bottom-left to top-right."""
    for di in ([(j, i - j) for j in range(cols)] for i in range(cols + rows - 1)):
        yield [matrix[i][j] for i, j in di if i >= 0 and j >= 0 and i < cols and j < rows]


def diagonalsNeg(matrix, cols, rows):
    """Get negative diagonals, going from top-left to bottom-right."""
    for di in ([(j, i - cols + j + 1) for j in range(cols)] for i in range(cols + rows - 1)):
        yield [matrix[i][j] for i, j in di if i >= 0 and j >= 0 and i < cols and j < rows]


class Game:
    def __init__(self, cols=7, rows=6, requiredToWin=4):
        """Create a new game."""
        self.cols = cols
        self.rows = rows
        self.win = requiredToWin
        self.board = [[NONE] * rows for _ in range(cols)]
        self.ganador = ''
        self.pasos = []

    def setGanador(self,g):
        self.ganador = g

    def insert(self, column, color):
        """Insert the color in the given column."""
        c = self.board[column]
        if c[0] != NONE:
            return False

        i = -1
        while c[i] != NONE:
            i -= 1
        c[i] = color
        paso = []
        for col in self.board:
            paso.append(col.copy())
        self.pasos.append(paso)
        return True

    def simularInsert(self, column, color):

        #copia del tablero

        paso = []
        for col in self.board:
            paso.append(col.copy())


        """Insert the color in the given column."""
        c = paso[column]
        if c[0] != NONE:
            return False

        i = -1
        while c[i] != NONE:
            i -= 1
        c[i] = color
        
        return paso

    def checkForWin(self):
        """Check the current board for a winner."""
        w = self.getWinner()
        if w:
            return w

    def getWinner(self):
        """Get the winner on the current board."""
        lines = (
            self.board,  # columns
            zip(*self.board),  # rows
            # positive diagonals
            diagonalsPos(self.board, self.cols, self.rows),
            # negative diagonals
            diagonalsNeg(self.board, self.cols, self.rows)
        )

        for line in chain(*lines):
            for color, group in groupby(line):
                if color != NONE and len(list(group)) >= self.win:
                    return color

    def printBoard(self):
        """Print the board."""
        print('  '.join(map(str, range(self.cols))))
        for y in range(self.rows):
            print('  '.join(str(self.board[x][y]) for x in range(self.cols)))
        print()

def partidaVer(n, g, agente, agente2):

    paso1 = []
    for col in g.board:
        paso1.append(col.copy())
    g.pasos.append(paso1)
    turn = RED

    jugar = True
    while jugar:
        time.sleep(1)
        os.system("cls")
        g.printBoard()
        colocado = False
        while not colocado:
            if turn == YELLOW:
                row = agente2.politica(g.board)
                if g.insert(int(row), turn):
                    colocado = True
            else:
                row = agente.politica(g.board)
                if g.insert(int(row), turn):
                    colocado = True
        turn = YELLOW if turn == RED else RED
        if g.checkForWin():
            os.system("cls")
            g.printBoard()
            print("Ha ganado ", g.checkForWin())
            g.setGanador(g.checkForWin())
            jugar = False
        else:
            huecos = 0
            for fila in g.board:
                huecos += fila.count(NONE)
            if huecos == 0:
                print("Empate")
                g.setGanador('.')
                jugar = False

def partida3(n, g, agente, agente2):

    paso1 = []
    for col in g.board:
        paso1.append(col.copy())
    g.pasos.append(paso1)
    turn = RED

    jugar = True
    while jugar:
        #g.printBoard()
        colocado = False
        while not colocado:
            if turn == YELLOW:
                row = agente2.politica(g.board)
                if g.insert(int(row), turn):
                    colocado = True
            else:
                row = agente.politica(g.board)
                if g.insert(int(row), turn):
                    colocado = True
        turn = YELLOW if turn == RED else RED
        if g.checkForWin():
            #print("Ha ganado ", g.checkForWin())
            g.setGanador(g.checkForWin())
            jugar = False
        else:
            huecos = 0
            for fila in g.board:
                huecos += fila.count(NONE)
            if huecos == 0:
                #print("Empate")
                g.setGanador('.')
                jugar = False

def partida4(n, g, agente):

    paso1 = []
    for col in g.board:
        paso1.append(col.copy())
    g.pasos.append(paso1)
    turn = RED

    jugar = True
    while jugar:
        g.printBoard()
        colocado = False
        while not colocado:
            if turn == YELLOW:
                row = input('{}\'s turn: '.format(
                    'Red' if turn == RED else 'Yellow'))
                if g.insert(int(row), turn):
                    colocado = True
            else:
                row = agente.politica_trucada()
                if g.insert(int(row), turn):
                    colocado = True
        turn = YELLOW if turn == RED else RED
        if g.checkForWin():
            print("Ha ganado ", g.checkForWin())
            g.printBoard()
            g.setGanador(g.checkForWin())
            jugar = False
        else:
            huecos = 0
            for fila in g.board:
                huecos += fila.count(NONE)
            if huecos == 0:
                print("Empate")
                g.setGanador('.')
                jugar = False

def partida2(n, g, agente):

    paso1 = []
    for col in g.board:
        paso1.append(col.copy())
        print(g.board)
    g.pasos.append(paso1)
    turn = RED

    jugar = True
    while jugar:
        g.printBoard()
        colocado = False
        while not colocado:
            if turn == RED:
                row = input('{}\'s turn: '.format(
                    'Red' if turn == RED else 'Yellow'))
                if g.insert(int(row), turn):
                    colocado = True
            else:
                row = agente.politica(g.board)
                if g.insert(int(row), turn):
                    colocado = True
        turn = YELLOW if turn == RED else RED
        if g.checkForWin():
            print("Ha ganado ", g.checkForWin())
            g.printBoard()
            g.setGanador(g.checkForWin())
            jugar = False
        else:
            huecos = 0
            for fila in g.board:
                huecos += fila.count(NONE)
            if huecos == 0:
                print("Empate")
                g.setGanador('.')
                jugar = False

def partida(n, g):

    paso1 = []
    for col in g.board:
        paso1.append(col.copy())
    g.pasos.append(paso1)
    turn = RED
    jugar = True
    while jugar:
        g.printBoard()
        colocado = False
        while not colocado:
            row = input('{}\'s turn: '.format(
                'Red' if turn == RED else 'Yellow'))
            if g.insert(int(row), turn):
                colocado = True
        turn = YELLOW if turn == RED else RED
        if g.checkForWin():
            print("Ha ganado ", g.checkForWin())
            g.setGanador(g.checkForWin())
            jugar = False
        else:
            huecos = 0
            for fila in g.board:
                huecos += fila.count(NONE)
            if huecos == 0:
                print("Empate")
                g.setGanador('.')
                jugar = False
    






if __name__ == '__main__':
    g = Game()
    turn = RED
    jugar = True
    while jugar:
        g.printBoard()
        colocado = False
        while not colocado:
            row = input('{}\'s turn: '.format(
                'Red' if turn == RED else 'Yellow'))
            if g.insert(int(row), turn):
                colocado = True
        turn = YELLOW if turn == RED else RED
        if g.checkForWin():
            print("Ha ganado ", g.checkForWin())
            jugar = False
