<<<<<<< HEAD
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 11:22:03 2022

@author: ignasi
"""
import copy

import chess
import numpy as np
import sys
import queue
from typing import List

RawStateType = List[List[List[int]]]

from itertools import permutations


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
        self.currentStateW = self.chess.boardSim.currentStateW
        self.innitialState = tuple(tuple(i) for i in sorted(self.currentStateW))
        self.depthMax = 8
        self.checkMate = False
        self.pathDone = False
        self.paths = {}
        self.paths['path'] = []
        self.paths['visited'] = []
        self.checkMateList = [{(0,0,2),(2,4,6)},{(0,1,2),(2,4,6)},{(0,2,2),(2,4,6)},{(0,3,2),(2,4,6)},{(0,5,2),(2,4,6)},{(0,6,2),(2,4,6)},{(0,7,2),(2,4,6)}]

                               
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
        """
        returns True if the current state matches any checkmate state in the checkmate list

        Args:
            mystate: current state of board (list[list])

        Returns:
            True: we are in check mate state
            False: we are not in checkmate state

        """
        if mystate in self.checkMateList:
            return True
        return False

        
    def recorregut(self,veinsVisitats, origin, destination):
        node = destination
        path = []
        while node != origin:
            path.append(node)
            node = veinsVisitats[node]
        path.append(node)
        path.reverse()
        return path

    def makeMove(self,current_state, next_state):
        start = [e for e in current_state if e not in next_state]
        to = [e for e in next_state if e not in current_state]
        start, to = start[0][0:2], to[0][0:2]   
        self.chess.moveSim(start, to) 

    def setify(self, states):
        setStates = set()
        for state in states:
            tup = tuple(state)
            setStates.add(tup)
        return setStates

    def recorregut(self, veinsVisitats, origin, destination): 
        node = destination
        path = []
        while node != origin:
            path.append(node)
            node = veinsVisitats[node]
        path.append(node)
        path.reverse()
        return path

    def DepthFirstSearch(self, currentState, depth):
      
        # Your Code here
        
        self.listVisitedStates.append(currentState)
        self.pathToTarget.append(currentState)
        if not self.checkMate:
            for state in self.getListNextStatesW(currentState):
                set_state = self.setify(state)
                if self.isCheckMate(set_state):
                    self.depthMax = depth
                    self.checkMate = True
                    self.pathDone = True
                    self.pathToTarget.append(state)
                    self.listVisitedStates.append(state)
                    self.paths['path'] = self.pathToTarget.copy()
                    self.paths['visited'] = self.listVisitedStates.copy()
                    return True
                
                elif state in self.listVisitedStates:
                    continue
                elif depth >= self.depthMax:
                    continue
                else:
                    self.makeMove(currentState, state)
                    self.DepthFirstSearch(state, depth+1)
                    self.makeMove(state, currentState)
                    if len(self.pathToTarget) != 0:
                        self.pathToTarget.pop()
                    if len(self.listVisitedStates) != 0:
                        self.listVisitedStates.pop()    
        if self.pathDone:
            self.pathToTarget = copy.copy(self.paths['path'])
            self.listVisitedStates = copy.copy(self.paths['visited'])
            self.currentStateW = self.pathToTarget[-1]
            for i in range(len(self.pathToTarget)):
                j = i+1
                if j < len(self.pathToTarget):
                    self.makeMove(self.pathToTarget[i], self.pathToTarget[j])
            
        return 


 







    def BreadthFirstSearch(self, currentState):
       
        # Your Code here
        
        pass


    def BestFirstSearch(self, currentState):
        
        # Your Code here
        pass    
                
                
    def AStarSearch(self, currentState):
        
        # Your Code here
        pass
        

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

    # initialise board
    print("stating AI chess... ")
    aichess = Aichess(TA, True)
    currentState = aichess.chess.board.currentStateW.copy()
    print("printing board")
    
    print("piece: \nR --> 2 \nK --> 6")

    aichess.chess.boardSim.print_board()

    # get list of next states for current state
    print("current State", currentState)

    # it uses board to get them... careful 
    aichess.getListNextStatesW(currentState)
    #   aichess.getListNextStatesW([[7,4,2],[7,4,6]])
    print("list next states ", aichess.listNextStates)

    # starting from current state find the end state (check mate) - recursive function
    # aichess.chess.boardSim.listVisitedStates = []
    # find the shortest path, initial depth 0

    print("\n\n\nStart game.................\n\n\n")

    depth = 0


    aichess.DepthFirstSearch(currentState, depth)
    # aichess.BreadthFirstSearch(currentState)
    # aichess.BestFirstSearch(currentState)
    # aichess.AStarSearch(currentState)


    # MovesToMake = ['1e','2e','2e','3e','3e','4d','4d','3c']

    # for k in range(int(len(MovesToMake)/2)):

    #     print("k: ",k)

    #     print("start: ",MovesToMake[2*k])
    #     print("to: ",MovesToMake[2*k+1])

    #     start = translate(MovesToMake[2*k])
    #     to = translate(MovesToMake[2*k+1])

    #     print("start: ",start)
    #     print("to: ",to)

    #     aichess.chess.moveSim(start, to)

    aichess.chess.boardSim.print_board()
    print("#Move sequence...  ", aichess.pathToTarget)
    print("#Visited sequence...  ", aichess.listVisitedStates)

    print("#Current State...  ", aichess.currentStateW)

=======
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 11:22:03 2022

@author: ignasi
"""
import copy

import chess
import numpy as np
import sys
import queue
from typing import List

RawStateType = List[List[List[int]]]

from itertools import permutations


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
        self.currentStateW = self.chess.boardSim.currentStateW
        self.innitialState = tuple(tuple(i) for i in sorted(self.currentStateW))
        self.depthMax = 8
        self.checkMate = False
        self.pathDone = False
        self.paths = {}
        self.paths['path'] = []
        self.paths['visited'] = []
        self.checkMateList = [{(0,0,2),(2,4,6)},{(0,1,2),(2,4,6)},{(0,2,2),(2,4,6)},{(0,3,2),(2,4,6)},{(0,5,2),(2,4,6)},{(0,6,2),(2,4,6)},{(0,7,2),(2,4,6)}]

                               
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
        """
        returns True if the current state matches any checkmate state in the checkmate list

        Args:
            mystate: current state of board (list[list])

        Returns:
            True: we are in check mate state
            False: we are not in checkmate state

        """
        if mystate in self.checkMateList:
            return True
        return False

        
    def recorregut(self,veinsVisitats, origin, destination):
        node = destination
        path = []
        while node != origin:
            path.append(node)
            node = veinsVisitats[node]
        path.append(node)
        path.reverse()
        return path

    def makeMove(self,current_state, next_state):
        start = [e for e in current_state if e not in next_state]
        to = [e for e in next_state if e not in current_state]
        start, to = start[0][0:2], to[0][0:2]   
        self.chess.moveSim(start, to) 

    def setify(self, states):
        setStates = set()
        for state in states:
            tup = tuple(state)
            setStates.add(tup)
        return setStates

    def recorregut(self, veinsVisitats, origin, destination): 
        node = destination
        path = []
        while node != origin:
            path.append(node)
            node = veinsVisitats[node]
        path.append(node)
        path.reverse()
        return path

    def DepthFirstSearch(self, currentState, depth):
      
        # Your Code here
        
        self.listVisitedStates.append(currentState)
        self.pathToTarget.append(currentState)
        if not self.checkMate:
            for state in self.getListNextStatesW(currentState):
                set_state = self.setify(state)
                if self.isCheckMate(set_state):
                    self.depthMax = depth
                    self.checkMate = True
                    self.pathDone = True
                    self.pathToTarget.append(state)
                    self.listVisitedStates.append(state)
                    self.paths['path'] = self.pathToTarget.copy()
                    self.paths['visited'] = self.listVisitedStates.copy()
                    return True
                
                elif state in self.listVisitedStates:
                    continue
                elif depth >= self.depthMax:
                    continue
                else:
                    self.makeMove(currentState, state)
                    self.DepthFirstSearch(state, depth+1)
                    self.makeMove(state, currentState)
                    if len(self.pathToTarget) != 0:
                        self.pathToTarget.pop()
                    if len(self.listVisitedStates) != 0:
                        self.listVisitedStates.pop()    
        if self.pathDone:
            self.pathToTarget = copy.copy(self.paths['path'])
            self.listVisitedStates = copy.copy(self.paths['visited'])
            self.currentStateW = self.pathToTarget[-1]
            for i in range(len(self.pathToTarget)):
                j = i+1
                if j < len(self.pathToTarget):
                    self.makeMove(self.pathToTarget[i], self.pathToTarget[j])
            
        return 


 







    def BreadthFirstSearch(self, currentState):
       
        # Your Code here
        
        pass


    def BestFirstSearch(self, currentState):
        
        # Your Code here
        pass    
                
                
    def AStarSearch(self, currentState):
        
        # Your Code here
        pass
        

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

    # initialise board
    print("stating AI chess... ")
    aichess = Aichess(TA, True)
    currentState = aichess.chess.board.currentStateW.copy()
    print("printing board")
    
    print("piece: \nR --> 2 \nK --> 6")

    aichess.chess.boardSim.print_board()

    # get list of next states for current state
    print("current State", currentState)

    # it uses board to get them... careful 
    aichess.getListNextStatesW(currentState)
    #   aichess.getListNextStatesW([[7,4,2],[7,4,6]])
    print("list next states ", aichess.listNextStates)

    # starting from current state find the end state (check mate) - recursive function
    # aichess.chess.boardSim.listVisitedStates = []
    # find the shortest path, initial depth 0

    print("\n\n\nStart game.................\n\n\n")

    depth = 0


    aichess.DepthFirstSearch(currentState, depth)
    # aichess.BreadthFirstSearch(currentState)
    # aichess.BestFirstSearch(currentState)
    # aichess.AStarSearch(currentState)


    # MovesToMake = ['1e','2e','2e','3e','3e','4d','4d','3c']

    # for k in range(int(len(MovesToMake)/2)):

    #     print("k: ",k)

    #     print("start: ",MovesToMake[2*k])
    #     print("to: ",MovesToMake[2*k+1])

    #     start = translate(MovesToMake[2*k])
    #     to = translate(MovesToMake[2*k+1])

    #     print("start: ",start)
    #     print("to: ",to)

    #     aichess.chess.moveSim(start, to)

    aichess.chess.boardSim.print_board()
    print("#Move sequence...  ", aichess.pathToTarget)
    print("#Visited sequence...  ", aichess.listVisitedStates)

    print("#Current State...  ", aichess.currentStateW)

>>>>>>> a21aeee9c027a9b5f159961d1a1ce9fe12aca9ee
