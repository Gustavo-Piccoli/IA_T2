import random
import sys
import os
"""
caminho = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\othello"
sys.path.append(caminho)
import board
from board import Board
from my_heuristic import My_Heuristic
from node import Node
from heuristic import Heuristic
"""


import advsearch.othello.board as board
from advsearch.othello.board import Board
from advsearch.perry_o_ornitorrinco.heuristic import Heuristic
from advsearch.perry_o_ornitorrinco.node import Node
from advsearch.perry_o_ornitorrinco.my_heuristic import My_Heuristic


MAX_DEPTH = 4

class MinMax:

    def __init__(self,agent_color,the_board:Board,max_depth, heuristic:Heuristic):
        
        self.agent_color = agent_color
        self.opponent_color = the_board.opponent(agent_color)
        alpha = float('-inf')
        beta = -alpha
        self.raiz =  Node(the_board,agent_color,alpha,beta,0,None,None)
        self.max_depth = max_depth
        self.heuristic = heuristic

    def run(self):
        node = self.raiz
        #começa com node raiz
        max_value = self.__max_play(node)
        move = (-1,-1)
        for successor in node.successors:
            if successor and successor.value and successor.value == max_value:
                move = successor.move
                break
    
        return move

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
           if node.board.winner() == node.color:
                node.value = float('inf')
                return node.value
        if node.depth >= self.max_depth:
            node.value = max(node.value,self.quiesce(node.alpha,node.beta,node,0))
            return node.value
        move = None
        successors = []
        for move in node.board.legal_moves(node.color):
            succ = self.__create_successor(node,move)
            successors.append(succ)
            node.value = max(node.value,self.__min_play(succ))
            if node.value >= node.beta:
                break
            node.alpha  = max(node.alpha,node.value)
        node.successors = successors
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
            if node.board.winner() == node.color:
                node.value = float('-inf')
                return node.value
        if node.depth >= self.max_depth:
            node.value = min(node.value,self.quiesce(node.alpha,node.beta,node,0))
            return node.value
        move = None
        successors = []
        for move in node.board.legal_moves(node.color):
            succ = self.__create_successor(node,move)
            successors.append(succ)
            node.value = min(node.value,self.__max_play(succ))
            if node.value <= node.alpha:
                break
            node.beta  = min(node.beta,node.value)
        node.successors = successors
        return node.value
    def quiesce(self,alpha, beta, node:Node, depth):

        """
         most obvious ones: forced moves (i.e. there is only one move), corner moves
        """
        stand_pat = self.heuristic.get_state_value(node)
        if depth == 2:
            return stand_pat
        if stand_pat >= beta:
            return beta
        if alpha < stand_pat:
            alpha = stand_pat
        
        legal_moves = node.board.legal_moves(node.color)
        for move in legal_moves:
            if len(legal_moves) <= 1 or self.__corner_move(move):
                succ = self.__create_successor(node,move)
                score = -self.quiesce( -beta, -alpha, succ, depth+1)
                if score >= beta:
                    return beta
                if score > alpha:
                    alpha = score
        
        return alpha
    def __corner_move(self,move):
        move = (move[1],move[0]) # movimento é inverso por algum motivo, bizarro

        if move == (0,1) or move == (1,0) or move == (1,1) or move == (0,0):
            return True
        if move == (0,6) or move == (1,7) or move == (1,6) or move == (0,7):
            return True
        if move == (7,1) or move == (6,0) or move == (6,1) or move == (7,0):
            return True
        if move == (7,6) or move == (6,7) or move == (6,6) or move == (7,7): 
            return True
        return False 
    
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
    heuristic = My_Heuristic(color)
    board_copy = the_board.copy()
    min_max = MinMax(color,board_copy,MAX_DEPTH,heuristic)
    #verifica se o jogo acabou
    the_board.print_board()
    if the_board.is_terminal_state():
        print('a')
        return (-1, -1)
    #faz a jogada
    else:
        move = min_max.run()
        if move == (-1,-1):
            pass
        return move

'''
Minhas Notas:
Recebe um tabuleiro e uma cor e retorna um movimento
Um movimento é uma tupla com dois inteiros com valores entre 0 e 7
Caso não haja movimento valido, retorna a tupla -1, -1
O primeiro inteiro é a coluna e o segundo a linha
'''

