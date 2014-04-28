from random import choice

from tictactoe import Board
from tictactoe import Move
from tictactoe import PLAYER1
from tictactoe import PLAYER2
from tictactoe import Piece


def get_best_move(player, opponent, board, verbose=False):
    possibilities = {}
    for x, y in board.get_moves():
        move = Move(Piece(player, x, y))
        possibilities[move] = board.add_move(move)

    # Check for immediate win
    for move, new_board in possibilities.iteritems():
        state, winner = new_board.get_state()
        if state == 'WINNER':
            move.state = 'WIN'
            return move

    # Forced move
    if len(possibilities) == 1:
        move = possibilities.iterkeys().next()
        move.state = 'TIE'
        return move

    # Consider the best opponent move
    possibilities2 = {}
    for move, new_board in possibilities.iteritems():
        opp_move = get_best_move(opponent, player, new_board)
        if opp_move.state == 'LOSE':
            move.state = 'WIN'
            return move
        elif opp_move.state == 'WIN':
            move.state = 'LOSE'
            continue
        else:  # opp_move.state == 'TIE'
            move.state = 'TIE'
        possibilities2[move] = new_board.add_move(opp_move)

    # We're gonna lose :(
    if len(possibilities2) == 0:
        move = choice(possibilities.keys())
        assert move.state == 'LOSE'
        return move

    # Tie game
    move = choice(possibilities2.keys())
    assert move.state == 'TIE'
    return move


def check_over(board):
    print board
    state, winner = board.get_state()
    if state == 'WINNER':
        print state, winner
        return True
    elif state == 'TIE':
        print state
        return True
    return False


if __name__ == '__main__':
    board = Board()
    print board
    print '\n---'

    while True:
        i, j = map(int, raw_input().split(' '))
        board = board.add_move(Move(Piece(PLAYER1, i, j)))
        if check_over(board):
            break
        print '\n---'

        move = get_best_move(PLAYER2, PLAYER1, board, verbose=True)
        board = board.add_move(move)
        if check_over(board):
            break
        print '\n---'
