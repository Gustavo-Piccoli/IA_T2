
from advsearch.othello.board import Board
class Node:
    def __init__(self,board,color,alpha,beta,depth,parent, move, successors = None,value =None):
        self.board:Board = board
        self.color = color
        self.alpha = alpha
        self.beta = beta
        self.depth = depth
        self.parent = parent
        self.move = move
        self.successors:list = successors
        self.value = value