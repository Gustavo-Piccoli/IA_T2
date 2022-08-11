import random
import sys
import os
#caminho = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\othello"
#sys.path.append(caminho)
#import board
#from board import Board
import advsearch.othello.board as board
from advsearch.othello.board import Board
import math
MAX_DEPTH = 5
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

    def __init__(self,agent_color,the_board:Board,max_depth):
        
        self.agent_color = agent_color
        self.opponent_color = the_board.opponent(agent_color)
        alpha = float('-inf')
        beta = -alpha
        self.raiz =  Node(the_board,agent_color,alpha,beta,0,None,None)
        self.max_depth = max_depth
        self.agent_num_corners = self.get_num_corners(the_board,self.agent_color)
        self.opp_num_corners = self.get_num_corners(the_board,self.opponent_color)


    def num_center_pieces(self,my_board:Board,color):
        count = 0
        for i in range(2,6):
            for j in range(2,6):
                if my_board.tiles[i][j] == color:
                    count+=1
        return count
                  
    def get_num_corners_at_risk(self,my_board:Board, color):
        """
        get number of pre-corners tiles that the player possess that gives the risk of giving up a corner
        pre-corner - tile that can be eaten to get the corner
        """
        bottom_right = my_board.tiles[7][7]
        upper_right = my_board.tiles[0][7]
        bottom_left = my_board.tiles[7][0]
        upper_left = my_board.tiles[0][0]
        count=0
        if my_board.tiles[1][1] == color:
            if upper_left == self.agent_color or upper_left == self.opponent_color:
                count+=1
        if my_board.tiles[1][6] == color:
            if upper_right == self.agent_color or upper_right == self.opponent_color:
                count+=1
        if my_board.tiles[6][1] == color:
            if bottom_left == self.agent_color or bottom_left == self.opponent_color:
                count+=1
        if my_board.tiles[6][6] == color:
            if bottom_right == self.agent_color or bottom_right == self.opponent_color:
                count+=1
        return count
        
    def get_num_corners(self,my_board:Board,color):
        """
        get number of corners that the player possess
        """
        count=0
        if my_board.tiles[0][0] == color:
            count+=1
        if my_board.tiles[0][7] == color:
            count+=1
        if my_board.tiles[7][0] == color:
            count+=1
        if my_board.tiles[7][7] == color:
            count+=1
        return count

    def run(self):
        node = self.raiz
        #começa com node raiz
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
    def get_num_of_outer_pieces(self,my_board:Board,color):
        count = 0
        for i in [0,7]:
            for j in range(8):
                if my_board.tiles[i][j] == color:
                    count+=1
        for j in [0,7]:
            for i in range(1,7):
                if my_board.tiles[i][j] == color:
                    count+=1
        return count

    def get_state_value(self,node:Node):
        """
        get value for node
        """
        if node.board.is_terminal_state():
            if node.board.winner() == self.agent_color:
                return float('inf')
        pieces_in_center = self.num_center_pieces(node.board,self.agent_color)
        pieces_value = node.board.num_pieces(self.agent_color) - node.board.num_pieces(self.opponent_color)
        number_of_pieces_placed  = node.board.num_pieces(self.agent_color) + node.board.num_pieces(self.opponent_color)
        opp_legal_moves_value = len(node.board.legal_moves(self.opponent_color))
        agent_legal_moves_value = len(node.board.legal_moves(self.agent_color))
        agent_corners = self.get_num_corners(node.board,self.agent_color) - self.agent_num_corners
        opp_corners = self.get_num_corners(node.board,self.opponent_color) - self.opp_num_corners
        num_corner_risk  = self.get_num_corners_at_risk(node.board,self.agent_color)
        outer_pieces = self.get_num_of_outer_pieces(node.board,self.agent_color) - self.get_num_of_outer_pieces(node.board,self.opponent_color)
        w_corner_risk = -4
        w_opp_legal_moves = -1 
        w_agent_corner = 20
        w_opp_corner = -10
        w_pieces = modified_sigmoid(number_of_pieces_placed)
        w_pieces_in_center = 0.5*inverse_modified_sigmoid(number_of_pieces_placed)
        w_outer_pieces = 0.5
        w_agent_moves = 2*inverse_modified_sigmoid(number_of_pieces_placed)
        return w_pieces*pieces_value + opp_legal_moves_value*w_opp_legal_moves \
            + agent_legal_moves_value*w_agent_moves + agent_corners*w_agent_corner + opp_corners*w_opp_corner \
            + num_corner_risk*w_corner_risk +pieces_in_center*w_pieces_in_center + outer_pieces*w_outer_pieces
    
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
    board_copy = the_board.copy()
    min_max = MinMax(color,board_copy,MAX_DEPTH)
    #verifica se o jogo acabou
    the_board.print_board()
    if the_board.is_terminal_state():
        return (-1, -1)
    #faz a jogada
    else:
        acao = min_max.run()
        return acao

def modified_sigmoid(x):
    return 1/(1+math.e**(-((x/(4))-5)))

def inverse_modified_sigmoid(x):
    """
    starts at 1 and goes to 0
    """
    return 1/(1+math.e**(((x/(4))-6)))
'''
Minhas Notas:
Recebe um tabuleiro e uma cor e retorna um movimento
Um movimento é uma tupla com dois inteiros com valores entre 0 e 7
Caso não haja movimento valido, retorna a tupla -1, -1
O primeiro inteiro é a coluna e o segundo a linha
'''

o = board.Board()
print(make_move(o, 'W'))