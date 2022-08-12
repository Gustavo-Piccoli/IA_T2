
import math
from advsearch.perry_o_ornitorrinco.heuristic import Heuristic
from advsearch.othello.board import Board
from advsearch.perry_o_ornitorrinco.node import Node

class My_Heuristic(Heuristic):
    
    def __init__(self,agent_color):
        self.agent_color = agent_color
        if agent_color == Board.WHITE:
            self.opponent_color = Board.BLACK
        else:
            self.opponent_color = Board.WHITE

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
        count=0
        for move in my_board.legal_moves(my_board.opponent(color)):
            #se com um movimento vai para um canto
            if move[0] in [0,7] and move[1] in [0,7]:
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

    def x_square_occupied(self,my_board:Board,color):
        count=0
        if my_board.tiles[1][1] == color and my_board.tiles[0][0]  == '.':
            count+=1
        if my_board.tiles[1][6] == color and my_board.tiles[0][7] == '.':
            count+=1
        if my_board.tiles[6][1] == color and my_board.tiles[7][0] == '.':
            count+=1
        if my_board.tiles[6][6] == color and my_board.tiles[7][7] == '.':
            count+=1
        return count


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

    def long_frontier_sequence_penalty(self,my_board:Board,color):
        line1 = 0
        line6 = 0
        column1 = 0
        column6 = 0

        max_sequence1 = 0
        max_sequence6 = 0

        long_seq = 2
        for j in range(8):
            if my_board.tiles[1][j] == color:
                line1+=1
            else:
                if line1>long_seq:
                    max_sequence1 = max(line1,max_sequence1)
                line1 = 0

            if my_board.tiles[6][j] == color:
                line6+=1
            else:
                if line6>long_seq:
                    max_sequence6 =  max(line6,max_sequence6)
                line6 = 0
        line1 = max_sequence1
        line6 = max_sequence6
        for i in range(8):
            if my_board.tiles[i][1] == color:
                column1+=1
            else:
                if column1>long_seq:
                    max_sequence1 = max(column1,max_sequence1)
                column1 = 0

            if my_board.tiles[i][6] == color:
                column6+=1
            else:
                if column6>long_seq:
                    max_sequence6 =  max(column6,max_sequence6)
                column6 = 0    
        column1 = max_sequence1
        column6 = max_sequence6

        return -(line1 + line6 + column1 + column6)

    def get_state_value(self,node:Node):
        """
        get value for node
        """
    
        pieces_in_center = self.num_center_pieces(node.board,self.agent_color)
        pieces_value = node.board.num_pieces(self.agent_color)  - node.board.num_pieces(self.opponent_color)  
        number_of_pieces_placed  = node.board.num_pieces(self.agent_color) + node.board.num_pieces(self.opponent_color)
        opp_legal_moves_value = len(node.board.legal_moves(self.opponent_color))
        agent_legal_moves_value = len(node.board.legal_moves(self.agent_color))
        agent_corners = self.get_num_corners(node.board,self.agent_color) 
        opp_corners = self.get_num_corners(node.board,self.opponent_color) 
        num_corner_risk  = self.get_num_corners_at_risk(node.board,self.agent_color)

        outer_pieces = self.get_num_of_outer_pieces(node.board,self.agent_color) 
        long_frontier_seq_penalty = self.long_frontier_sequence_penalty(node.board,self.agent_color) 
        
        if node.parent == None:
            placed_on_xsquare = 0
        else:
            placed_on_xsquare = self.x_square_occupied(node.board,self.agent_color) - self.x_square_occupied(node.parent.board,self.agent_color)
        
        w_xsquare = -100
        w_corner_risk = -15
        w_opp_legal_moves = -0.7 
        w_agent_corner = 30
        w_opp_corner = -30
        w_pieces = 2*self.modified_sigmoid(number_of_pieces_placed)
        w_pieces_in_center = self.inverse_modified_sigmoid(number_of_pieces_placed)
        w_outer_pieces = 0.35
        w_agent_moves = 1
        return w_pieces*pieces_value + opp_legal_moves_value*w_opp_legal_moves \
            + agent_legal_moves_value*w_agent_moves + agent_corners*w_agent_corner + opp_corners*w_opp_corner \
            + num_corner_risk*w_corner_risk +pieces_in_center*w_pieces_in_center + outer_pieces*w_outer_pieces  + long_frontier_seq_penalty \
            + w_xsquare*placed_on_xsquare
    
    def modified_sigmoid(self,x):
        return 1/(1+math.e**(-((x/(4))-5)))

    def inverse_modified_sigmoid(self,x):
        """
        starts at 1 and goes to 0
        """
        return 1/(1+math.e**(((x/(5))-6)))