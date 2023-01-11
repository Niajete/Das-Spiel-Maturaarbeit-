from Konstant import *
import pygame
import numpy as np
import random
import copy

screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(BG_Color)


class Board:
    def __init__(self):
        self.squares = np.zeros((ROWS, COLS))
        self.empty_sqrs = self.squares #Liste
        self.marked_sqrs = 0 #Numer
        
    def final_state(self, show=False):

        # Falls es noch keinen Gewinner gibt -- return 0 (bedeutet nicht, dass es unentschieden ist)
        # Falls Player 1 gewinnt -- return 1
        # Falls Player 2 gewinnt -- return 2

        # Vertikalle gewinne
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = CIRC_Color if self.squares[0][col] == 2 else CROSS_Color
                    iPos = (col * SQSIZE + SQSIZE // 2, 20)
                    fPos = (col * SQSIZE + SQSIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[0][col]

        # Horizontalle gewinne
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = CIRC_Color if self.squares[row][0] == 2 else CROSS_Color
                    iPos = (20, row * SQSIZE + SQSIZE // 2)
                    fPos = (WIDTH - 20, row * SQSIZE + SQSIZE // 2 )
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[row][0]

        # desc diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                    color = CIRC_Color if self.squares[1][1] == 2 else CROSS_Color
                    iPos = (20, 20)
                    fPos = (WIDTH - 20, HEIGHT - 20 )
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
            return self.squares[1][1]

        # asc diagonal
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                    color = CIRC_Color if self.squares[1][1] == 2 else CROSS_Color
                    iPos = (20, HEIGHT - 20)
                    fPos = (WIDTH - 20, 20 )
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
            return self.squares[1][1]
                # desc diagonal

        # kein Gewinner
        return 0 

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range (COLS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append ((row, col)) # append = used to add a single item to certain collection types

        return empty_sqrs

    def isfull(self):
        return self.marked_sqrs == 9

    def isempty(self):
        return self.marked_sqrs == 0


class Game:

    def __init__(self):    
        self.board = Board()
        self.player = 1   #1-cross  #2-circles
        self.gamemode = 'ai'
        self.running = True
        self.show_lines()

    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()


    def show_lines(self):

        screen.fill(BG_Color)

        # Vertikal
        pygame.draw.line(screen, LINE_Color, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_Color, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)

        # Horizontal
        pygame.draw.line(screen, LINE_Color, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_Color, (0, HEIGHT - SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)

    def draw_fig(self, row, col):
        if self.player == 1:
            #draw Kruez
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen, CROSS_Color, start_desc, end_desc, CROSS_WIDTH)

            start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pygame.draw.line(screen, CROSS_Color, start_asc, end_asc, CROSS_WIDTH)

        elif self.player == 2:
            #draw Kreis
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(screen, CIRC_Color, center, RADIUS, CIRC_WIDTH)

    def next_turn(self):
        self.player = self.player % 2 + 1 # % zeigt unterschied zw. Player und 2 -- Wenn Player 1; 1+1 =2 

    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull() # Show = True -- winning lines zeichnen

class AI:
    def __init__(self, player=2): # AI = Player 2
        self.player = player

    def rnd(self, board):
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0, len(empty_sqrs))

        return empty_sqrs[idx] # (row, col)

    def eval(self, main_board):
       move = self.rnd(main_board)

       return move

class Minimax:
    def __init__(self, player=2): # AI = Player 2
        self.player = player

    def minimax(self, Board, maximizing):
        
        #terminal case
        case = Board.final_state() #ergibt eine Nummer zw. 0 und 2

        # player 1 gewinnt
        if case == 1:
            return 1, None #eval, move -- benötigen nur eval deswegen move = None

        # player 2 gewinnt
        if case == 2:
            return -1, None

        # unentschieden
        elif Board.isfull():
            return 0, None

        if maximizing:
            max_eval = -10
            best_move = None
            empty_sqrs = Board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(Board) #Testen auf einer Kopie des Boards
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0] 
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 10
            best_move = None
            empty_sqrs = Board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(Board) #Testen auf einer Kopie des Boards
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True)[0] 
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move


    def eval(self, main_board):
        eval, move = self.minimax(main_board, False) # False = AI ist minimizer

        #print(f"AI has chosen to mark the square in pos {move} with an eval of: {eval} ")

        return move