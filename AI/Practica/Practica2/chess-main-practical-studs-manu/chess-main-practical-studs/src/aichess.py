#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 11:22:03 2022

@author: ignasi
"""

import copy
import time

import chess
import numpy as np
import sys
from typing import List

RawStateType = List[List[List[int]]]

from itertools import permutations
from collections import defaultdict
from queue import PriorityQueue, Queue


class Aichess():
    """
    A class to represent the game of chess.
    ...
    Attributes:
    -----------
    chess : Chess
        represents the chess game
    Methods:
    --------
    startGame(pos:stup) -> None
        Promotes a pawn that has reached the other side to another, or the same, piece
    """

    def __init__(self, TA, myinit=True):

        if myinit:
            self.chess = chess.Chess(TA, True)
        else:
            self.chess = chess.Chess([], False)

        self.listNextStates = []
        self.listVisitedStates = []
        self.pathToTarget = []
        self.innitialStateW = self.chess.board.currentStateW
        self.currentStateW = self.chess.boardSim.currentStateW
        self.currentStateB = self.chess.boardSim.currentStateB
        self.checkMate = False

        self.depthMax = 8
        self.path = defaultdict()

        self.paths = {}
        self.paths['path'] = []
        self.paths['visited'] = []


    def getCurrentState(self):
        return self.currentStateW



    def getListNextStatesW(self, myState):
        self.chess.boardSim.getListNextStatesW(myState)
        self.listNextStates = self.chess.boardSim.listNextStates.copy()
        return self.listNextStates



    def isSameState(self, a, b):
        isSameState1 = True
        # a and b are lists
        for k in range(len(a)):
            if a[k] not in b:
                isSameState1 = False

        isSameState2 = True
        # a and b are lists
        for k in range(len(b)):
            if b[k] not in a:
                isSameState2 = False

        isSameState = isSameState1 and isSameState2
        return isSameState



    def isVisited(self, mystate):
        if (len(self.listVisitedStates) > 0):
            perm_state = list(permutations(mystate))

            isVisited = False
            for j in range(len(perm_state)):

                for k in range(len(self.listVisitedStates)):

                    if self.isSameState(list(perm_state[j]), self.listVisitedStates[k]):
                        isVisited = True
            return isVisited
        else:
            return False



    def isCheckMate(self, mystate):
        '''
        Check if is CheckMate

        @param mystate --> list(): 
            current piece on the chessboard

        @return --> bool:
            return true if is Checkmate otherwise false
        '''

        black_king_pos = self.currentStateB[0]                              # Get black King position
        white_rook_pos = mystate[0] if mystate[0][2] == 2 else mystate[1]   # Get white Rook position
        white_king_pos = mystate[1] if mystate[1][2] == 6 else mystate[0]   # Get white King position

        
        if (white_king_pos[1] != black_king_pos[1]) or \
            (white_rook_pos[0] != black_king_pos[0]) or \
            (white_king_pos[0] - 2 != black_king_pos[0]) or \
            (white_rook_pos[1] in {black_king_pos[1]-1, black_king_pos[1], black_king_pos[1]+1}) :
            return False

        return True


    def getPath(self, start, to):
        '''
        Return to finally answer path

        @param innitialState --> list(): 
            start point

        @param finalState --> list(): 
            end point

        @return --> list():
            Path from start to end
        '''

        state = to
        path = list()
        path.append(state)
        while state != start:
            state = self.path[tuple(tuple(piece) for piece in sorted(state))]
            path.append(state)
        return path[::-1]



    def moveOn(self, currentState, nextState):
        '''
        Moves a piece at currentState to nextState
        
        @param currentState --> list()
            Position of a piece to be moved

        @param nextState --> list()
            Position of where the piece is to be moved
        
        @return --> none:
        '''

        start = [e for e in currentState if e not in nextState][0][0:2]
        to = [e for e in nextState if e not in currentState][0][0:2]
        self.chess.moveSim(start, to)
        return





    def DepthFirstSearch(self, currentState, depth):
        '''
        Depth First Search
        
        @param currentState --> list()
            Position of a piece to be moved
        
        @return --> none:
            Generate paths on the way with DFS
        '''

        self.listVisitedStates.append(currentState)     # Add the visited pieces to listVisitedStates
        self.pathToTarget.append(currentState)          # Add the current state to pahtTotaget

        if not self.checkMate:                          # Check if there is no checkmate
            for nextState in self.getListNextStatesW(currentState):

                if self.isCheckMate(nextState):            
                    self.checkMate = True
                    self.pathToTarget.append(nextState)
                    self.listVisitedStates.append(nextState)
                    self.paths['path'] = self.pathToTarget.copy()           # Avoid recall pathToTarget 
                    self.paths['visited'] = self.listVisitedStates.copy()   # Avoid recall listVisitedStates
                    return
                
                elif nextState not in self.listVisitedStates and depth < self.depthMax:
                    self.moveOn(currentState, nextState)        # Move the pawn
                    self.DepthFirstSearch(nextState, depth+1)   # DFS recursion, go to the next depth
                    self.moveOn(nextState, currentState)        # Recall the pawn

                    if len(self.pathToTarget) != 0:
                        self.pathToTarget.pop()             # Recall pathToTarget
                    # if len(self.listVisitedStates) != 0:    # for case of depth 6
                    #     self.listVisitedStates.pop()        # Recall listVisitedStates

        if self.checkMate:                              # Generate final answer path
            self.pathToTarget = copy.copy(self.paths['path'])
            self.listVisitedStates = copy.copy(self.paths['visited'])
            
        return 





    def BreadthFirstSearch(self, currentState):
        '''
        Breadth First Search
        
        @param currentState --> list()
            Position of a piece to be moved
        
        @return --> none:
            Generate paths on the way with BFS
        '''

        queue = Queue()         # BFS we use a queue
        queue.put(currentState) # Add start state to queue

        start_key = tuple(tuple(state) for state in sorted(currentState)) # Generate dict key for start state
        self.path[start_key] = None                                       # the parent state of the current state is none

        while queue:            # There are always pieces in the queue
            state = queue.get()

            if state[0][0:2] != state[1][0:2]: # The following is exactly the same as DFS

                self.listVisitedStates.append(state) 

                if self.isCheckMate(state):
                    self.path[next_key] = state      # Defines the parent state of the current state
                    self.pathToTarget = self.getPath(self.innitialStateW, nextState) 
                    return

                for nextState in self.getListNextStatesW(state):
                    next_key = tuple(tuple(state) for state in sorted(nextState))   # Generate dict key
                    if next_key not in list(self.path.keys()):                      # same as <if not self.isVisited(nextState):> 
                        self.path[next_key] = state                                 # Defines the parent state of the current state
                        queue.put(nextState)                                        # Add the latest found to the queue

        return







    def AStarSearch(self, currentState):
        '''
        AStar Search
        
        @param currentState --> list()
            Position of a piece to be moved
        
        @return --> none:
            Generate paths on the way with A*Search
        '''

        def heuristica(mystate):
            '''
            A* search helper for calculating heuristica values

            @param mystate --> list():
                current state on the board

            @return --> int:
                heuristica value of the current state
            '''

            value = 0

            black_king_pos = self.currentStateB[0]                              # Get Black King position
            white_rook_pos = mystate[0] if mystate[0][2] == 2 else mystate[1]   # Get White Rook Position
            white_king_pos = mystate[1] if mystate[1][2] == 6 else mystate[0]   # Get White King Position

            # value of rook move
            if white_rook_pos[1] in {black_king_pos[1] - 1, black_king_pos[1] + 1} or white_rook_pos[1] == black_king_pos[1]:
                value += 1
            value += 1 if white_rook_pos[0] != 0 else 0 

            #Considering he can move diagonally
            value += max(abs(white_king_pos[1] - black_king_pos[1]), abs((white_king_pos[0] - 2) - black_king_pos[0]))

            return value


        queue = PriorityQueue()                              # A* search we use a PriorityQueue
        queue.put((heuristica(currentState), currentState))  # Add start state to PriorityQueue with him heuristica

        came_from  = defaultdict()                          # keep path of where piece came from for every position that’s been visited and him value
        cost_so_far = defaultdict(lambda : float('inf'))    # keep path of the total movement cost from the start position.

        start_key = tuple(tuple(state) for state in currentState)
        came_from [start_key] = 0                           # the start state is 0
        cost_so_far[start_key] = heuristica(currentState)   


        while not queue.empty():
            state = queue.get()[1]                          #Always get the state with the min heuristica value

            if state[0][0:2] != state[1][0:2]:              
                self.listVisitedStates.append(state)
                for nextState in self.getListNextStatesW(state):
                    
                    if not self.isVisited(nextState):
                        
                        next_key = tuple(tuple(piece) for piece in sorted(nextState))
                        if self.isCheckMate(nextState):
                            self.path[next_key] = state    # Defines the parent state of the current state
                            self.pathToTarget = self.getPath(self.innitialStateW, nextState)
                            return
                            
                        elif cost_so_far[next_key] > came_from [start_key] + 1 + heuristica(nextState): # Update values of came_from and cost_so_far
                            came_from [next_key] = came_from [start_key] + 1                            
                            cost_so_far[next_key] = came_from [next_key] + heuristica(nextState)

                            self.path[next_key] = state    # Defines the parent state of the current state
                            queue.put((cost_so_far[next_key], nextState))   # Add current state to PriorityQueue with new heuristica

        return




def translate(s):
    """
    Translates traditional board coordinates of chess into list indices
    """
    try:
        row = int(s[0])
        col = s[1]
        if row < 1 or row > 8:
            print(s[0] + "is not in the range from 1 - 8")
            return None
        if col < 'a' or col > 'h':
            print(s[1] + "is not in the range from a - h")
            return None
        dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        return (8 - row, dict[col])
    except:
        print(s + "is not in the format '[number][letter]'")
        return None


def movePiece(aichess, currentState, nextState):
    start = [e for e in currentState if e not in nextState][0][0:2]
    to = [e for e in nextState if e not in currentState][0][0:2]
    aichess.chess.move(start, to)
    return

if __name__ == "__main__":
    #   if len(sys.argv) < 2:
    #       sys.exit(usage())

    # intiialize board
    TA = np.zeros((8, 8))
    # white pieces
    # TA[0][0] = 2
    # TA[2][4] = 6
    # # black pieces
    # TA[0][4] = 12

    TA[7][0] = 2
    TA[7][4] = 6
    TA[0][4] = 12
    #TA[0][0] = 8

    # initialise board
    print("stating AI chess... ")
    aichess = Aichess(TA, True)
    currentState = aichess.chess.board.currentStateW.copy()


    aichess_DFS = copy.deepcopy(aichess)
    aichess_BFS = copy.deepcopy(aichess)
    aichess_ASTAR = copy.deepcopy(aichess)


    '''
        DFS TEST
    '''
    print("\n\nstating DFS ... ")
    depth = 0
    aichess_DFS.chess.board.print_board()

    start = time.time()
    aichess_DFS.DepthFirstSearch(currentState, depth)
    end = time.time()

    print("#Move sequence...  ", aichess_DFS.pathToTarget)
    print("#Visited sequence...  ", aichess_DFS.listVisitedStates)
    print("#Current State...  ", aichess_DFS.chess.board.currentStateW)

    startState = aichess_DFS.pathToTarget[0]
    path = aichess_DFS.pathToTarget[1:]
    for nextState in path:
        movePiece(aichess_DFS, startState, nextState)
        startState = nextState
        aichess_DFS.chess.board.print_board()
    print("DFS = ", end - start, "s")




    '''
        BFS TEST
    '''
    print("\n\nstating BFS ... ")
    aichess_BFS.chess.boardSim.print_board()

    start = time.time()
    aichess_BFS.BreadthFirstSearch(currentState)
    end = time.time()

    print("#Move sequence...  ", aichess_BFS.pathToTarget)
    print("#Visited sequence...  ", aichess_BFS.listVisitedStates)
    print("#Current State...  ", aichess_BFS.chess.board.currentStateW)

    startState = aichess_BFS.pathToTarget[0]
    path = aichess_BFS.pathToTarget[1:]
    for nextState in path:
        movePiece(aichess_BFS, startState, nextState)
        startState = nextState
        aichess_BFS.chess.board.print_board()
    print("BFS = ", end - start, "s")
    




    '''
        A* SEARCH TEST
    '''
    print("\n\nstating A* SEARCH ... ")
    aichess_ASTAR.chess.board.print_board()

    start = time.time()
    aichess_ASTAR.AStarSearch(currentState)
    end = time.time()

    print("#Move sequence...  ", aichess_ASTAR.pathToTarget)
    print("#Visited sequence...  ", aichess_ASTAR.listVisitedStates)
    print("#Current State...  ", aichess_ASTAR.chess.board.currentStateW)

    startState = aichess_ASTAR.pathToTarget[0]
    path = aichess_ASTAR.pathToTarget[1:]
    for nextState in path:
        movePiece(aichess_ASTAR, startState, nextState)
        startState = nextState
        aichess_ASTAR.chess.board.print_board()
    print("A* star = ", end - start, "s")