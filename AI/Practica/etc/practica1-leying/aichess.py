<<<<<<< HEAD
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 11:22:03 2022

@author: ignasi
"""

import chess
import numpy as np
import sys
import queue

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
        self.currentStateW = self.chess.boardSim.currentStateW;
        self.depthMax = 8;
        self.checkMate = False
        self.checkmateStates = [[[0, 0, 2], [2, 4, 6]], [[0, 1, 2], [2, 4, 6]], [[0, 2, 2], [2, 4, 6]], [[0, 3, 2],
                               [2, 4, 6]],[[0, 5, 2], [2, 4, 6]], [[0, 6, 2], [2, 4, 6]], [[0, 7, 2], [2, 4, 6]]]


    def getCurrentState(self):
    
        return self.myCurrentStateW
    
    
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
    
        if (len(self.listVisitedStates)>0):
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
        for state in self.checkmateStates:
            state1 = state[0]
            state2 = state[1]
            if (mystate[0] == state1 and mystate[1] == state2) or (mystate[0] == state2 and mystate[1] == state1):
                print("Checkmate")
                return True

        return False

    def DepthFirstSearch(self, currentState, depth):
        """
        Check mate from currentStateW through DFS backtracking
        """

        #save the temporary result
        self.pathToTarget = [currentState]
        result = []

        def is_better_solution(result,depth):
            """
            returns if current result is better solution than the one before
            Args:
                result: list[list]
                depth: int

            Returns:
                True: better solution
                False: not a better solution
            """

            return False

        def dfs_backtracking(currentState,depth,result):
            #base cases:
            #1.Finish when check-mate
            #2.Finish when have check all possibilities

            #1. We managed to reach checkmate state
            if self.isCheckMate(currentState):
                print('result:',result)
                return True

            # iterate all possible states from currentState (won't stop if we find the first solution)
            for state in self.getListNextStatesW(currentState):
                # state not visited yet
                if not self.isVisited(state):
                    self.listVisitedStates.append(state)
                    result.append(state)
                    #check-mate
                    if dfs_backtracking(state,depth+1,result):
                        # check if we found a better solution
                        if is_better_solution(result,depth+1):
                            # update pathToTarget
                            self.pathToTarget = result
                            print("Better check-mate")

                    #backtracking
                    result.pop()
                    self.listVisitedStates.pop()

            #2. We have iterated through all the possibilities and still can't find check-mate state
            print("Check-mate is not possible")
            return False

        return dfs_backtracking(currentState,depth,result)


    def BreadthFirstSearch(self, currentState, depth):
        """
        Check mate from currentStateW through BFS
        """

        '''
        tests
        
        state = [[7, 0, 2], [7, 4, 6]]
        print("nextStates of [[7, 0, 2], [7, 4, 6]]: ", self.getListNextStatesW(state))
        state1 = [[6, 0, 2], [7, 4, 6]]
        print("nextStates of [[6, 0, 2], [7, 4, 6]]: ", self.getListNextStatesW(state1))
        state2 = [[7, 3, 6], [6, 0, 2]]
        print("nextStates of [[7, 3, 6], [6, 0, 2]]:", self.getListNextStatesW(state2))
        '''

        def is_better_solution(result, depth):
            """
            returns if current result is better solution than the one before
            Args:
                result: list[list]
                depth: int

            Returns:
                True: better solution
                False: not a better solution
            """

            return False

        # create a stack called queue
        queue = []
        queue.append(currentState)
        self.listVisitedStates.append(currentState)


        while queue:
            state = queue.pop()

            # check if there are check-mate
            if self.isCheckMate(state):
                # check if this is a better solution
                if is_better_solution(state,depth):
                    print("better solution")
                    #build pathToTarget
                    #.....
                    #....

            nextStates = self.getListNextStatesW(state)
            for nextState in nextStates:
                if nextState not in self.listVisitedStates:
                    queue.append(nextState)
                    self.listVisitedStates.append(nextState)

    def compute_manhattan(self,current, next):
        """
        returns the manhattan distance beetween current state and next state
        Args:
            current:
            next:

        Returns:
            manhattan distance (int)
        """
        # formula per calcular manhattan distance:
        '''
        a = [x1,y1]
        b = [x2,y2]

        return abs(x1 -x2) + abs(y1 -y2)

        '''
        # aplicar para states?

        x1 = current[0][0]
        y1 = current[0][1]
        x2 = next[1][0]
        y2 = next[1][1]

        print('x1:', x1)
        print('y1:', y1)
        print('x2:', x2)
        print('y2:', y2)

        return abs(x1 - x2) + abs(y1 - y2)

    def AStarSearch(self,currentState):
        """
        Check mate from currentStateW through A*
        Args:
            currentState:
            depth:

        Returns:

        """


        def rebuild_path(came_from):
            """
            function that rebuild pathToTarget through came_from dict
            Args:
                came_from: dict() list of succesors
            """

        frontier = queue.PriorityQueue()
        frontier.put(currentState,0)

        # dict: the path we currently following
        came_from = {}
        # dict: current cost
        cost_so_far = {}
        came_from[currentState] = None
        cost_so_far[currentState] = 0

        while not frontier.empty():
            # get the current state
            # we will get the one with the minimum cost
            current = frontier.get()

            if self.isCheckMate(current):
                break

            for next in self.getListNextStatesW(current):
                # the new cost will be the cost we have spent to get to this point +
                # the cost we will probably spend applying the formula to calculate the manhattan distance
                # ------- no se si el manhattan se añade aqui, o despues?? !!!!!!!!!!!!!!-----------------
                new_cost = cost_so_far[current] + self.compute_manhattan(current,next)
                #if it has not been visited or the cost is lower than before
                if next not in cost_so_far or new_cost < cost_so_far[next]: # next already in cost_so_far, this one will probably lower
                    # put to our priority queue
                    frontier.put(next,priority)
                    # and its cost will be el cost que acabem de calcular
                    priority = new_cost + self.compute_manhattan(current, next)
                    # add to came from, to then rebuild the path list
                    came_from[next] = current

        rebuild_path(came_from)
        print("Done")

    def tests(self, currentState):
        '''
        if self.isCheckMate(currentState):
            return True
        return False

        print("nextStates of [[0, 0, 2], [7, 4, 6]]: ", self.getListNextStatesW(state))

        '''
        state = [[7, 0, 2], [7, 4, 6]]
        state1 = [[0,0,2],[7,4,6]]
        manhattan = self.compute_manhattan(state,state1)
        print('the manhatan distance is:',manhattan)
            

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


def get_board_details():

    # get list of next states for current state
    print("current State",currentState)

    # it uses board to get them... careful
    aichess.getListNextStatesW(currentState)
    print("list next states ", aichess.pathToTarget)

    # starting from current state find the end state (check mate) - recursive function
    # find the shortest path, initial depth 0
    depth = 0
    aichess.DepthFirstSearch(currentState, depth)
    print("DFS End")

    # example move piece from start to end state
    MovesToMake = ['1e', '2e']
    print("start: ", MovesToMake[0])
    print("to: ", MovesToMake[1])

    start = translate(MovesToMake[0])
    to = translate(MovesToMake[1])

    print("start: ", start)
    print("to: ", to)

    aichess.chess.moveSim(start, to)

    aichess.chess.boardSim.print_board()
    print("#Move sequence...  ", aichess.pathToTarget)
    print("#Visited sequence...  ", aichess.listVisitedStates)

    print("#Current State...  ", aichess.chess.board.currentStateW)




if __name__ == "__main__":

 #   if len(sys.argv) < 2:
 #       sys.exit(usage())

    # intiialize board
    TA = np.zeros((8, 8))
    TA[7][0] = 2
    TA[7][4] = 6
    TA[0][4] = 12

    # initialise board
    print("stating AI chess... ")
    aichess = Aichess(TA, True)
    currentState = aichess.chess.board.currentStateW.copy()

    print("printing board")
    aichess.chess.boardSim.print_board()

    depth = 0
    #aichess.DepthFirstSearch(currentState, depth)
    print("DFS End")

    #aichess.BreadthFirstSearch(currentState, depth)
    print("BFS End")

    #aichess.AStarSearch(currentState)
    print("A* End")

    print("isCheckMate ?", aichess.tests([[2, 4, 6],[0, 0, 2]]))
=======
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 11:22:03 2022

@author: ignasi
"""

import chess
import numpy as np
import sys
import queue

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
        self.currentStateW = self.chess.boardSim.currentStateW;
        self.depthMax = 8;
        self.checkMate = False
        self.checkmateStates = [[[0, 0, 2], [2, 4, 6]], [[0, 1, 2], [2, 4, 6]], [[0, 2, 2], [2, 4, 6]], [[0, 3, 2],
                               [2, 4, 6]],[[0, 5, 2], [2, 4, 6]], [[0, 6, 2], [2, 4, 6]], [[0, 7, 2], [2, 4, 6]]]


    def getCurrentState(self):
    
        return self.myCurrentStateW
    
    
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
    
        if (len(self.listVisitedStates)>0):
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
        for state in self.checkmateStates:
            state1 = state[0]
            state2 = state[1]
            if (mystate[0] == state1 and mystate[1] == state2) or (mystate[0] == state2 and mystate[1] == state1):
                print("Checkmate")
                return True

        return False

    def DepthFirstSearch(self, currentState, depth):
        """
        Check mate from currentStateW through DFS backtracking
        """

        #save the temporary result
        self.pathToTarget = [currentState]
        result = []

        def is_better_solution(result,depth):
            """
            returns if current result is better solution than the one before
            Args:
                result: list[list]
                depth: int

            Returns:
                True: better solution
                False: not a better solution
            """

            return False

        def dfs_backtracking(currentState,depth,result):
            #base cases:
            #1.Finish when check-mate
            #2.Finish when have check all possibilities

            #1. We managed to reach checkmate state
            if self.isCheckMate(currentState):
                print('result:',result)
                return True

            # iterate all possible states from currentState (won't stop if we find the first solution)
            for state in self.getListNextStatesW(currentState):
                # state not visited yet
                if not self.isVisited(state):
                    self.listVisitedStates.append(state)
                    result.append(state)
                    #check-mate
                    if dfs_backtracking(state,depth+1,result):
                        # check if we found a better solution
                        if is_better_solution(result,depth+1):
                            # update pathToTarget
                            self.pathToTarget = result
                            print("Better check-mate")

                    #backtracking
                    result.pop()
                    self.listVisitedStates.pop()

            #2. We have iterated through all the possibilities and still can't find check-mate state
            print("Check-mate is not possible")
            return False

        return dfs_backtracking(currentState,depth,result)


    def BreadthFirstSearch(self, currentState, depth):
        """
        Check mate from currentStateW through BFS
        """

        '''
        tests
        
        state = [[7, 0, 2], [7, 4, 6]]
        print("nextStates of [[7, 0, 2], [7, 4, 6]]: ", self.getListNextStatesW(state))
        state1 = [[6, 0, 2], [7, 4, 6]]
        print("nextStates of [[6, 0, 2], [7, 4, 6]]: ", self.getListNextStatesW(state1))
        state2 = [[7, 3, 6], [6, 0, 2]]
        print("nextStates of [[7, 3, 6], [6, 0, 2]]:", self.getListNextStatesW(state2))
        '''

        def is_better_solution(result, depth):
            """
            returns if current result is better solution than the one before
            Args:
                result: list[list]
                depth: int

            Returns:
                True: better solution
                False: not a better solution
            """

            return False

        # create a stack called queue
        queue = []
        queue.append(currentState)
        self.listVisitedStates.append(currentState)


        while queue:
            state = queue.pop()

            # check if there are check-mate
            if self.isCheckMate(state):
                # check if this is a better solution
                if is_better_solution(state,depth):
                    print("better solution")
                    #build pathToTarget
                    #.....
                    #....

            nextStates = self.getListNextStatesW(state)
            for nextState in nextStates:
                if nextState not in self.listVisitedStates:
                    queue.append(nextState)
                    self.listVisitedStates.append(nextState)

    def compute_manhattan(self,current, next):
        """
        returns the manhattan distance beetween current state and next state
        Args:
            current:
            next:

        Returns:
            manhattan distance (int)
        """
        # formula per calcular manhattan distance:
        '''
        a = [x1,y1]
        b = [x2,y2]

        return abs(x1 -x2) + abs(y1 -y2)

        '''
        # aplicar para states?

        x1 = current[0][0]
        y1 = current[0][1]
        x2 = next[1][0]
        y2 = next[1][1]

        print('x1:', x1)
        print('y1:', y1)
        print('x2:', x2)
        print('y2:', y2)

        return abs(x1 - x2) + abs(y1 - y2)

    def AStarSearch(self,currentState):
        """
        Check mate from currentStateW through A*
        Args:
            currentState:
            depth:

        Returns:

        """


        def rebuild_path(came_from):
            """
            function that rebuild pathToTarget through came_from dict
            Args:
                came_from: dict() list of succesors
            """

        frontier = queue.PriorityQueue()
        frontier.put(currentState,0)

        # dict: the path we currently following
        came_from = {}
        # dict: current cost
        cost_so_far = {}
        came_from[currentState] = None
        cost_so_far[currentState] = 0

        while not frontier.empty():
            # get the current state
            # we will get the one with the minimum cost
            current = frontier.get()

            if self.isCheckMate(current):
                break

            for next in self.getListNextStatesW(current):
                # the new cost will be the cost we have spent to get to this point +
                # the cost we will probably spend applying the formula to calculate the manhattan distance
                # ------- no se si el manhattan se añade aqui, o despues?? !!!!!!!!!!!!!!-----------------
                new_cost = cost_so_far[current] + self.compute_manhattan(current,next)
                #if it has not been visited or the cost is lower than before
                if next not in cost_so_far or new_cost < cost_so_far[next]: # next already in cost_so_far, this one will probably lower
                    # put to our priority queue
                    frontier.put(next,priority)
                    # and its cost will be el cost que acabem de calcular
                    priority = new_cost + self.compute_manhattan(current, next)
                    # add to came from, to then rebuild the path list
                    came_from[next] = current

        rebuild_path(came_from)
        print("Done")

    def tests(self, currentState):
        '''
        if self.isCheckMate(currentState):
            return True
        return False

        print("nextStates of [[0, 0, 2], [7, 4, 6]]: ", self.getListNextStatesW(state))

        '''
        state = [[7, 0, 2], [7, 4, 6]]
        state1 = [[0,0,2],[7,4,6]]
        manhattan = self.compute_manhattan(state,state1)
        print('the manhatan distance is:',manhattan)
            

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


def get_board_details():

    # get list of next states for current state
    print("current State",currentState)

    # it uses board to get them... careful
    aichess.getListNextStatesW(currentState)
    print("list next states ", aichess.pathToTarget)

    # starting from current state find the end state (check mate) - recursive function
    # find the shortest path, initial depth 0
    depth = 0
    aichess.DepthFirstSearch(currentState, depth)
    print("DFS End")

    # example move piece from start to end state
    MovesToMake = ['1e', '2e']
    print("start: ", MovesToMake[0])
    print("to: ", MovesToMake[1])

    start = translate(MovesToMake[0])
    to = translate(MovesToMake[1])

    print("start: ", start)
    print("to: ", to)

    aichess.chess.moveSim(start, to)

    aichess.chess.boardSim.print_board()
    print("#Move sequence...  ", aichess.pathToTarget)
    print("#Visited sequence...  ", aichess.listVisitedStates)

    print("#Current State...  ", aichess.chess.board.currentStateW)




if __name__ == "__main__":

 #   if len(sys.argv) < 2:
 #       sys.exit(usage())

    # intiialize board
    TA = np.zeros((8, 8))
    TA[7][0] = 2
    TA[7][4] = 6
    TA[0][4] = 12

    # initialise board
    print("stating AI chess... ")
    aichess = Aichess(TA, True)
    currentState = aichess.chess.board.currentStateW.copy()

    print("printing board")
    aichess.chess.boardSim.print_board()

    depth = 0
    #aichess.DepthFirstSearch(currentState, depth)
    print("DFS End")

    #aichess.BreadthFirstSearch(currentState, depth)
    print("BFS End")

    #aichess.AStarSearch(currentState)
    print("A* End")

    print("isCheckMate ?", aichess.tests([[2, 4, 6],[0, 0, 2]]))
>>>>>>> a21aeee9c027a9b5f159961d1a1ce9fe12aca9ee
