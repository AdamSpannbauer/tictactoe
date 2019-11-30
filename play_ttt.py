import random
import difflib
from mgsub import mgsub
from graph import Graph
from tictactoe import TicTacToe


def flatten_board(tictactoe):
    """Convert numpy array board to str"""
    return ''.join(tictactoe.board.astype('str').flatten())


def invert_board(flat_board):
    """Used to change all Xs to Os and vice versa

    Used so 'AI' can 'learn' from every move rather than every other move

    >>> invert_board('110200000')
    '220100000'
    """
    return mgsub([flat_board], ['1', '2'], ['2', '1'])[0]


def first_person_board(flat_board, piece_value=1):
    """Ensure board is in first person view for piece_value of interest

    First person view of the board here means the player of interest's pieces are all 1s.
    The other player's pieces are all 2s.

    >>> first_person_board('110200000', 1)
    '110200000'
    >>> first_person_board('110200000', 2)
    '220100000'
    """
    if piece_value == 1:
        return flat_board
    else:
        return invert_board(flat_board)


def second_person_board(flat_board, piece_value=1):
    """Ensure board is in first person view for piece_value of interest

    First person view of the board here means the player of interest's pieces are all 1s.
    The other player's pieces are all 2s.

    >>> second_person_board('110200000', 1)
    '220100000'
    >>> second_person_board('110200000', 2)
    '110200000'
    """
    if piece_value == 2:
        return flat_board
    else:
        return invert_board(flat_board)


def board_diff(prev, cur):
    i = [i + 1 for i, a, b in enumerate(zip(prev, cur)) if a != b]
    for row in range(3):
        for col in range(3):
            if prev[i] == 0 and not cur[i] == 0:
                return col, row
            else:
                i += 1


def cpu_place_piece(tictactoe, value, move_history, print_flag=False):
    current_board = flatten_board(tictactoe)
    fp_board = first_person_board(current_board, value)
    sp_board = second_person_board(current_board, value)
    try:
        edges = move_history.nodes[sp_board].edges
    except KeyError:  # If move never seen before
        # print('Never seen board before.')
        tictactoe.place_random_piece(value=value)
        if print_flag:
            print('\nCPU has played (Never seen before):')
            print(tictactoe)
        return

    # rm negatively weighted moves
    edges = {k: v for k, v in edges.items() if v > 0}
    best_moves = sorted(edges, key=edges.get)
    for move in best_moves:
        position = board_diff(fp_board, move)
        try:
            tictactoe.place_piece(value=value, position=position)
            if print_flag:
                print('\nCPU has played:')
                print(tictactoe)
            return
        except IndexError:  # If position unavailable
            continue

    # print('No known moves available')
    tictactoe.place_random_piece(value=value)
    if print_flag:
        print('\nCPU has played (No known avail):')
        print(tictactoe)


def player_place_piece(tictactoe, value, print_flag=True):
    x = input('\nPlace piece in col ("exit" to quit): ')
    y = input('Place piece in row ("exit" to quit): ')

    if x == 'exit' or y == 'exit':
        return True

    x = int(x)
    y = int(y)

    tictactoe.place_piece(value, (x, y))
    if print_flag:
        print('\nPlayer has played:')
        print(ttt)


all_moves = Graph()
ttt = TicTacToe()
player_moves = [Graph(), Graph()]

player = 0
record = {0: 0, 1: 0, 2: 0}
count = 0
n_rounds = 50000
while True:
    piece = player + 1

    prev_move = flatten_board(ttt)
    if random.random() >= 0.75:
        ttt.place_random_piece(value=piece)
    else:
        cpu_place_piece(ttt, piece, all_moves)
    current_move = flatten_board(ttt)

    player_moves[player].add_nodes([second_person_board(prev_move, piece)],
                                   [{first_person_board(current_move, piece): 0}])

    prev_move = current_move
    if player == 0:
        player = 1
    else:
        player = 0

    if ttt.game_is_over:
        record[ttt.winner] += 1

        count += 1
        if count > n_rounds:
            break
        elif count % 1000 == 0:
            print(f'\nCPU 1 vs CPU 2 record after {count} rounds (0 is tie)')
            print(record)

        if ttt.winner is not 0:  # 0 means a tie
            winning_ind = ttt.winner - 1
            winning_moves = player_moves[winning_ind]
            losing_moves = player_moves[int(not winning_ind)]

            winning_moves.set_all_weights(5)
            losing_moves.set_all_weights(-5)

            all_moves.merge(winning_moves)
            all_moves.merge(losing_moves)
        else:
            tie_moves_1 = player_moves[0]
            tie_moves_2 = player_moves[1]

            tie_moves_1.set_all_weights(0)
            tie_moves_2.set_all_weights(0)

            all_moves.merge(tie_moves_1)
            all_moves.merge(tie_moves_2)

        ttt.reset_game()
        player_moves = [Graph(), Graph()]
        player = 0

print('Trained!')

ttt = TicTacToe()
print(ttt)

while True:
    player_place_piece(ttt, 1)
    try:
        cpu_place_piece(ttt, 2, all_moves, print_flag=True)
    except ValueError:  # game is over
        pass

    if ttt.game_is_over:
        if ttt.winner == 1:
            print('\nPlayer Won!!')
        elif ttt.winner == 2:
            print('\nCPU Won!!')
        else:
            print('\nTie')

        ttt.reset_game()

        print('\n\nNew Game')
        print(ttt)
