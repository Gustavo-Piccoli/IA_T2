import random
import sys
import os

import advsearch.othello.board as board
from advsearch.othello.board import Board
MAX_DEPTH =7
class Node:
    def __init__(self,board,color,alpha,beta,depth,parent, acao, filhos = None,value =None):
        self.board:Board = board
        self.color = color
        self.alpha = alpha
        self.beta = beta
        self.depth = depth
        self.parent = parent
        self.acao = acao
        self.filhos:list = filhos
        self.value = value
class MinMax:
    def __init__(self,agent_color,the_board,max_depth):
        if agent_color == the_board.BLACK:
            opponent_color = the_board.WHITE
        else:
            opponent_color = the_board.BLACK
        self.agent_color = agent_color
        self.opponent_color = opponent_color
        alpha = float('-inf')
        beta = -alpha
        self.raiz =  Node(the_board,agent_color,alpha,beta,0,None,None)
        self.max_depth = max_depth
    
    def run(self):
        node = self.raiz
        #começa com nodo raiz
        max_value = self.__max_play(node)
        acao = (-1,-1)
        for filho in node.filhos:
            if filho and filho.value and filho.value == max_value:
                acao = filho.acao
                break
        return acao
    def __max_play(self,node:Node):
        """
        v = -∞ 
        para cada s em SUCESSORES(estado)
            v = max(v, VALOR-MIN(s, alfa, beta ))
            alfa = max(alfa, v)
            se alfa ≥ beta: break  // sai do loop: o MIN que chamou conhece uma alternativa beta melhor que alfa.
        retorna v
        """ 
        node.value = float('-inf')
        if node.board.is_terminal_state():
            node.value = max(node.value,self.get_state_value(node))
            return node.value
        if node.depth >= self.max_depth:
            node.value = max(node.value,self.get_state_value(node))
            return node.value
        move = None
        successors = []
        for move in node.board.legal_moves(node.color):
            succ = self.__create_successor(node,move)
            successors.append(succ)
            node.value = max(node.value,self.__min_play(succ))
            node.alpha  = max(node.alpha,node.value)
            if node.alpha >= node.beta:
                break
        node.filhos = successors
        return node.value
    def __min_play(self,node:Node):
        """
        v = +∞ 
        para cada s em SUCESSORES(estado)
            v = min(v, VALOR-MAX(s, alfa, beta ))
            beta = min(beta, v)
            se beta ≤ alfa: break  // sai do loop: o  MAX que chamou conhece uma alternativa alfa melhor que beta.
        retorna v
        """       
        node.value = float('inf')
        if node.board.is_terminal_state():
            node.value = min(node.value,self.get_state_value(node))
            return node.value
        if node.depth >= self.max_depth:
            node.value = min(node.value,self.get_state_value(node))
            return node.value
        move = None
        successors = []
        for move in node.board.legal_moves(node.color):
            succ = self.__create_successor(node,move)
            successors.append(succ)
            node.value = min(node.value,self.__max_play(succ))
            node.beta  = min(node.alpha,node.value)
            if node.alpha >= node.beta:
                break
        return node.value

    def get_state_value(self,nodo:Node):
        """
        get value for node
        """
        return nodo.board.num_pieces(self.agent_color) - nodo.board.num_pieces(self.opponent_color)
    
    def __create_successor(self,node: Node,move):
        if node.color == node.board.BLACK:
            opponent_color = node.board.WHITE
        else:
            opponent_color = node.board.BLACK
        copy_board = node.board.copy()
        copy_board.process_move(move, node.color)
        return Node(copy_board,opponent_color,node.alpha,node.beta,node.depth + 1,node,move)

        
def make_move(the_board:Board, color):
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
        
        board_copy = the_board.copy()
        min_max = MinMax(color,board_copy,5)
        acao = min_max.run()
        return acao

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