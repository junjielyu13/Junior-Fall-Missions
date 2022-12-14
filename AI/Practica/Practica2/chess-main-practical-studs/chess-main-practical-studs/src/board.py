import piece
import numpy as np
import random


class Board():
    """
    A class to represent a chess board.

    ...

    Attributes:
    -----------
    board : list[list[Piece]]
        represents a chess board

    turn : bool
        True if white's turn

    white_ghost_piece : tup
        The coordinates of a white ghost piece representing a takeable pawn for en passant

    black_ghost_piece : tup
        The coordinates of a black ghost piece representing a takeable pawn for en passant

    Methods:
    --------
    print_board() -> None
        Prints the current configuration of the board

    move(start:tup, to:tup) -> None
        Moves the piece at `start` to `to` if possible. Otherwise, does nothing.

    """

    def __init__(self, initState, xinit=True):

        # initstate
        # matrix 8x8
        """
        Initializes the board per standard chess rules
        """
        self.listNames = ['P', 'R', 'H', 'B', 'Q', 'K', 
                          'P', 'R', 'H', 'B', 'Q', 'K']

        self.listSuccessorStates = []
        self.listNextStates = []

        self.board = []

        self.currentStateW = []  # actuali current state
        self.currentStateB = []

        self.listVisitedStates = []

        # Board set-up
        for i in range(8):
            self.board.append([None] * 8)

        # assign pieces
        if xinit:

            # White
            self.board[7][0] = piece.Rook(True)
            self.board[7][1] = piece.Knight(True)
            self.board[7][2] = piece.Bishop(True)
            self.board[7][3] = piece.Queen(True)
            self.board[7][4] = piece.King(True)
            self.board[7][5] = piece.Bishop(True)
            self.board[7][6] = piece.Knight(True)
            self.board[7][7] = piece.Rook(True)

            for i in range(8):
                self.board[6][i] = piece.Pawn(True)

            # Black
            self.board[0][0] = piece.Rook(False)
            self.board[0][1] = piece.Knight(False)
            self.board[0][2] = piece.Bishop(False)
            self.board[0][3] = piece.Queen(False)
            self.board[0][4] = piece.King(False)
            self.board[0][5] = piece.Bishop(False)
            self.board[0][6] = piece.Knight(False)
            self.board[0][7] = piece.Rook(False)

            for i in range(8):
                self.board[1][i] = piece.Pawn(False)

        # assign pieces
        else:

            self.currentState = initState

            # assign pieces
            for i in range(8):
                for j in range(8):

                    # White
                    if initState[i][j] == 1:
                        self.board[i][j] = piece.Pawn(True)
                        # assign AI State

                    elif initState[i][j] == 2:
                        self.board[i][j] = piece.Rook(True)
                    elif initState[i][j] == 3:
                        self.board[i][j] = piece.Knight(True)
                    elif initState[i][j] == 4:
                        self.board[i][j] = piece.Bishop(True)
                    elif initState[i][j] == 5:
                        self.board[i][j] = piece.Queen(True)
                    elif initState[i][j] == 6:
                        self.board[i][j] = piece.King(True)
                    # Blacks
                    elif initState[i][j] == 7:
                        self.board[i][j] = piece.Pawn(False)
                    elif initState[i][j] == 8:
                        self.board[i][j] = piece.Rook(False)
                    elif initState[i][j] == 9:
                        self.board[i][j] = piece.Knight(False)
                    elif initState[i][j] == 10:
                        self.board[i][j] = piece.Bishop(False)
                    elif initState[i][j] == 11:
                        self.board[i][j] = piece.Queen(False)
                    elif initState[i][j] == 12:
                        self.board[i][j] = piece.King(False)

                    # store current state (Whites)
                    if (initState[i][j] > 0 and initState[i][j] < 7):
                        self.currentStateW.append([i, j, int(initState[i][j])])

                    # target state (Blacks)
                    if initState[i][j] > 6 and initState[i][j] > 7:
                        self.currentStateB.append([i, j, int(initState[i][j])])





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




    def getListNextStatesW(self, mypieces):
        """
        Gets the list of next possible states given the currentStateW
        for each kind of piece
        """

        self.listNextStates = []

        for j in range(len(mypieces)):

            self.listSuccessorStates = []

            mypiece = mypieces[j]
            listOtherPieces = mypieces.copy()
            listOtherPieces.remove(mypiece)

            listPotentialNextStates = []


            if mypiece[2] == 6:
                listPotentialNextStates = [
                                            [mypiece[0] - 1, mypiece[1],     6], 
                                            [mypiece[0] - 1, mypiece[1] + 1, 6],
                                            [mypiece[0] - 1, mypiece[1] - 1, 6],
                                            [mypiece[0],     mypiece[1] - 1, 6],
                                            [mypiece[0],     mypiece[1] + 1, 6], 
                                            [mypiece[0] + 1, mypiece[1] - 1, 6], 
                                            [mypiece[0] + 1, mypiece[1] + 1, 6],
                                            [mypiece[0] + 1, mypiece[1],     6]
                                           ]
                # check they are empty
                for k in range(len(listPotentialNextStates)):
                    aa = listPotentialNextStates[k]
                    if (aa[0] > -1 and aa[0] < 8 and aa[1] > -1 and aa[1] < 8 
                        and listPotentialNextStates[k] not in self.currentStateW):

                        if ((self.board[aa[0]][aa[1]] == None) or 
                            (self.board[aa[0]][aa[1]] != None and 
                             self.board[mypiece[0]][mypiece[1]] != None and 
                             self.board[aa[0]][aa[1]].color != self.board[mypiece[0]][mypiece[1]].color)
                            ):
                            self.listSuccessorStates.append([aa[0], aa[1], aa[2]])

            elif mypiece[2] == 2:
                listPotentialNextStates = []

                ix = mypiece[0]
                iy = mypiece[1]
                while (ix < 7):
                    ix = ix + 1
                    if self.board[ix][iy] != None and self.board[mypiece[0]][mypiece[1]] != None and self.board[ix][iy].color != self.board[mypiece[0]][mypiece[1]].color:
                        listPotentialNextStates.append([ix, iy, 2])
                        break
                    elif self.board[ix][iy] != None and self.board[mypiece[0]][mypiece[1]] != None and self.board[ix][iy].color == self.board[mypiece[0]][mypiece[1]].color:
                        break
                    elif self.board[ix][iy] == None:
                        listPotentialNextStates.append([ix, iy, 2])

                ix = mypiece[0]
                iy = mypiece[1]
                while (ix > 0):
                    ix = ix - 1
                    if self.board[ix][iy] != None and self.board[mypiece[0]][mypiece[1]] != None and self.board[ix][iy].color != self.board[mypiece[0]][mypiece[1]].color:
                        listPotentialNextStates.append([ix, iy, 2])
                        break
                    elif self.board[ix][iy] != None and self.board[mypiece[0]][mypiece[1]] != None and self.board[ix][iy].color == self.board[mypiece[0]][mypiece[1]].color:
                        break
                    elif self.board[ix][iy] == None:
                        listPotentialNextStates.append([ix, iy, 2])


                ix = mypiece[0]
                iy = mypiece[1]
                while (iy < 7):
                    iy = iy + 1
                    if self.board[ix][iy] != None and self.board[mypiece[0]][mypiece[1]] != None and self.board[ix][iy].color != self.board[mypiece[0]][mypiece[1]].color:
                        listPotentialNextStates.append([ix, iy, 2])
                        break
                    elif self.board[ix][iy] != None and self.board[mypiece[0]][mypiece[1]] != None and self.board[ix][iy].color == self.board[mypiece[0]][mypiece[1]].color:
                        break
                    elif self.board[ix][iy] == None:
                        listPotentialNextStates.append([ix, iy, 2])

                ix = mypiece[0]
                iy = mypiece[1]
                while (iy > 0):
                    iy = iy - 1
                    if self.board[ix][iy] != None and self.board[mypiece[0]][mypiece[1]] != None and self.board[ix][iy].color != self.board[mypiece[0]][mypiece[1]].color:
                        listPotentialNextStates.append([ix, iy, 2])
                        break
                    elif self.board[ix][iy] != None and self.board[mypiece[0]][mypiece[1]] != None and self.board[ix][iy].color == self.board[mypiece[0]][mypiece[1]].color:
                        break
                    elif self.board[ix][iy] == None:
                        listPotentialNextStates.append([ix, iy, 2])



                # check positions are not occupied - so far cannot kill pieces
                listPotentialNextStates
                for k in range(len(listPotentialNextStates)):
                    if listPotentialNextStates[k] not in listOtherPieces and listPotentialNextStates[k]:
                        self.listSuccessorStates.append(listPotentialNextStates[k])
                  



            # add other state pieces
            for k in range(len(self.listSuccessorStates)):
                self.listNextStates.append([self.listSuccessorStates[k]]+listOtherPieces)
            



    def getListNextStatesB(self, mypieces):

        """
        Gets the list of next possible states given the currentStateB
        for each kind of piece
        """

        self.listNextStates = []


        for j in range(len(mypieces)):

            self.listSuccessorStates = []

            mypiece = mypieces[j]
            listOtherPieces = mypieces.copy()
            listOtherPieces.remove(mypiece)

            listPotentialNextStates = []

            
            if mypiece[2] == 12:
                listPotentialNextStates = [
                                           [mypiece[0] - 1, mypiece[1] + 1, 12],
                                           [mypiece[0] - 1, mypiece[1] - 1, 12],
                                           [mypiece[0] - 1, mypiece[1],     12],
                                           [mypiece[0] + 1, mypiece[1],     12],
                                           [mypiece[0] + 1, mypiece[1] + 1, 12],
                                           [mypiece[0] + 1, mypiece[1] - 1, 12], 
                                           [mypiece[0],     mypiece[1] - 1, 12],
                                           [mypiece[0],     mypiece[1] + 1, 12] 
                                          ]

                # check they are empty
                for k in range(len(listPotentialNextStates)):

                    aa = listPotentialNextStates[k]
                    if (aa[0] > -1 and aa[0] < 8 and aa[1] > -1 and aa[1] < 8 and listPotentialNextStates[k] not in self.currentStateB):
                        if ((self.board[aa[0]][aa[1]] == None) or 
                            (self.board[aa[0]][aa[1]] != None and 
                             self.board[mypiece[0]][mypiece[1]] != None and 
                             self.board[aa[0]][aa[1]].color != self.board[mypiece[0]][mypiece[1]].color)
                            ):

                            self.listSuccessorStates.append([aa[0], aa[1], aa[2]])


            elif mypiece[2] == 8:
                listPotentialNextStates = []

                ix = mypiece[0]
                iy = mypiece[1]
                while (ix < 7):
                    ix = ix + 1
                    if self.board[ix][iy] != None  and   self.board[mypiece[0]][mypiece[1]] != None and self.board[ix][iy].color != self.board[mypiece[0]][mypiece[1]].color:
                        listPotentialNextStates.append([ix, iy, 8])
                        break
                    elif self.board[ix][iy] != None  and   self.board[mypiece[0]][mypiece[1]] != None and self.board[ix][iy].color == self.board[mypiece[0]][mypiece[1]].color:
                        break
                    elif self.board[ix][iy] == None:
                        listPotentialNextStates.append([ix, iy, 8])

                ix = mypiece[0]
                iy = mypiece[1]
                while (ix > 0):
                    ix = ix - 1
                    if self.board[ix][iy] != None and self.board[mypiece[0]][mypiece[1]] != None and self.board[ix][iy].color != self.board[mypiece[0]][mypiece[1]].color:
                        listPotentialNextStates.append([ix, iy, 8])
                        break
                    elif self.board[ix][iy] != None and self.board[mypiece[0]][mypiece[1]] != None and self.board[ix][iy].color == self.board[mypiece[0]][mypiece[1]].color:
                        break
                    elif self.board[ix][iy] == None:
                        listPotentialNextStates.append([ix, iy, 8])

                ix = mypiece[0]
                iy = mypiece[1]
                while (iy < 7):
                    iy = iy + 1
                    if self.board[ix][iy] != None and self.board[mypiece[0]][mypiece[1]] != None and self.board[ix][iy].color != self.board[mypiece[0]][mypiece[1]].color:
                        listPotentialNextStates.append([ix, iy, 8])
                        break
                    elif self.board[ix][iy] != None and self.board[mypiece[0]][mypiece[1]] != None and self.board[ix][iy].color == self.board[mypiece[0]][mypiece[1]].color:
                        break
                    elif self.board[ix][iy] == None:
                        listPotentialNextStates.append([ix, iy, 8])

                ix = mypiece[0]
                iy = mypiece[1]
                while (iy > 0):
                    iy = iy - 1
                    if self.board[ix][iy] != None and self.board[mypiece[0]][mypiece[1]] != None and self.board[ix][iy].color != self.board[mypiece[0]][mypiece[1]].color:
                        listPotentialNextStates.append([ix, iy, 8])
                        break
                    elif self.board[ix][iy] != None and self.board[mypiece[0]][mypiece[1]] != None and self.board[ix][iy].color == self.board[mypiece[0]][mypiece[1]].color:
                        break
                    elif self.board[ix][iy] == None:
                        listPotentialNextStates.append([ix, iy, 8])


                # check positions are not occupied - so far cannot kill pieces
                listPotentialNextStates
                for k in range(len(listPotentialNextStates)):
                    if listPotentialNextStates[k] not in listOtherPieces and listPotentialNextStates[k]:
                        self.listSuccessorStates.append(listPotentialNextStates[k])


            # add other state pieces
            for k in range(len(self.listSuccessorStates)):
                self.listNextStates.append([self.listSuccessorStates[k]]+listOtherPieces)


        

    def __eq__(self, board) -> bool:

        for i in range(8):
            for j in range(8):
                if self.board[i][j] != None  and board.board[i][j] == None:
                    return False
                elif self.board[i][j] == None  and board.board[i][j] != None:
                    return False
                elif self.board[i][j] != None  and board.board[i][j] != None and self.board[i][j].pieceNum != board.board[i][j].pieceNum:
                    return False
        return True




    def print_board(self):
        """
        Prints the current state of the board.
        """
        boardrow = 8
        buffer = "[0] "
        for i in range(33):
            buffer += "*"
        print(buffer)
        for i in range(len(self.board)):
            tmp_str = f"{boardrow} {i} |"
            for j in self.board[i]:
                if j == None or j.name == 'GP':
                    tmp_str += "   |"
                elif len(j.name) == 2:
                    tmp_str += (" " + str(j) + "|")
                else:
                    tmp_str += (" " + str(j) + " |")
            print(tmp_str)
            boardrow -= 1
        buffer = "    "
        for i in range(33):
            buffer += "*"
        print(buffer)
        buffer = "    "
        for i in range(8):
            buffer += f"  {i} "
        buffer += "  [1]"
        print(buffer)
        print("      A   B   C   D   E   F   G   H")





        