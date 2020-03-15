import random
from board import Board, RED_HOLES, RED_MANCALA, BLUE_MANCALA, BLUE_HOLES, N


# TODO: def heuristics1()

# TODO: def heuristics2()

# TODO: MiniMax():
# TODO: Alpha_Beta():
# TODO: calculate_point():

def payoff(board, player):
    board = board.board
    if player == 'red':
        # new_board.red_moves(move, clockwise=True)
        return (board[0] + board[12]) - (board[6] + board[18])
    else:
        return (board[6] + board[18]) - (board[0] + board[12])


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
def mini_max(depth, board, player):
    global count
    count +=1
    print('Node: {}'.format(count))
    board.pretty()
    print("payoff {}:".format(player), payoff(board, player))
    if depth > 1 or is_game_over(board.board):
        return payoff(board,player), None
    if player == 'red':
        best_value = (-10 * N), None  # best_value (score, move)
        max_moves = get_available_moves(board.board, 'red')
        if max_moves == []:
            val = mini_max(depth+1, board, 'blue')
            if val[0] > best_value[0]:
                best_value = val[0], None
        for move in max_moves:
            cw_move_result = board.red_moves(index=move) # clockwise move
            ccw_move_result = board.red_moves(index=move, clockwise=False) # counter-clockwise move

            cw_val = mini_max(depth+1, Board(cw_move_result[0]), 'blue')
            ccw_val = mini_max(depth + 1, Board(ccw_move_result[0]), 'blue')
            best_value = max(cw_val[0], ccw_val[0], best_value[0]), move
        return best_value

    elif player == 'blue':
        best_value = (10 * N), None
        min_moves = get_available_moves(board.board, 'blue')
        if min_moves == []:
            val = mini_max(depth + 1, board, 'red')
            if val[0] < best_value[0]:
                best_value = val[0], None
        for move in min_moves:
            cw_move_result = board.red_moves(index=move)  # clockwise move
            ccw_move_result = board.red_moves(index=move, clockwise=False)  # counter-clockwise move
            cw_val = mini_max(depth + 1, Board(cw_move_result[0]), 'red')
            ccw_val = mini_max(depth + 1, Board(ccw_move_result[0]), 'red')
            best_value = min(cw_val[0], ccw_val[0], best_value[0]), move
        return best_value


def run_game():
    board = Board()
    board.display()
    global first_player
    first_player = random.choice(['red', 'blue'])
    print('{} turn'.format(first_player))
    while not is_game_over(board.board):
        if first_player == 'red':
            available_moves = get_available_moves(board.board, 'red')
            move = int(input('Please choose a hole to move: {} '.format(available_moves)))
            if move not in available_moves:
                print('Invalid move input: {} '.format(move))
                return
            direction = int(input('Please choose a direction to move: 1. clockwise 2. counterclockwise '))
            if direction == 1:
                direction = True
            elif direction == 2:
                direction = False
            else:
                print('Invalid direction input: {} '.format(direction))
                return
            move_result = board.red_moves(index=move, clockwise=direction)
            board.run_move(move_result[0])
            if move_result[3] is not None:
                eat = int(input('Please choose a hole to eat: {} '.format(move_result[3])))
                if eat not in move_result[3]:
                    print('ERROR INPUT: invalid hole to eat {} '.format(eat))
            if move_result[2]: # play again is true
                first_player = 'red'
                return
            first_player = 'blue'
        elif first_player == 'blue':
            print('AI (blue) turn:')
            move_index = mini_max(0, board, player='blue')[1] # mini_max return (payoff, move_index)
            move_result = board.blue_moves(index=move_index)
            board.run_move(move_result[0])
            first_player = 'red'
            return
        else:
            print('ERROR INPUT @first player {} '.format(first_player))
            break
    print('GAME OVER!')

run_game()
