# TODO: finish refactoring this and move cpu into TicTacToe class
import random
import logging
from graph import Graph
from tictactoe import TicTacToe
import board_utils

logger = logging.getLogger(__name__)


def cpu_place_piece(tictactoe, value, knowledge_graph):
    current_board = board_utils.flatten_board(tictactoe)
    fp_board = board_utils.first_person_board(current_board, value)
    sp_board = board_utils.second_person_board(current_board, value)
    try:
        edges = knowledge_graph.nodes[sp_board].edges
    # If move never seen before
    except KeyError:
        tictactoe.place_random_piece(value=value)
        return

    # rm negatively weighted moves
    edges = {k: v for k, v in edges.items() if v > 0}
    best_moves = sorted(edges, key=edges.get)
    for move in best_moves:
        position = board_utils.board_diff(fp_board, move)
        try:
            tictactoe.place_piece(value=value, position=position)
            return
        # If desired move isn't an open space
        except IndexError:
            continue

    # If no known moves available
    tictactoe.place_random_piece(value=value)


def train(log_every_n=1000):
    # Storage for move history and learning which are good
    # Store all moves in first person
    all_knowledge = Graph()
    # Store moves per player in first person.
    # Will be added to all_knowledge after each training game and reset
    game_knowledge = [Graph(), Graph()]

    ttt = TicTacToe()

    # Player 1 will start each round
    player = 1
    # Keep tally of wins and losses
    record = {0: 0, 1: 0, 2: 0}
    count = 0
    n_rounds = 50000
    while True:
        prev_move = ttt.flat_board
        # Place piece
        # Randomly decide to ignore knowledge and place randomly
        if random.random() >= 0.75:
            ttt.place_random_piece(value=player)
        else:
            cpu_place_piece(ttt, player, all_knowledge)
        current_move = ttt.flat_board

        # Store move for player of interest
        game_knowledge[player - 1].add_nodes(
            [board_utils.second_person_board(prev_move, player)],
            [{board_utils.first_person_board(current_move, player): 0}]
        )

        # Change to other players turn
        player = 1 if player == 2 else 2

        # Consolidate knowledge after round
        if ttt.game_is_over:
            # Keep score
            record[ttt.winner] += 1

            # Show score
            count += 1
            if count > n_rounds:
                break
            elif count % log_every_n == 0:
                logger.info(f'\nCPU 1 vs CPU 2 record after {count} rounds (0 is tie)')
                logger.info(record)

            if ttt.winner is not 0:  # 0 means a tie
                winning_ind = ttt.winner - 1
                winning_moves = game_knowledge[winning_ind]
                losing_moves = game_knowledge[int(not winning_ind)]

                winning_moves.set_all_weights(5)
                losing_moves.set_all_weights(-5)

                all_knowledge.merge(winning_moves)
                all_knowledge.merge(losing_moves)
            else:
                tie_moves_1 = game_knowledge[0]
                tie_moves_2 = game_knowledge[1]

                tie_moves_1.set_all_weights(0)
                tie_moves_2.set_all_weights(0)

                all_knowledge.merge(tie_moves_1)
                all_knowledge.merge(tie_moves_2)

            ttt.reset_game()
            game_knowledge = [Graph(), Graph()]
            player = 1
