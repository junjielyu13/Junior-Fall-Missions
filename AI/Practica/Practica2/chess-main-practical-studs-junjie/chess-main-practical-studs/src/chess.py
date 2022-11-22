
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
        self.currentStateW = []  # self.boardSim.currentStateW.copy()
        self.currentStateB = []  # self.boardSim.currentStateB.copy();

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
            logging.critical("There is no piece to move at the start place")
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

    def moveSimGetPoint(self, start, to, weight):
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

        logging.debug("Before: ")
        logging.debug(self.boardSim.currentStateW)
        logging.debug(self.boardSim.currentStateB)

        if self.boardSim.board[start[0]][start[1]] == None:
            # self.boardSim.print_board()
            logging.critical("There is no piece to move at the start place")
            return weight

        White = self.boardSim.board[start[0]][start[1]].color

        target_piece = self.boardSim.board[start[0]][start[1]]
        end_piece = self.boardSim.board[to[0]][to[1]]

        is_end_piece = end_piece != None

        # Checks if a player's own piece is at the `to` coordinate
        if is_end_piece and target_piece.color == end_piece.color:
            return weight

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

                # if self.turn:

                if self.whitePlayer == True and self.whiteTurn == True:
                    #print("white Player White turn: " + str(self.boardSim.board[to[0]][to[1]]) + " taken.")
                    logging.warning("white Player White turn: " +  str(self.boardSim.board[to[0]][to[1]]) + " taken.")
                elif self.whitePlayer == True and self.whiteTurn == False:
                    #print("white Player Black turn: " +  str(self.boardSim.board[to[0]][to[1]]) + " taken.")
                    logging.warning("white Player Black turn: " +  str(self.boardSim.board[to[0]][to[1]]) + " taken.")
                elif self.whitePlayer == False and self.whiteTurn == True:
                    #print("Black Player White turn: " + str(self.boardSim.board[to[0]][to[1]]) + " taken.")
                    logging.warning("Black Player White turn: " + str(self.boardSim.board[to[0]][to[1]]) + " taken.")
                elif self.whitePlayer == False and self.whiteTurn == False:
                    #print("Black Player Black turn: " + str(self.boardSim.board[to[0]][to[1]]) + " taken.")
                    logging.warning("Black Player Black turn: " + str(self.boardSim.board[to[0]][to[1]]) + " taken.")
                else:
                    logging.critical("error")
                    print("eroror")

                if self.whitePlayer == self.whiteTurn:
                    weight += self.boardSim.board[to[0]][to[1]].point
                else:
                    weight -= self.boardSim.board[to[0]][to[1]].point

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

                logging.debug("piece to delete")
                logging.debug(pieceToDelete)

                if not White:
                    logging.debug("self.boardSim.currentStateW")
                    logging.debug(self.boardSim.currentStateW)
                    if pieceToDelete in self.boardSim.currentStateW:
                        self.boardSim.currentStateW.remove(pieceToDelete)
                        logging.debug("white after remove self.boardSim.currentStateW")
                        logging.debug(self.boardSim.currentStateW)
                        self.boardSim.currentStateW = copy.deepcopy(self.boardSim.currentStateW)
                    else:
                        logging.critical("White: doesn't have a piece to delete")
                        logging.debug(self.boardSim.currentStateW)
                else:
                    logging.debug("self.boardSim.currentStateB")
                    logging.debug(self.boardSim.currentStateB)
                    if pieceToDelete in self.boardSim.currentStateB:
                        logging.debug(self.boardSim.currentStateB)
                        self.boardSim.currentStateB.remove(pieceToDelete)
                        logging.debug("blakc after remove self.boardSim.currentStateW")
                        logging.debug(self.boardSim.currentStateB)
                        self.boardSim.currentStateB = copy.deepcopy(self.boardSim.currentStateB)
                    else:
                        logging.critical("black: doesn't have a piece to delete")
                        logging.debug(self.boardSim.currentStateB)

            else:                                   # Just a move
                # evaluate heuristica

                heuristica = 0

                pos = [0,0]
                Ourpos = [0,0]
                for i in range(8):
                    for j in range(8):
                        if self.boardSim.board[i][j] != None and self.boardSim.board[i][j].name == 'K' and self.boardSim.board[start[0]][start[1]].color != self.boardSim.board[i][j].color:
                            oppsiteKing = self.boardSim.board[i][j]
                            pos[0] = i
                            pos[1] = j
                        if self.boardSim.board[i][j] != None and self.boardSim.board[i][j].name == 'K' and target_piece.color == self.boardSim.board[i][j].color:
                            Ourpos[0] = i
                            Ourpos[1] = j

                if target_piece.name == 'K':
                    distEuclide = abs(start[0] - pos[0]) + abs(start[1] - pos[1])
                    if distEuclide == 3 and (start[0] != pos[0] or start[1] != pos[1]):
                        heuristica += 0
                    elif distEuclide > 2:
                        heuristica += distEuclide*10

                    logging.info(f"heuristica king : {heuristica}")
                    

                elif target_piece.name == 'R':
                    distEuclideKing = abs(Ourpos[0] - pos[0]) + abs(Ourpos[1] - pos[1])
                    distEuclideRook = abs(start[0] - pos[0]) + abs(start[1] - pos[1])


                    ix = start[0]
                    iy = start[1]
                    while (ix < 7):
                        ix = ix + 1
                        distEuclideRook = abs(ix - pos[0]) + abs(iy  - pos[1])
                        if ix == pos[0] and distEuclideRook >= 2:
                            heuristica += 7
                            break

                    ix = start[0]
                    iy = start[1]
                    while (ix > 0):
                        ix = ix - 1
                        distEuclideRook = abs(ix - pos[0]) + abs(iy  - pos[1])
                        if ix == pos[0] and distEuclideRook >= 2: 
                            heuristica += 7
                            break

                    ix = start[0]
                    iy = start[1]
                    while (iy < 7):
                        iy = iy + 1
                        distEuclideRook = abs(ix - pos[0]) + abs(iy  - pos[1])
                        if iy == pos[1] and distEuclideRook >= 2:
                            heuristica += 7
                            break

                    ix = start[0]
                    iy = start[1]
                    while (iy > 0):
                        iy = iy - 1
                        distEuclideRook = abs(ix - pos[0]) + abs(iy  - pos[1])
                        if iy == pos[1] and distEuclideRook >= 2:
                            heuristica += 7
                            break

                    if distEuclideKing == 3 and (start[0] != pos[0] or start[1] != pos[1]):
                        heuristica += 20
                        

                else:
                    heuristica += 0


                if self.whitePlayer == self.whiteTurn:
                    weight += heuristica
                else:
                    weight -= heuristica

                logging.info(f"heuristica rook : {heuristica}")


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
        logging.debug("End: ")
        logging.debug(self.boardSim.currentStateW)
        logging.debug(self.boardSim.currentStateB)
        return weight





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

                print(str(self.board.board[to[0]][to[1]]) + " taken.")
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


        self.board.currentStateW = copy.deepcopy(self.board.currentStateW)
        self.board.currentStateB = copy.deepcopy(self.board.currentStateB)





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


if __name__ == "__main__":

    initLogging()

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

    # # white pieces
    # TA[7][5] = 6        # white king
    # TA[7][0] = 2        # white rook

    # # black pieces
    # TA[0][5] = 12       # black king
    # TA[0][0] = 8        # black rook

    # white pieces
    TA[5][5] = 6        # white king
    TA[6][0] = 2        # white rook

    # black pieces
    TA[3][4] = 12       # black king


    # initialize board
    chess = Chess(TA)
    #  chess = Chess([],False)

    # print board
    chess.board.print_board()



    
    WhitePlayerAichess = aichess.Aichess(TA, True, True)
    WhitePlayerCurrentState = WhitePlayerAichess.chess.board.currentStateW.copy()

    BlackPlayerAichess = aichess.Aichess(TA, False, True)
    BlackPlayerCurrentState = BlackPlayerAichess.chess.board.currentStateB.copy()


    WhitePlayerMinimax = copy.deepcopy(WhitePlayerAichess)
    BlackPlayerMinimax = copy.deepcopy(BlackPlayerAichess)

    # WhitePlayerNextState = WhitePlayerMinimax.Minimax(WhitePlayerCurrentState, 4)
    # logging.critical("minimax WHITE: ")
    # logging.critical(WhitePlayerCurrentState)
    # logging.critical(WhitePlayerNextState)

    # BlackPlayerNextState = BlackPlayerMinimax.Minimax(BlackPlayerCurrentState, 4)
    # logging.critical("minimax BLACK: ")
    # logging.critical(BlackPlayerCurrentState)
    # logging.critical(BlackPlayerNextState)

    # chessTable = Queue(12)    
    # chessTable.put(chess.board)

    # while not GameOver(chess.board.board):

    #     # ----------------White Player -------------------------------- #
    #     print("White player minimax: ")
    #     WhitePlayerCurrentState = chess.board.currentStateW
    #     WhitePlayerMinimax.chess.boardSim = chess.board
    #     WhitePlayerMinimax.currentStateW = chess.board.currentStateW
    #     WhitePlayerMinimax.currentStateB = chess.board.currentStateB
    #     WhitePlayerNextState = WhitePlayerMinimax.Minimax(2)
    #     print(WhitePlayerCurrentState)
    #     print(WhitePlayerNextState)

    #     movePiece(chess, WhitePlayerCurrentState, WhitePlayerNextState)
    #     chess.board.print_board()

    #     if GameOver(chess.board.board):
    #         break
        
    #     # chessTable.put(chess.board)
    #     # if chessTable.qsize() >= 12:
    #     #     chesslist = chessTable.queue
            
    #     #     if ( (chesslist[0] == chesslist[4] and chesslist[4] == chesslist[8]) and 
    #     #          (chesslist[1] == chesslist[5] and chesslist[5] == chesslist[9]) and 
    #     #          (chesslist[2] == chesslist[6] and chesslist[6] == chesslist[10]) and 
    #     #          (chesslist[3] == chesslist[7] and chesslist[7] == chesslist[11]) 
    #     #         ):

    #     #         print("white empate")
    #     #         break
    #     #     chessTable.get()





    #     # ----------------Black Player -------------------------------- #
    #     print("Black player minimax: ")
    #     BlackPlayerCurrentState = chess.board.currentStateB
    #     BlackPlayerMinimax.chess.boardSim = chess.board
    #     BlackPlayerMinimax.currentStateW = chess.board.currentStateW
    #     BlackPlayerMinimax.currentStateB = chess.board.currentStateB
    #     BlackPlayerNextState = BlackPlayerMinimax.Minimax(2)
    #     print(BlackPlayerCurrentState)
    #     print(BlackPlayerNextState)

    #     movePiece(chess, BlackPlayerCurrentState, BlackPlayerNextState)
    #     chess.board.print_board()

    #     if GameOver(chess.board.board):
    #         break
        
        
        # chessTable.put(chess.board)
        # if chessTable.qsize() >= 12:
        #     chesslist = chessTable.queue
            
        #     if ( (chesslist[0] == chesslist[4] and chesslist[4] == chesslist[8]) and 
        #          (chesslist[1] == chesslist[5] and chesslist[5] == chesslist[9]) and 
        #          (chesslist[2] == chesslist[6] and chesslist[6] == chesslist[10]) and 
        #          (chesslist[3] == chesslist[7] and chesslist[7] == chesslist[11]) 
        #         ):

        #         print("black empate")
        #         break
        #     chessTable.get()




    # -----------------------------------------------------------------------------




    WhitePlayerMinimax = copy.deepcopy(WhitePlayerAichess)
    BlackPlayerMinimax = copy.deepcopy(BlackPlayerAichess)

    # WhitePlayerNextState = WhitePlayerMinimax.AlfaBeta(WhitePlayerCurrentState, 3)
    # logging.critical("minimax WHITE: ")
    # logging.critical(WhitePlayerCurrentState)
    # logging.critical(WhitePlayerNextState)

    # BlackPlayerNextState = BlackPlayerMinimax.AlfaBeta(BlackPlayerCurrentState, 3)
    # logging.critical("minimax BLACK: ")
    # logging.critical(BlackPlayerCurrentState)
    # logging.critical(BlackPlayerNextState)

    # chessTable = Queue(12)    
    # chessTable.put(chess.board)

    depth = 2

    while not GameOver(chess.board.board):

        # ----------------White Player -------------------------------- #
        print("White player minimax: ")
        WhitePlayerCurrentState = chess.board.currentStateW
        WhitePlayerMinimax.chess.boardSim = chess.board
        WhitePlayerMinimax.currentStateW = chess.board.currentStateW
        WhitePlayerMinimax.currentStateB = chess.board.currentStateB
        WhitePlayerNextState = WhitePlayerMinimax.AlfaBeta(WhitePlayerCurrentState, depth)

        logging.critical("minimax WHITE: ")
        logging.critical(WhitePlayerCurrentState)
        logging.critical(WhitePlayerNextState)
        print(WhitePlayerCurrentState)
        print(WhitePlayerNextState)

        movePiece(chess, WhitePlayerCurrentState, WhitePlayerNextState)
        chess.board.print_board()

        if GameOver(chess.board.board):
            break


        # ----------------Black Player -------------------------------- #
        print("Black player minimax: ")
        BlackPlayerCurrentState = chess.board.currentStateB
        BlackPlayerMinimax.chess.boardSim = chess.board
        BlackPlayerMinimax.currentStateW = chess.board.currentStateW
        BlackPlayerMinimax.currentStateB = chess.board.currentStateB
        BlackPlayerNextState = BlackPlayerMinimax.AlfaBeta(BlackPlayerCurrentState, depth)
        logging.critical("minimax BLACK: ")
        logging.critical(BlackPlayerCurrentState)
        logging.critical(BlackPlayerNextState)
        print(BlackPlayerCurrentState)
        print(BlackPlayerNextState)

        movePiece(chess, BlackPlayerCurrentState, BlackPlayerNextState)
        chess.board.print_board()

        if GameOver(chess.board.board):
            break


    # WhitePlayerMinimax = copy.deepcopy(WhitePlayerAichess)
    # BlackPlayerMinimax = copy.deepcopy(BlackPlayerAichess)

    # # WhitePlayerNextState = WhitePlayerMinimax.Expectimax(WhitePlayerCurrentState, 3)
    # # logging.critical("minimax WHITE: ")
    # # logging.critical(WhitePlayerCurrentState)
    # # logging.critical(WhitePlayerNextState)

    # # BlackPlayerNextState = BlackPlayerMinimax.Expectimax(BlackPlayerCurrentState, 2)
    # # logging.critical("minimax BLACK: ")
    # # logging.critical(BlackPlayerCurrentState)
    # # logging.critical(BlackPlayerNextState)

    # # chessTable = Queue(12)    
    # # chessTable.put(chess.board)

    # while not GameOver(chess.board.board):

    #     # ----------------White Player -------------------------------- #
    #     print("White player minimax: ")
    #     WhitePlayerCurrentState = chess.board.currentStateW
    #     WhitePlayerMinimax.chess.boardSim = chess.board
    #     WhitePlayerMinimax.currentStateW = chess.board.currentStateW
    #     WhitePlayerMinimax.currentStateB = chess.board.currentStateB
    #     WhitePlayerNextState = WhitePlayerMinimax.Expectimax(WhitePlayerCurrentState, 3)

    #     logging.critical("minimax WHITE: ")
    #     logging.critical(WhitePlayerCurrentState)
    #     logging.critical(WhitePlayerNextState)
    #     print(WhitePlayerCurrentState)
    #     print(WhitePlayerNextState)

    #     movePiece(chess, WhitePlayerCurrentState, WhitePlayerNextState)
    #     chess.board.print_board()

    #     if GameOver(chess.board.board):
    #         break


    #     # ----------------Black Player -------------------------------- #
    #     print("Black player minimax: ")
    #     BlackPlayerCurrentState = chess.board.currentStateB
    #     BlackPlayerMinimax.chess.boardSim = chess.board
    #     BlackPlayerMinimax.currentStateW = chess.board.currentStateW
    #     BlackPlayerMinimax.currentStateB = chess.board.currentStateB
    #     BlackPlayerNextState = BlackPlayerMinimax.Expectimax(BlackPlayerCurrentState, 3)
    #     logging.critical("minimax BLACK: ")
    #     logging.critical(BlackPlayerCurrentState)
    #     logging.critical(BlackPlayerNextState)
    #     print(BlackPlayerCurrentState)
    #     print(BlackPlayerNextState)

    #     movePiece(chess, BlackPlayerCurrentState, BlackPlayerNextState)
    #     chess.board.print_board()

    #     if GameOver(chess.board.board):
    #         break
        


