import random
import sys
import os
caminho = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\othello"
sys.path.append(caminho)
import board




def make_move(the_board, color):
    """
    Returns an Othello move
    :param the_board: a board.Board object with the current game state
    :param color: a character indicating the color to make the move ('B' or 'W')
    :return: (int, int) tuple with x, y indexes of the move (remember: 0 is the first row/column)
    """
    #verifica se o jogo acabou
    the_board.print_board()
    if the_board.is_terminal_state():
        return (-1, -1)
    #faz a jogada
    else:
        (tabuleiro, cor, m, pos_x, pos_y) = max_play(the_board, color, 0, -7, 7)
        return (pos_x, pos_y)



def max_play(the_board, color, m, alfa, beta):
    maximizar = -7
    pos_x = None
    pos_y = None
    if the_board.is_terminal_state():
        return (the_board, color, m, -1, -1)
    for i in range (8):
        for j in range (8):
            if the_board.is_legal((i, j), color):  
                the_board.tiles[i][j] = color
                (tabuleiro, cor, m, min_i, min_j) = min_play(the_board, color, m, alfa, beta)
                if maximizar < m:
                    maximizar = m
                    pos_x = i
                    pos_y = j
                    the_board.tiles[i][j] = '.'
                if maximizar >= beta:
                    return (tabuleiro, cor, maximizar, pos_x, pos_y)
                if maximizar > alfa:
                    alfa = maximizar
    return (tabuleiro, cor, maximizar, pos_x, pos_y)



def min_play(the_board, color, m, alfa, beta):
    minimizar = 7
    pos_x = None
    pos_y = None
    if the_board.is_terminal_state():
        return (the_board, color, m, -1, -1)
    for i in range (8):
        for j in range (8):
            if the_board.is_legal((i, j), color):  
                if color == 'B':
                    color_i = 'W'
                else:
                    color_i = 'B'
                the_board.tiles[i][j] = color_i
                (tabuleiro, cor, m, max_i, max_j) = max_play(the_board, color, m, alfa, beta)
                if minimizar > m:
                    minimizar = m
                    pos_x = i
                    pos_y = j
                    the_board.tiles[i][j] = '.'
                if minimizar <= alfa:
                    return (tabuleiro, cor, minimizar, pos_x, pos_y)
                if minimizar < beta:
                    beta = minimizar
    return (tabuleiro, cor, minimizar, pos_x, pos_y)

'''
Minhas Notas:
Recebe um tabuleiro e uma cor e retorna um movimento
Um movimento é uma tupla com dois inteiros com valores entre 0 e 7
Caso não haja movimento valido, retorna a tupla -1, -1
O primeiro inteiro é a coluna e o segundo a linha
'''
o = board.Board()
print(make_move(o, 'W'))