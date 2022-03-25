import random
import copy
import time


class TicTacToe:

    def __init__(self):
        self.board = []
        self.pasos = []

    def create_board(self):

        self.board = []

        for i in range(3):
            row = []
            for j in range(3):
                row.append('-')
            self.board.append(row)

        self.pasos = []
        self.guardarPaso()

    def getEstado(self):

        

        estado = []

        for i in range(len(self.board)):

            for j in range(len(self.board)):

                if self.board[i][j] == "X":
                    estado.append(1)
                elif self.board[i][j] == "O":
                    estado.append(-1)
                else:
                    estado.append(0)
        return estado

    def getEstadoReverse(self,estado):

        estado = []

        for i in range(len(estado)):

            for j in range(len(estado)):

                if estado[i][j] == 1:
                    estado.append("X")
                elif estado[i][j] == -1:
                    estado.append("O")
                else:
                    estado.append("-")

        return estado
    
    def convertir(self,board):

        estado = []

        for i in range(len(board)):

                if board[i] == "X":
                    estado.append(1)
                elif board[i] == "O":
                    estado.append(-1)
                else:
                    estado.append(0)

        return estado
  
    
    def notFinished(self):


        if (self.is_player_win("X") == False) and (self.is_player_win("O") == False):

            return True


    def tableroToString(self):
        cadena = ""
        for fila in self.board:
            for columna in fila:
                cadena += columna
        return cadena

    def guardarPaso(self):
        cadena = ""
        for fila in self.board:
            for columna in fila:
                cadena += columna
        self.pasos.append(cadena)

    def get_random_first_player(self):
        return random.randint(0, 1)

    def fix_spot(self, row, col, player, real):

        if real and self.board[row][col] != "-":

            return False

        self.board[row][col] = player

        if real:
            self.guardarPaso()

        return True
    
    def freeSpots(self):
        
        huecos = 0

        for fila in self.board:
            huecos += fila.count("-")
        
        return huecos


    def getHijos(self, tablero):

        indice = 0

        for casilla in tablero:
            self.board[indice//3][indice % 3] = casilla
            indice += 1

        resultado = []
        casillas = []

        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "-":
                    casillas.append([i, j])

        for pos in casillas:
            player = self.board[pos[0]][pos[1]]

            self.fix_spot(pos[0], pos[1], 'X', False)

            cadena = ""
            for fila in self.board:
                for columna in fila:
                    cadena += columna
            resultado.append(cadena)

            self.fix_spot(pos[0], pos[1], '-', False)

            player = self.board[pos[0]][pos[1]]

            self.fix_spot(pos[0], pos[1], 'O', False)

            cadena = ""
            for fila in self.board:
                for columna in fila:
                    cadena += columna
            resultado.append(cadena)

            self.fix_spot(pos[0], pos[1], '-', False)

        return resultado

    def getHijosContrario(self, tablero, player):

        if player == "X":
            player = "O"
        else:
            player = "X"

        indice = 0

        for casilla in tablero:
            self.board[indice//3][indice % 3] = casilla
            indice += 1

        resultado = []
        casillas = []

        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "-":
                    casillas.append([i, j])

        for pos in casillas:

            self.fix_spot(pos[0], pos[1], player, False)

            cadena = ""
            for fila in self.board:
                for columna in fila:
                    cadena += columna
            resultado.append(cadena)

            self.fix_spot(pos[0], pos[1], '-', False)

        return resultado

    def getHijosPropios(self, tablero, player):

        indice = 0

        for casilla in tablero:
            self.board[indice//3][indice % 3] = casilla
            indice += 1

        resultado = []
        casillas = []

        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "-":
                    casillas.append([i, j])

        for pos in casillas:

            self.fix_spot(pos[0], pos[1], player, False)

            cadena = ""
            for fila in self.board:
                for columna in fila:
                    cadena += columna
            resultado.append(cadena)

            self.fix_spot(pos[0], pos[1], '-', False)

        return resultado

    def getTableros(self, player):
        resultado = [[], []]

        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '-':
                    resultado[0].append([i, j])

        for pos in resultado[0]:

            self.fix_spot(pos[0], pos[1], player, False)

            cadena = ""
            for fila in self.board:
                for columna in fila:
                    cadena += columna
            resultado[1].append(cadena)

            self.fix_spot(pos[0], pos[1], '-', False)

        return resultado

    def getPadres(self, tablero):

        indice = 0
        for casilla in tablero:
            self.board[indice//3][indice % 3] = casilla
            indice += 1

        resultado = []
        casillas = []

        for i in range(3):
            for j in range(3):
                if self.board[i][j] != "-":
                    casillas.append([i, j])

        for pos in casillas:
            player = self.board[pos[0]][pos[1]]

            self.fix_spot(pos[0], pos[1], '-', False)

            cadena = ""
            for fila in self.board:
                for columna in fila:
                    cadena += columna
            resultado.append(cadena)

            self.fix_spot(pos[0], pos[1], player, False)

        return resultado

    def is_player_win(self, player):
        win = None

        n = len(self.board)

        # checking rows
        for i in range(n):
            win = True
            for j in range(n):
                if self.board[i][j] != player:
                    win = False
                    break
            if win:
                return win

        # checking columns
        for i in range(n):
            win = True
            for j in range(n):
                if self.board[j][i] != player:
                    win = False
                    break
            if win:
                return win

        # checking diagonals
        win = True
        for i in range(n):
            if self.board[i][i] != player:
                win = False
                break
        if win:
            return win

        win = True
        for i in range(n):
            if self.board[i][n - 1 - i] != player:
                win = False
                break
        if win:
            return win
        return False

        for row in self.board:
            for item in row:
                if item == '-':
                    return False
        return True

    def is_board_filled(self):
        for row in self.board:
            for item in row:
                if item == '-':
                    return False
        return True

    def swap_player_turn(self, player):
        return 'X' if player == 'O' else 'O'

    def show_board(self):
        for row in self.board:
            for item in row:
                print(item, end=" ")
            print()

    def start(self, ver, a1, a2):

        self.create_board()


        player = 'X' if self.get_random_first_player() == 1 else 'O'

        while True:
            if ver:
                print(f"Player {player} turn")
            if ver:
                self.show_board()

            if player == 'X':
                if not a1:
                    # taking user input
                    row, col = list(
                        map(int, input("Enter row and column numbers to fix spot: ").split()))
                    print()
                    # fixing the spot
                    success = self.fix_spot(row - 1, col - 1, player, True)
                else:
                    row, col = a1.politica()
                    success = self.fix_spot(row, col, player, True)
                    if ver:
                        time.sleep(2)
            else:
                if not a2:
                    # taking user input
                    row, col = list(
                        map(int, input("Enter row and column numbers to fix spot: ").split()))
                    print()
                    # fixing the spot
                    success = self.fix_spot(
                        row - 1, col - 1, player, True)
                else:
                    row, col = a2.politica()
                    success = self.fix_spot(row, col, player, True)
                    if ver:
                        time.sleep(2)

            if not success:

                return (player+"error", copy.deepcopy(self.pasos))                

            # checking whether current player is won or not
            if self.is_player_win(player):
                if not a1 and not a2:
                    if ver:
                        print(f"Player {player} wins the game!")
                        break
                else:
                    if ver:
                        print(f"Player {player} wins the game!")
                        self.show_board()
                    return (player, copy.deepcopy(self.pasos))

            # checking whether the game is draw or not
            if self.is_board_filled():
                if not a1 and not a2:
                    if ver:
                        print("Match Draw!")
                        break
                else:
                    if ver:
                        print("Match Draw!")
                        self.show_board()
                    return ("-", copy.deepcopy(self.pasos))

            # swapping the turn
            player = self.swap_player_turn(player)

        # showing the final view of board
        if ver:
            print()
            self.show_board()
        return ("-", copy.deepcopy(self.pasos))

    def startPVP(self, ver, a1, a2):

        self.create_board()

        player = 'X' if self.get_random_first_player() == 1 else 'O'

        while True:
            if ver:
                print(f"Player {player} turn")
            if ver:
                self.show_board()

            if player == 'X':
                if not a1:
                    # taking user input
                    row, col = list(
                        map(int, input("Enter row and column numbers to fix spot: ").split()))
                    print()
                    # fixing the spot
                    success= self.fix_spot(
                        row - 1, col - 1, player, True)
                else:
                    row, col = a1.politicaVoraz()
                    success= self.fix_spot(row, col, player, True)
                    if ver:
                        time.sleep(2)
            else:
                if not a2:
                    # taking user input
                    row, col = list(
                        map(int, input("Enter row and column numbers to fix spot: ").split()))
                    print()
                    # fixing the spot
                    success= self.fix_spot(
                        row - 1, col - 1, player, True)
                else:
                    row, col = a2.politicaVoraz()
                    success= self.fix_spot(row, col, player, True)
                    if ver:
                        time.sleep(2)

            if not success:

                return (player+"error", copy.deepcopy(self.pasos)) 

            # checking whether current player is won or not
            if self.is_player_win(player):
                if not a1 and not a2:
                    if ver:
                        print(f"Player {player} wins the game!")
                        break
                else:
                    if ver:
                        print(f"Player {player} wins the game!")
                        self.show_board()
                    return (player, copy.deepcopy(self.pasos))

            # checking whether the game is draw or not
            if self.is_board_filled():
                if not a1 and not a2:
                    if ver:
                        print("Match Draw!")
                        break
                else:
                    if ver:
                        print("Match Draw!")
                        self.show_board()
                    return ("-", copy.deepcopy(self.pasos))

            # swapping the turn
            player = self.swap_player_turn(player)
        # showing the final view of board
        if ver:
            print()
            self.show_board()
        return ("-", copy.deepcopy(self.pasos))

    def startPVPRand(self, ver, a1, a2):

        self.create_board()

        player = 'X' if self.get_random_first_player() == 1 else 'O'

        while True:
            if ver:
                print(f"Player {player} turn")
            if ver:
                self.show_board()

            if player == 'X':
                if not a1:
                    # taking user input
                    row, col = list(
                        map(int, input("Enter row and column numbers to fix spot: ").split()))
                    print()
                    # fixing the spot
                    success= self.fix_spot(
                        row - 1, col - 1, player, True)
                else:
                    row, col = a1.politicaAleatoria()
                    success= self.fix_spot(row, col, player, True)
                    if ver:
                        time.sleep(2)
            else:
                if not a2:
                    # taking user input
                    row, col = list(
                        map(int, input("Enter row and column numbers to fix spot: ").split()))
                    print()
                    # fixing the spot
                    success= self.fix_spot(
                        row - 1, col - 1, player, True)
                else:
                    row, col = a2.politicaVoraz()
                    success = self.fix_spot(row, col, player, True)
                    if ver:
                        time.sleep(2)

            if not success:

                return (player+"error", copy.deepcopy(self.pasos)) 

            # checking whether current player is won or not
            if self.is_player_win(player):
                if not a1 and not a2:
                    if ver:
                        print(f"Player {player} wins the game!")
                        break
                else:
                    if ver:
                        print(f"Player {player} wins the game!")
                        self.show_board()
                    return (player, copy.deepcopy(self.pasos))

            # checking whether the game is draw or not
            if self.is_board_filled():
                if not a1 and not a2:
                    if ver:
                        print("Match Draw!")
                        break
                else:
                    if ver:
                        print("Match Draw!")
                        self.show_board()
                    return ("-", copy.deepcopy(self.pasos))

            # swapping the turn
            player = self.swap_player_turn(player)
        # showing the final view of board
        if ver:
            print()
            self.show_board()
        return ("-", copy.deepcopy(self.pasos))