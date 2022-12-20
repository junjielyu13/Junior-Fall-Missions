
import board
import piece
import aichess

from lib import initLogging, logging


import numpy as np
from queue import Queue
import copy


class Chess():

    """
    A class to represent the game of chess.

    ...

    Attributes:
    -----------
    board : Board
        represents the chess board of the game

    turn : bool
        True if white's turn

    white_ghost_piece : tup
        The coordinates of a white ghost piece representing a takeable pawn for en passant

    black_ghost_piece : tup
        The coordinates of a black ghost piece representing a takeable pawn for en passant

    Methods:
    --------
    promote(pos:stup) -> None
        Promotes a pawn that has reached the other side to another, or the same, piece

    move(start:tup, to:tup) -> None
        Moves the piece at `start` to `to` if possible. Otherwise, does nothing.
    """

    def __init__(self, initboard, myinit=True):

        if myinit:
            self.board = board.Board(initboard, False)
            self.boardSim = board.Board(initboard, False)
        else:
            self.board = board.Board([], True)
            self.boardSim = board.Board([], True)

        self.turn = True

        self.whiteTurn = True
        self.whitePlayer = True

        self.white_ghost_piece = None
        self.black_ghost_piece = None


        # AI current state
        self.currentStateW = copy.deepcopy(self.boardSim.currentStateW)
        self.currentStateB = copy.deepcopy(self.boardSim.currentStateB)

        self.innitialStateW = copy.deepcopy(self.boardSim.currentStateW)
        self.innitialStateB = copy.deepcopy(self.boardSim.currentStateB)



    def promotion(self, pos):
        pawn = None
        while pawn == None:
            promote = input("Promote pawn to [Q, R, N, B, P(or nothing)]: ")
            if promote not in ['Q', 'R', 'N', 'B', 'P', '']:
                print("Not a valid promotion piece")
            else:
                if promote == 'Q':
                    pawn = piece.Queen(True)
                elif promote == 'R':
                    pawn = piece.Rook(True)
                elif promote == 'N':
                    pawn = piece.Knight(True)
                elif promote == 'B':
                    pawn = piece.Bishop(True)
                elif promote == 'P' or promote == '':
                    pawn = piece.Pawn(True)
        self.board.board[pos[0]][pos[1]] = pawn

    def moveSim(self, start, to):
        """
        Moves a piece at `start` to `to`. Does nothing if there is no piece at the starting point.
        Does nothing if the piece at `start` belongs to the wrong color for the current turn.
        Does nothing if moving the piece from `start` to `to` is not a valid move.

        start : tup
            Position of a piece to be moved

        to : tup
            Position of where the piece is to be moved

        precondition: `start` and `to` are valid positions on the board
        """

        if self.boardSim.board[start[0]][start[1]] == None:
            #print("There is no piece to move at the start place")
            return

        if self.boardSim.board[to[0]][to[1]] != None:
            #print("other piece there")
            pass

        target_piece = self.boardSim.board[start[0]][start[1]]

        # to ensure alternate moves - ica
        # if self.turn != target_piece.color:
        #    print("That's not your piece to move")
        #    return

        end_piece = self.boardSim.board[to[0]][to[1]]
        is_end_piece = end_piece != None

        # Checks if a player's own piece is at the `to` coordinate
        if is_end_piece and self.boardSim.board[start[0]][start[1]].color == end_piece.color:
            #print("There's a piece in the path.")
            return

        if target_piece.is_valid_move(self.boardSim, start, to):

            # Special check for if the move is castling
            # Board reconfiguration is handled in Piece
            if target_piece.name == 'K' and abs(start[1] - to[1]) == 2:

                print("castled")

                if self.turn and self.black_ghost_piece:
                    self.boardSim.board[self.black_ghost_piece[0]
                                        ][self.black_ghost_piece[1]] = None
                elif not self.turn and self.white_ghost_piece:
                    self.boardSim.board[self.white_ghost_piece[0]
                                        ][self.white_ghost_piece[1]] = None
                self.turn = not self.turn
                return

            if self.boardSim.board[to[0]][to[1]]:

                print(str(self.boardSim.board[to[0]][to[1]]) + " taken.")
                # Special logic for ghost piece, deletes the actual pawn that is not in the `to`
                # coordinate from en passant
                if self.boardSim.board[to[0]][to[1]].name == "GP":

                    if self.turn:
                        self.boardSim.board[self.black_ghost_piece[0] +
                                            1][self.black_ghost_piece[1]] = None
                        self.black_ghost_piece = None
                    else:
                        self.boardSim.board[self.white_ghost_piece[0] -
                                            1][self.black_ghost_piece[1]] = None
                        self.white_ghost_piece = None

            self.boardSim.board[to[0]][to[1]] = target_piece
            self.boardSim.board[start[0]][start[1]] = None
            #print(str(target_piece) + " moved.")

            if self.turn and self.black_ghost_piece:
                self.boardSim.board[self.black_ghost_piece[0]
                                    ][self.black_ghost_piece[1]] = None
            elif not self.turn and self.white_ghost_piece:
                self.boardSim.board[self.white_ghost_piece[0]
                                    ][self.white_ghost_piece[1]] = None

            # alternate player
            self.turn = not self.turn

            # AI state change - identify change to make in state
            for m in range(len(self.boardSim.currentStateW)):

                # print("piece to move",self.board.currentStateW[m])
                aa = self.boardSim.currentStateW[m]
                # only the one to move and only for whites so far
                if self.boardSim.listNames[int(aa[2]-1)] == str(target_piece) and target_piece.color:
                    #print("->piece initial state ",self.boardSim.currentStateW[m])
                    self.boardSim.currentStateW[m][0] = to[0]
                    self.boardSim.currentStateW[m][1] = to[1]
                    #print("->piece to state ",self.boardSim.currentStateW[m])

               #   print("Next States: ",self.board.getListNextStatesW(self.board.currentStateW[m]))

    def moveSimGetPoint(self, start, to):
        """
        Moves a piece at `start` to `to`. Does nothing if there is no piece at the starting point.
        Does nothing if the piece at `start` belongs to the wrong color for the current turn.
        Does nothing if moving the piece from `start` to `to` is not a valid move.

        start : tup
            Position of a piece to be moved

        to : tup
            Position of where the piece is to be moved

        precondition: `start` and `to` are valid positions on the board

        return point for ever move
        """

        if self.boardSim.board[start[0]][start[1]] == None:
            return 

        White = self.boardSim.board[start[0]][start[1]].color

        target_piece = self.boardSim.board[start[0]][start[1]]
        end_piece = self.boardSim.board[to[0]][to[1]]

        is_end_piece = end_piece != None

        # Checks if a player's own piece is at the `to` coordinate
        if is_end_piece and target_piece.color == end_piece.color:
            return 

        # Check if a player move piece is valid move
        if target_piece.is_valid_move(self.boardSim, start, to):

            # Special check for if the move is castling
            # Board reconfiguration is handled in Piece
            if target_piece.name == 'K' and abs(start[1] - to[1]) == 2:

                print("castled")

                if self.turn and self.black_ghost_piece:
                    self.boardSim.board[self.black_ghost_piece[0]][self.black_ghost_piece[1]] = None
                elif not self.turn and self.white_ghost_piece:
                    self.boardSim.board[self.white_ghost_piece[0]][self.white_ghost_piece[1]] = None
                self.turn = not self.turn
                return

            if self.boardSim.board[to[0]][to[1]]:  # Eat piece

                # Special logic for ghost piece, deletes the actual pawn that is not in the `to`
                # coordinate from en passant
                if self.boardSim.board[to[0]][to[1]].name == "GP":
                    if self.turn:
                        self.boardSim.board[self.black_ghost_piece[0] + 1][self.black_ghost_piece[1]] = None
                        self.black_ghost_piece = None
                    else:
                        self.boardSim.board[self.white_ghost_piece[0] - 1][self.black_ghost_piece[1]] = None
                        self.white_ghost_piece = None

                # Remove piece on the list

                pieceToDelete = [to[0], to[1], self.boardSim.board[to[0]][to[1]].pieceNum]



                if not White:
                    if pieceToDelete in self.boardSim.currentStateW:
                        self.boardSim.currentStateW.remove(pieceToDelete)
                        self.boardSim.currentStateW = copy.deepcopy(self.boardSim.currentStateW)
                else:
                    if pieceToDelete in self.boardSim.currentStateB:
                        self.boardSim.currentStateB.remove(pieceToDelete)
                        self.boardSim.currentStateB = copy.deepcopy(self.boardSim.currentStateB)



            # move piece
            self.boardSim.board[to[0]][to[1]] = target_piece
            self.boardSim.board[start[0]][start[1]] = None

            if self.turn and self.black_ghost_piece:
                self.boardSim.board[self.black_ghost_piece[0]][self.black_ghost_piece[1]] = None
            elif not self.turn and self.white_ghost_piece:
                self.boardSim.board[self.white_ghost_piece[0]][self.white_ghost_piece[1]] = None

            # alternate player
            #self.turn = not self.turn

            if White:
                # AI state change - identify change to make in state
                for m in range(len(self.boardSim.currentStateW)):
                    whitePiece = self.boardSim.currentStateW[m]
                    if whitePiece[0] == start[0] and whitePiece[1] == start[1] and whitePiece[2] == target_piece.pieceNum:
                    # only the one to move and only for whites so far
                    # if self.boardSim.listNames[int(aa[2]-1)] == str(target_piece) and target_piece.color == True:
                        self.boardSim.currentStateW[m][0] = to[0]
                        self.boardSim.currentStateW[m][1] = to[1]
            else:
                # AI state change - identify change to make in state
                for m in range(len(self.boardSim.currentStateB)):
                    #aa = self.boardSim.currentStateB[m]
                    blackPiece = self.boardSim.currentStateB[m]
                    if blackPiece[0] == start[0] and blackPiece[1] == start[1] and blackPiece[2] == target_piece.pieceNum:
                    # only the one to move and only for black so far
                    # if self.boardSim.listNames[int(aa[2]-1)] == str(target_piece) and target_piece.color == False:
                        self.boardSim.currentStateB[m][0] = to[0] 
                        self.boardSim.currentStateB[m][1] = to[1]

        

        

        # logging.warning(weight)
        self.boardSim.currentStateW = copy.deepcopy(self.boardSim.currentStateW)
        self.boardSim.currentStateB = copy.deepcopy(self.boardSim.currentStateB)
        return 





    def move(self, start, to):
        """
        Moves a piece at `start` to `to`. Does nothing if there is no piece at the starting point.
        Does nothing if the piece at `start` belongs to the wrong color for the current turn.
        Does nothing if moving the piece from `start` to `to` is not a valid move.

        start : tup
            Position of a piece to be moved

        to : tup
            Position of where the piece is to be moved

        precondition: `start` and `to` are valid positions on the board
        """



        if self.board.board[start[0]][start[1]] == None:
            return


        White = self.board.board[start[0]][start[1]].color
        target_piece = self.board.board[start[0]][start[1]]

        

        
        target_piece = self.board.board[start[0]][start[1]]
        end_piece = self.board.board[to[0]][to[1]]
        is_end_piece = end_piece != None

        # Checks if a player's own piece is at the `to` coordinate
        if is_end_piece and self.board.board[start[0]][start[1]].color == end_piece.color:
            return

        if target_piece.is_valid_move(self.board, start, to):

            # Special check for if the move is castling
            # Board reconfiguration is handled in Piece
            if target_piece.name == 'K' and abs(start[1] - to[1]) == 2:
                print("castled")
                if self.turn and self.black_ghost_piece:
                    self.board.board[self.black_ghost_piece[0]][self.black_ghost_piece[1]] = None
                elif not self.turn and self.white_ghost_piece:
                    self.board.board[self.white_ghost_piece[0]][self.white_ghost_piece[1]] = None
                self.turn = not self.turn
                return


            if self.board.board[to[0]][to[1]]:
                # print(str(self.board.board[to[0]][to[1]]) + " taken.")
                # Special logic for ghost piece, deletes the actual pawn that is not in the `to`
                # coordinate from en passant
                if self.board.board[to[0]][to[1]].name == "GP":
                    if self.turn:
                        self.board.board[self.black_ghost_piece[0] + 1][self.black_ghost_piece[1]] = None
                        self.black_ghost_piece = None
                    else:
                        self.board.board[self.white_ghost_piece[0] - 1][self.black_ghost_piece[1]] = None
                        self.white_ghost_piece = None
                
                
                pieceToDelete = [to[0], to[1], self.board.board[to[0]][to[1]].pieceNum]

                if not White:
                    if pieceToDelete in self.board.currentStateW:
                        self.board.currentStateW.remove(pieceToDelete)
                        self.board.currentStateW = copy.deepcopy(self.board.currentStateW)
                else:
                    if pieceToDelete in self.board.currentStateB:
                        self.board.currentStateB.remove(pieceToDelete)
                        self.board.currentStateB = copy.deepcopy(self.board.currentStateB)



            self.board.board[to[0]][to[1]] = target_piece
            self.board.board[start[0]][start[1]] = None



            if self.turn and self.black_ghost_piece:
                self.board.board[self.black_ghost_piece[0]][self.black_ghost_piece[1]] = None
            elif not self.turn and self.white_ghost_piece:
                self.board.board[self.white_ghost_piece[0]][self.white_ghost_piece[1]] = None

            # # alternate player
            # self.turn = not self.turn


            
            if White:
                # AI state change - identify change to make in state
                for m in range(len(self.board.currentStateW)):
                    whitePiece = self.board.currentStateW[m]
                    if whitePiece[0] == start[0] and whitePiece[1] == start[1] and whitePiece[2] == target_piece.pieceNum:
                        self.board.currentStateW[m][0] = to[0]
                        self.board.currentStateW[m][1] = to[1]
            else:
                # AI state change - identify change to make in state
                for m in range(len(self.board.currentStateB)):
                    blackPiece = self.board.currentStateB[m]
                    if blackPiece[0] == start[0] and blackPiece[1] == start[1] and blackPiece[2] == target_piece.pieceNum:
                        self.board.currentStateB[m][0] = to[0] 
                        self.board.currentStateB[m][1] = to[1]


        self.currentStateW = copy.deepcopy(self.board.currentStateW)
        self.currentStateB = copy.deepcopy(self.board.currentStateB)
        self.innitialStateW = copy.deepcopy(self.board.currentStateW)
        self.innitialStateB = copy.deepcopy(self.board.currentStateB)
        self.boardSim = copy.deepcopy(self.board)



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


def inputGame():

    # intiialize board
    # current state initialization
    TA = np.zeros((8, 8))

    # # white pieces
    # TA[[6, ]] = 1  # white pawn
    # TA[7][0] = 2   # white rook
    # TA[7][1] = 3   # white knight
    # TA[7][2] = 4   # white bishop
    # TA[7][3] = 6   # white king
    # TA[7][4] = 5   # white queen
    # TA[7][5] = 4   # white bishop
    # TA[7][6] = 3   # white knight
    # TA[7][7] = 2   # white rook
    # # black pieces
    # TA[[1, ]] = 7  # black pawn
    # TA[0][0] = 8   # black rook
    # TA[0][1] = 9   # black knight
    # TA[0][2] = 10  # black bishop
    # TA[0][3] = 11  # black queen
    # TA[0][4] = 12  # black king
    # TA[0][5] = 10  # black bishop
    # TA[0][6] = 9   # black knight
    # TA[0][7] = 8   # black rook

    # initialize board
    chess = Chess(TA)
    chess.board.print_board()

    chess.board.print_board()
    while True:

        start = input("From: ")
        to = input("To: ")

        start = translate(start)
        to = translate(to)

        if start == None or to == None:
            continue

        chess.move(start, to)

        # check for promotion pawns
        i = 0
        while i < 8:
            if not chess.turn and chess.board.board[0][i] != None and \
                    chess.board.board[0][i].name == 'P':
                chess.promotion((0, i))
                break
            elif chess.turn and chess.board.board[7][i] != None and \
                    chess.board.board[7][i].name == 'P':
                chess.promotion((7, i))
                break
            i += 1

        chess.board.print_board()


def GameOver(board):
    '''
    True --> game over
    '''

    count = 0
    for i in range(8):
        for j in range(8):
            if (board[i][j] != None) and (board[i][j].pieceNum == 6 or board[i][j].pieceNum == 12):
                count += 1

    if count < 2:
        return True
    else:
        return False


def movePiece(chess, currentState, nextState):
    start = [e for e in currentState if e not in nextState][0][0:2]
    to = [e for e in nextState if e not in currentState][0][0:2]
    chess.move(start, to)
    return


def practica2():
    # intiialize board
    # current state initialization
    TA = np.zeros((8, 8))

    # white pieces
    TA[7][5] = 6        # white king
    TA[7][0] = 2        # white rook

    # black pieces
    TA[0][5] = 12       # black king
    TA[0][0] = 8        # black rook



    # initialize board
    chess = Chess(TA)
    # print board
    chess.board.print_board()

    WhitePlayerAichess = aichess.Aichess(TA, True, True)
    BlackPlayerAichess = aichess.Aichess(TA, False, True)

    #-------------------------- MiniMax --------------------------------------- #
    print("#-------------------------- MiniMax --------------------------------------- #")


    WhitePlayerMinimax = copy.deepcopy(WhitePlayerAichess)
    BlackPlayerMinimax = copy.deepcopy(BlackPlayerAichess)

    depth = 2
    while not GameOver(chess.board.board):

        # ----------------White Player -------------------------------- #
        print("White player minimax: ")
        WhitePlayerCurrentState = copy.deepcopy(chess.board.currentStateW)
        WhitePlayerMinimax.chess = copy.deepcopy(chess)
        WhitePlayerMinimax.chessStack = [copy.deepcopy(WhitePlayerMinimax.chess)]

        WhitePlayerMinimax.currentStateW = copy.deepcopy(chess.board.currentStateW)
        WhitePlayerMinimax.currentStateB = copy.deepcopy(chess.board.currentStateB)
        WhitePlayerMinimax.innitialStateW = copy.deepcopy(chess.board.currentStateW)
        WhitePlayerMinimax.innitialStateB = copy.deepcopy(chess.board.currentStateB)
        WhitePlayerNextState = WhitePlayerMinimax.Minimax(depth)
        print(WhitePlayerCurrentState)

    
        print(WhitePlayerNextState)

        movePiece(chess, WhitePlayerCurrentState, WhitePlayerNextState)
        chess.board.print_board()

        if GameOver(chess.board.board):
            break
    

        # ----------------Black Player -------------------------------- #
        print("Black player minimax: ")
        BlackPlayerCurrentState = copy.deepcopy(chess.board.currentStateB)
        BlackPlayerMinimax.chess = copy.deepcopy(chess)
        BlackPlayerMinimax.chessStack = [copy.deepcopy(BlackPlayerMinimax.chess)]

        BlackPlayerMinimax.currentStateW = copy.deepcopy(chess.board.currentStateW)
        BlackPlayerMinimax.currentStateB = copy.deepcopy(chess.board.currentStateB)
        BlackPlayerMinimax.innitialStateW = copy.deepcopy(chess.board.currentStateW)
        BlackPlayerMinimax.innitialStateB = copy.deepcopy(chess.board.currentStateB)

        BlackPlayerNextState = BlackPlayerMinimax.Minimax(depth)
        print(BlackPlayerCurrentState)
        print(BlackPlayerNextState)

        movePiece(chess, BlackPlayerCurrentState, BlackPlayerNextState)
        chess.board.print_board()

        if GameOver(chess.board.board):
            break
        
        






    # # -------------------------------Alpha beta------------------------------------ #
    print("# -------------------------------Alpha beta------------------------------------ #")



    WhitePlayerAlphaBeta = copy.deepcopy(WhitePlayerAichess)
    BlackPlayerAlphaBeta = copy.deepcopy(BlackPlayerAichess)


    depth = 2
    while not GameOver(chess.board.board):

        # ----------------------White Player -------------------------------- #
        print("White player Alpha beta: ")
        WhitePlayerCurrentState = copy.deepcopy(chess.board.currentStateW)
        WhitePlayerAlphaBeta.chess = copy.deepcopy(chess)
        WhitePlayerAlphaBeta.chessStack = [copy.deepcopy(WhitePlayerAlphaBeta.chess)]

        WhitePlayerAlphaBeta.currentStateW = copy.deepcopy(chess.board.currentStateW)
        WhitePlayerAlphaBeta.currentStateB = copy.deepcopy(chess.board.currentStateB)
        WhitePlayerAlphaBeta.innitialStateW = copy.deepcopy(chess.board.currentStateW)
        WhitePlayerAlphaBeta.innitialStateB = copy.deepcopy(chess.board.currentStateB)

        WhitePlayerNextState = WhitePlayerAlphaBeta.AlphaBeta(depth)
        print(WhitePlayerCurrentState)
        print(WhitePlayerNextState)

        movePiece(chess, WhitePlayerCurrentState, WhitePlayerNextState)
        chess.board.print_board()

        if GameOver(chess.board.board):
            break

        

        # ----------------Black Player -------------------------------- #
        print("Black player Alpha beta: ")
        BlackPlayerCurrentState = copy.deepcopy(chess.board.currentStateB)
        BlackPlayerAlphaBeta.chess = copy.deepcopy(chess)
        BlackPlayerAlphaBeta.chessStack = [copy.deepcopy(BlackPlayerAlphaBeta.chess)]

        BlackPlayerAlphaBeta.currentStateW = copy.deepcopy(chess.board.currentStateW)
        BlackPlayerAlphaBeta.currentStateB = copy.deepcopy(chess.board.currentStateB)
        BlackPlayerAlphaBeta.innitialStateW = copy.deepcopy(chess.board.currentStateW)
        BlackPlayerAlphaBeta.innitialStateB = copy.deepcopy(chess.board.currentStateB)

        BlackPlayerNextState = BlackPlayerAlphaBeta.AlphaBeta(depth)
        print(BlackPlayerCurrentState)
        print(BlackPlayerNextState)

        movePiece(chess, BlackPlayerCurrentState, BlackPlayerNextState)
        chess.board.print_board()

        if GameOver(chess.board.board):
            break






    # -----------------------------Expect Max-------------------------------- #
    print("# -----------------------------Expect Max-------------------------------- #")

    WhitePlayerExpectMax = copy.deepcopy(WhitePlayerAichess)
    BlackPlayerExpectMax = copy.deepcopy(BlackPlayerAichess)


    while not GameOver(chess.board.board):

        # ----------------White Player -------------------------------- #
        print("White player ExpectMax: ")
        BlackPlayerCurrentState = copy.deepcopy(chess.board.currentStateB)
        WhitePlayerExpectMax.chess = copy.deepcopy(chess)
        WhitePlayerExpectMax.chessStack = [copy.deepcopy(WhitePlayerExpectMax.chess)]

        WhitePlayerExpectMax.currentStateW = copy.deepcopy(chess.board.currentStateW)
        WhitePlayerExpectMax.currentStateB = copy.deepcopy(chess.board.currentStateB)
        WhitePlayerExpectMax.innitialStateW = copy.deepcopy(chess.board.currentStateW)
        WhitePlayerExpectMax.innitialStateB = copy.deepcopy(chess.board.currentStateB)
        WhitePlayerNextState = WhitePlayerExpectMax.ExpectiMax()


        print(WhitePlayerCurrentState)
        print(WhitePlayerNextState)

        movePiece(chess, WhitePlayerCurrentState, WhitePlayerNextState)
        chess.board.print_board()

        if GameOver(chess.board.board):
            break


        # ----------------Black Player -------------------------------- #
        print("Black player ExpectMax: ")
        BlackPlayerCurrentState = copy.deepcopy(chess.board.currentStateB)
        BlackPlayerExpectMax.chess = copy.deepcopy(chess)
        BlackPlayerExpectMax.chessStack = [copy.deepcopy(BlackPlayerExpectMax.chess)]

        BlackPlayerExpectMax.currentStateW = copy.deepcopy(chess.board.currentStateW)
        BlackPlayerExpectMax.currentStateB = copy.deepcopy(chess.board.currentStateB)
        BlackPlayerExpectMax.innitialStateW = copy.deepcopy(chess.board.currentStateW)
        BlackPlayerExpectMax.innitialStateB = copy.deepcopy(chess.board.currentStateB)

        BlackPlayerNextState = BlackPlayerExpectMax.ExpectiMax()
        print(BlackPlayerCurrentState)
        print(BlackPlayerNextState)

        movePiece(chess, BlackPlayerCurrentState, BlackPlayerNextState)
        chess.board.print_board()

        if GameOver(chess.board.board):
            break




def exercici1():
    # intiialize board
    # current state initialization
    TA = np.zeros((8, 8))

    # white pieces
    TA[7][5] = 6        # white king
    TA[7][0] = 2        # white rook

    # black pieces
    TA[0][5] = 12       # black king


    # initialize board
    chess = Chess(TA)
    # print board
    chess.board.print_board()

    WhitePlayerAichess = aichess.Aichess(TA, True, True)
    WhitePlayerAichess.Q_Learning()


def exercici2():
    pass

if __name__ == "__main__":

    initLogging()


    exercici1()

    


        


