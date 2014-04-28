from collections import Counter
from copy import deepcopy

import numpy as np


PLAYER1 = 'WHITE'
PLAYER2 = 'BLACK'

BOARD_WIDTH = 3
BOARD_HEIGHT = 3
WIN_LEN = 3


class IllegalMoveException(Exception):
    pass


class Board(object):

    def __init__(self):
        board = np.array([None] * BOARD_WIDTH * BOARD_HEIGHT)
        self.board = board.reshape(BOARD_WIDTH, BOARD_HEIGHT)
        self.history = []


    def __repr__(self):
        return str(self)


    def __str__(self):
        rows = ['']
        for row in self.board:
            rows.append(''.join(['_' if piece is None else str(piece)
                                 for piece in row]))
        return '\n'.join(rows)


    def get_state(self):
        '''
        Returns ('PENDING', None) if the game is playing
        Returns ('TIE', None) if the game is tied
        Returns ('WINNER', PLAYER1|PLAYER2) if there's a winner
        '''

        def check_winner(three):
            counts = Counter([piece.player for piece in
                              filter(lambda x: x is not None, three)])
            if counts[PLAYER1] == WIN_LEN:
                return ('WINNER', PLAYER1)
            if counts[PLAYER2] == WIN_LEN:
                return ('WINNER', PLAYER2)
            return None

        # Check for winners
        for row in self.board:
            result = check_winner(row)
            if result is not None:
                return result

        for col in self.board.T:
            result = check_winner(col)
            if result is not None:
                return result

        # Check the diagonals
        result = check_winner([self.board[idx][idx]
                               for idx in range(WIN_LEN)])
        if result is not None:
            return result
        result = check_winner([self.board[BOARD_HEIGHT-idx-1][idx]
                               for idx in range(WIN_LEN)])
        if result is not None:
            return result

        # Check for tie game
        if len(filter(lambda x: x is not None,
                      self.board.flatten())) == 9:
            return ('TIE', None)

        # Otherwise, return pending
        return ('PENDING', None)


    def get_moves(self):
        '''
        yields a list of locations (tuple of (row, col))
        '''
        for i, row in enumerate(self.board):
            for j, piece in enumerate(row):
                if piece is None:
                    yield (j, i)


    def can_move(self, move):
        # Check that the player isn't executing out of turn
        if len(self.history) == 0:
            if move.player == PLAYER2:
                return False
        elif self.history[-1].player == move.player:
            return False
        # Check that the location is still available
        return self.board[move.piece.row][move.piece.col] is None


    def add_move(self, move):
        '''
        Tries to execute the move.  Raises IllegalMoveException if
        the move is illegal
        '''
        if self.can_move(move):
            new_board = deepcopy(self)
            new_board.history.append(move)
            new_board.board[move.piece.row][move.piece.col] = move.piece
            return new_board
        else:
            raise IllegalMoveException


class Move(object):

    def __init__(self, piece, state=None):
        self.player = piece.player
        self.piece = piece
        self.state = state


    def __repr__(self):
        return str(self)


    def __str__(self):
        return '%s %d %d' % (self.player, self.piece.col, self.piece.row)


class Piece(object):

    def __init__(self, player, col, row):
        self.player = player

        if type(row) != int or type(col) != int:
            raise IllegalMoveException
        if row >= BOARD_WIDTH or row < 0:
            raise IllegalMoveException
        if col >= BOARD_HEIGHT or col < 0:
            raise IllegalMoveException

        self.row = row
        self.col = col


    def __str__(self):
        if self.player == PLAYER1:
            return 'W'
        else:
            return 'B'


