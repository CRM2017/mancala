import random
from board import Board, RED_HOLES, RED_MANCALA, BLUE_MANCALA, BLUE_HOLES, N

# TODO: Alpha_Beta():


def heuristics1(board, player):
    board = board.board
    if player == 'red':
        # new_board.red_moves(move, clockwise=True)
        return (board[0] + board[12]) - (board[6] + board[18])
    else:
        return (board[6] + board[18]) - (board[0] + board[12])


def heuristics2(board, player):
    score = 0
    if player == 'red':
        for index in RED_HOLES:
            score += board[index]
        return score
    else:
        for index in BLUE_HOLES:
            score += board[index]
        return score

def get_most_stones_index(board, index_list):
    hole_index = -1
    stones = board[index_list[0]]
    for index in index_list:
        if board[index] > stones:
            hole_index = index
            stones = board[index]
    return hole_index, stones


def calculate_score(board):
    red_score = board[0] + board[12]
    blue_score = board[6] + board[18]
    print('Final score: red with {}, blue with {}'.format(red_score, blue_score))


def is_game_over(board):
    # there is any stones in red holes or blue hole, return False (game is not over)
    if any(board[1:4] + board[10:12] + board[13:16] + board[22:24]) or \
            any(board[4:6] + board[7:10] + board[16:18] + board[19:22]):
        return False
    else:
        return True


def get_available_moves(board, player):
    moves = []
    if player == 'red':
        for hole in RED_HOLES:
            if board[hole] != 0:
                moves.append(hole)
    else:
        for hole in BLUE_HOLES:
            if board[hole] != 0:
                moves.append(hole)
    return moves


def switch_player(player):
    if player == 'red':
        return 'blue'
    elif player == 'blue':
        return 'red'
    else:
        print('INPUT ERROR @func: switch_player()')

count = 0
def _mini_max(depth, board, player):
    global count
    count +=1
    print('Node: {}'.format(count))
    board.pretty()
    print("payoff {}:".format(player), heuristics1(board, player))
    if depth > 2 or is_game_over(board.board):
        return heuristics1(board, player), None
    if player == 'red':
        best_value = (-10 * N), None  # best_value (score, move)
        max_moves = get_available_moves(board.board, 'red')
        if max_moves == []:
            val = _mini_max(depth+1, board, 'blue')
            if val[0] > best_value[0]:
                best_value = val[0], None
        for move in max_moves:
            cw_move_result = board.red_moves(index=move) # clockwise move
            ccw_move_result = board.red_moves(index=move, clockwise=False) # counter-clockwise move

            cw_val = _mini_max(depth+1, Board(cw_move_result[0]), 'blue')
            ccw_val = _mini_max(depth + 1, Board(ccw_move_result[0]), 'blue')
            best_value = max(cw_val[0], ccw_val[0], best_value[0]), move
        return best_value

    elif player == 'blue':
        best_value = (10 * N), None
        min_moves = get_available_moves(board.board, 'blue')
        if min_moves == []:
            val = _mini_max(depth + 1, board, 'red')
            if val[0] < best_value[0]:
                best_value = val[0], None
        for move in min_moves:
            cw_move_result = board.red_moves(index=move)  # clockwise move
            ccw_move_result = board.red_moves(index=move, clockwise=False)  # counter-clockwise move
            cw_val = _mini_max(depth + 1, Board(cw_move_result[0]), 'red')
            ccw_val = _mini_max(depth + 1, Board(ccw_move_result[0]), 'red')
            best_value = min(cw_val[0], ccw_val[0], best_value[0]), move
        return best_value


def run_max_move(depth, board, player):
    best_value = [(-10 * N), None]  # best_value list [score, move]
    max_moves = get_available_moves(board.board, player)
    if max_moves == []:
        val = mini_max(depth + 1, board, switch_player(player))
        if val[0] > best_value[0]:
            best_value = [val[0], None]
    for move in max_moves:
        cw_move_result = None
        ccw_move_result = None
        if player == 'red':
            cw_move_result = board.red_moves(index=move)  # clockwise move
            ccw_move_result = board.red_moves(index=move, clockwise=False)  # counter-clockwise move
        elif player == 'blue':
            cw_move_result = board.blue_moves(index=move)  # clockwise move
            ccw_move_result = board.blue_moves(index=move, clockwise=False)  # counter-clockwise move
        cw_val = mini_max(depth + 1, Board(cw_move_result[0]), switch_player(player))
        ccw_val = mini_max(depth + 1, Board(ccw_move_result[0]), switch_player(player))
        best_value = [max(cw_val[0], ccw_val[0], best_value[0]), move]
    return best_value


def run_mini_move(depth, board, player):
    best_value = (10 * N), None
    min_moves = get_available_moves(board.board, player)
    if min_moves == []:
        val = mini_max(depth + 1, board, switch_player(player))
        if val[0] < best_value[0]:
            best_value = [val[0], None]
    for move in min_moves:
        cw_move_result = None
        ccw_move_result = None
        if player == 'red':
            cw_move_result = board.red_moves(index=move)  # clockwise move
            ccw_move_result = board.red_moves(index=move, clockwise=False)  # counter-clockwise move
        elif player == 'blue':
            cw_move_result = board.blue_moves(index=move)  # clockwise move
            ccw_move_result = board.blue_moves(index=move, clockwise=False)  # counter-clockwise move
        cw_val = mini_max(depth + 1, Board(cw_move_result[0]), switch_player(player))
        ccw_val = mini_max(depth + 1, Board(ccw_move_result[0]), switch_player(player))
        best_value = [min(cw_val[0], ccw_val[0], best_value[0]), move]
    return best_value


def mini_max(depth, board, player):
    global count
    count +=1
    print('Node: {}'.format(count))
    board.pretty()
    print('payoff {}:'.format(player), heuristics1(board, 'red'))
    if depth > 1 or is_game_over(board.board):
        return [heuristics1(board, player), None]
    if player == 'red':
        return run_max_move(depth, board, player)

    elif player == 'blue':
        return run_mini_move(depth, board, player)


def run_game():
    board = Board()
    print('Initial Board View:')
    board.display()
    global first_player
    first_player = random.choice(['red', 'blue'])
    while not is_game_over(board.board):
        if first_player == 'blue':
            print('Player (Blue) turn:')
            available_moves = get_available_moves(board.board, 'Blue')
            move = int(input('Please choose a hole to move: {} '.format(available_moves)))
            if move not in available_moves:
                print('Invalid move input: {} '.format(move))
                first_player = 'blue'
            else:
                direction = int(input('Please choose a direction to move: 1. clockwise 2. counterclockwise '))
                if direction == 1:
                    direction = True
                elif direction == 2:
                    direction = False
                else:
                    print('Invalid direction input: {} '.format(direction))
                    return
                move_result = board.blue_moves(index=move, clockwise=direction)
                board.run_move(move_result[0])
                if move_result[3] is not None:
                    eat = int(input('Please choose a hole to eat: {} '.format(move_result[3])))
                    if eat not in move_result[3]:
                        print('ERROR INPUT: invalid hole to eat {} '.format(eat))
                        return
                    else:
                        board.eat(player='blue', eat_index=move)
                        first_player = 'red'
                if move_result[2]: # play again is true
                    print('Blue player plays again!')
                    first_player = 'blue'
                else:
                    first_player = 'red'
        elif first_player == 'red':
            print('AI (Red) turn: ', end='')
            move_index = _mini_max(0, board, player='red')[1] # mini_max return (payoff, move_index)
            print('Moving index {}'.format(move_index))
            move_result = board.red_moves(index=move_index)
            board.run_move(move_result[0])

            if move_result[3] is not None:
                most_stones_index = get_most_stones_index(board.board, move_result[3])
                print('AI (Red) eating {})'.format(most_stones_index))
                board.eat(player='red', eat_index=most_stones_index)
                first_player = 'red'

            if move_result[2]:  # play again is true
                print('AI (Red) plays again!')
                first_player = 'red'
            else:
                first_player = 'blue'
        else:
            print('ERROR INPUT @first player {} '.format(first_player))
            break

    print('GAME OVER!')
    board.clear_board()
    calculate_score(board.board)

BOARD = Board()
print(mini_max(0,board=BOARD, player='red'))