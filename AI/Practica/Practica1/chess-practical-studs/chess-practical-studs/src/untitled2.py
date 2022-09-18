#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 11:18:55 2022

@author: ignasi
"""
    # list of from-to positions
    #MovesToMake = ['1e','2e']
    # '2e','3e','3e','4d','4d','3c']

#    for k in range(int(len(MovesToMake)/2)):

#        print("k: ",k)


#        print("start: ",MovesToMake[2*k])
#        print("to: ",MovesToMake[2*k+1])

#        start = translate(MovesToMake[2*k])
#        to = translate(MovesToMake[2*k+1])

#        print("start: ",start)
#        print("to: ",to)

#    while True:

#        start = input("From: ")
#        to = input("To: ")

#        start = translate(start)
#        to = translate(to)

 #       if start == None or to == None:
 #           continue

#        print("aichess current state White",aichess.chess.board.currentStateW)
#        print("aichess current state Black",aichess.chess.board.currentStateB)

#        print("liststart ",[list(start)])

#        aichess.chess.board.getListNextStatesW([list(start)])
    #aichess.chess.board.getListNextStatesW(aichess.chess.board.currentStateW)
#       print("next states",aichess.chess.board.listNextStates)
#       print("len(next)",len(aichess.chess.board.listNextStates))

    # starting from current state find the end state (check mate) - recursive function
    #aichess.chess.board.listVisitedStates = []

    #DepthFirstSearch(ichess.chess.board.currentStateW)


#        print("aichess previous state",aichess.chess.board.currentStateW)
#        aichess.chess.move(start, to)
#        print("aichess state",aichess.chess.board.currentStateW)

    # check for promotion pawns
    #   i = 0
    #   while i < 8:
    #
    #       if not aichess.chess.turn and aichess.chess.board.board[0][i] != None and \
    #           aichess.chess.board.board[0][i].name == 'P':
    #           aichess.chess.promotion((0, i))
    #           break
    #
    #       elif aichess.chess.turn and aichess.chess.board.board[7][i] != None and \
    #           aichess.chess.board.board[7][i].name == 'P':
    #           aichess.chess.promotion((7, i))
    #           break
    #
    #       i += 1
    #
    #   print("#Move...  ",k)
