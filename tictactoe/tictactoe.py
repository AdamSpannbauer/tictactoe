import time
import numpy as np
from tqdm import tqdm
from .board_utils import flatten_board, first_person_board, second_person_board, board_diff
from .graph import Graph


class TicTacToe:
    """Play tic-tac-toe with a CPU"""
    _piece_map = {'X': 1, 'O': 2, 1: 'X', 2: 'O'}

    def __init__(self, cpu_knowledge=None):
        self.board = np.array([[0, 0, 0],
                               [0, 0, 0],
                               [0, 0, 0]])
        self.game_is_over = False
        self.winner = 0
        self.last_played_piece = None
        self.last_played_loc = None
        self.cpu_knowledge = Graph() if cpu_knowledge is None else cpu_knowledge

        self.cli = True

    def __repr__(self):
        return self.board.__repr__()

    def __str__(self):
        """Convert numpy array of 0s, 1s, & 2s into a display with Xs and 0s

        Example not run as doctest cause i didnt want to deal with the whitespace
        # >>> ttt = TicTacToe()
        # >>> print(ttt)
           |   |
        ---|---|---
           |   |
        ---|---|---
           |   |
        """
        display = ''
        for row in range(3):
            display += '\n'
            for col in range(3):
                value = self.board[row, col]
                if not value == 0:
                    piece = ' ' + self._piece_map[value] + ' '
                else:
                    piece = '   '

                if col == 1:
                    piece = '|' + piece + '|'

                display += piece

            display += '\n'
            if row < 2:
                display += '---|---|---'

        return display

    @property
    def flat_board(self):
        """Represent TicTacToe board as a flat string

        >>> ttt = TicTacToe()
        >>> ttt.board
        array([[0, 0, 0],
               [0, 0, 0],
               [0, 0, 0]])
        >>> ttt.flat_board
        '000000000'
        """
        return flatten_board(self)

    def reset_game(self, reset_cpu_knowledge=False):
        """Clear board"""
        if reset_cpu_knowledge:
            cpu_knowledge = None
        else:
            cpu_knowledge = self.cpu_knowledge

        self.__init__(cpu_knowledge=cpu_knowledge)

    @staticmethod
    def _three_in_a_row(values):
        """Check if set of 3 has all same nonzero value in it

        :param values: 3 values to check for a win
        """
        return len(np.unique(values)) == 1 and not np.all(values == 0)

    def _game_over(self):
        """Check if game has ended via victory or tie

        * Will return 0 if game is not over or if game has ended in a tie.
          Will set game_is_over attribute to True if board is found to be full with no winner.
        * Will return 1 if there are three 1s in a row (will set game_is_over attribute to True)
        * Will return 2 if there are three 2s in a row (will set game_is_over attribute to True)

        Will return first instance of win found (in case game somehow kept going past first win).
        Order checked:
          * Main diag
          * Opp diag
          * Rows 0->1
          * Columns 0->1
        """

        # No pieces played yet
        if np.all(self.board == 0):
            return 0

        # Winning cases
        diags = [
            self.board.diagonal(),
            np.fliplr(self.board).diagonal()
        ]

        # Check diags
        for diag in diags:
            if self._three_in_a_row(diag):
                self.game_is_over = True
                return np.unique(diag)[0]

        # Check rows
        for row in self.board:
            if self._three_in_a_row(row):
                self.game_is_over = True
                return np.unique(row)[0]

        # Check cols
        for col in self.board.T:
            if self._three_in_a_row(col):
                self.game_is_over = True
                return np.unique(col)[0]

        # No open spots left and no winner
        if np.all(self.board != 0):
            self.game_is_over = True

        return 0

    @staticmethod
    def _get_player_location_cli():
        msg = '\n(x, y) location to place piece?\n(format as x,y where x and y are [0-3] representing col,row):\n'
        input_loc = input(msg)
        return (int(v) for v in input_loc.split(','))

    @staticmethod
    def _get_player_location_gui():
        NotImplementedError('Comeback later...')

    def _get_player_location(self):
        if self.cli:
            return self._get_player_location_cli()
        else:
            return self._get_player_location_gui()

    def place_piece(self, value, position=None):
        """Place a piece at given coords

        :param value: value of piece to place (either 1 or 2)
        :param position: coordinates to place piece as (x, y) on zero indexed 2d grid;
                         if None then position will be prompted via input() if self.cli is True


        >>> ttt = TicTacToe()
        >>> ttt.place_piece(1, (0, 0))
        >>> ttt.board
        array([[1, 0, 0],
               [0, 0, 0],
               [0, 0, 0]])
        >>> # ttt.place_piece(1, (0, 0))
        IndexError: A piece is already placed at that position.
        >>> ttt.game_is_over = True
        >>> # ttt.place_piece(1, (0, 0))
        ValueError: Game is over.
        """
        if self.game_is_over:
            raise ValueError('Game is over.')

        if position is None:
            position = self._get_player_location()

        x, y = position
        if self.board[y, x] == 0:
            self.board[y, x] = value
            self.last_played_loc = position
            self.last_played_piece = value
        else:
            raise IndexError('A piece is already placed at that position.')

        self.winner = self._game_over()

    def place_random_piece(self, value):
        """Place a piece on any open space on board

        :param value: value of piece to randomly place

        >>> np.random.seed(42)
        >>> ttt = TicTacToe()
        >>> ttt.place_random_piece(1)
        >>> ttt.place_random_piece(2)
        >>> ttt.place_random_piece(1)
        >>> ttt.board
        array([[0, 0, 0],
               [2, 0, 1],
               [1, 0, 0]])
        """
        open_spaces = np.where(self.board == 0)
        n_open = len(open_spaces[0])

        if not n_open:
            self.game_is_over = True
        else:
            i = np.random.choice(n_open)
            position = open_spaces[1][i], open_spaces[0][i]

            self.place_piece(value, position)

    def cpu_place_piece(self, value):
        """Have a CPU player place a piece

        If ai has not been trained then this is equivalent to TicTacToe.place_random_piece().
        Train with TicTacToe.train_cpu().

        :param value: value of piece for CPU to place

        >>> np.random.seed(42)
        >>> ttt = TicTacToe()
        >>> ttt.place_piece(1, (0, 0))
        >>> ttt.cpu_place_piece(2)
        >>> ttt.board
        array([[1, 0, 0],
               [0, 0, 0],
               [0, 2, 0]])
        """
        current_board = self.flat_board
        fp_board = first_person_board(current_board, value)
        sp_board = second_person_board(current_board, value)
        try:
            edges = self.cpu_knowledge.nodes[sp_board].edges
        # If move never seen before in knowledge
        except KeyError:
            self.place_random_piece(value=value)
            return

        # Remove negatively weighted moves
        edges = {k: v for k, v in edges.items() if v > 0}
        best_moves = sorted(edges, key=edges.get)
        for move in best_moves:
            position = board_diff(fp_board, move)
            try:
                self.place_piece(value=value, position=position)
                return
            # If desired move isn't an open space
            except IndexError:
                continue

        # If no known moves available
        self.place_random_piece(value=value)

    def train_cpu(self, n_rounds=5000, random_move_percent=0.25):
        """Train CPU AI to play against

        :param n_rounds: Number of rounds for computer to play itself
        :param random_move_percent: Chance for CPU to make random choice rather than best known choice
        :return: None; cpu_knowledge attribute will be modified

        >>> ttt = TicTacToe()
        >>> ttt.cpu_knowledge
        >>> ttt.train_cpu()
        >>> ttt.cpu_knowledge
        """
        # Store moves per player in first person.
        # Will be added to self.cpu_knowledge after each training game and reset
        game_knowledge = [Graph(), Graph()]

        # Player 1 will start
        player = 1
        count = 0
        pbar = tqdm(desc='Training', total=n_rounds)
        while count < n_rounds:
            prev_move = self.flat_board
            # Place piece
            # Randomly decide to ignore knowledge and place randomly
            if np.random.random() <= random_move_percent:
                self.place_random_piece(value=player)
            else:
                self.cpu_place_piece(player)
            current_move = self.flat_board

            # Store move for player of interest
            # Example: game_knowledge[0].add_nodes(names=['000000000'], edges=[{'000000001': 0}])
            game_knowledge[player - 1].add_nodes(
                [second_person_board(prev_move, player)],
                [{first_person_board(current_move, player): 0}]
            )

            # Change to other player's turn
            player = 1 if player == 2 else 2

            # Consolidate knowledge after round
            if self.game_is_over:
                count += 1
                pbar.update(1)
                if self.winner is not 0:  # 0 means a tie
                    winning_ind = self.winner - 1
                    winning_moves = game_knowledge[winning_ind]
                    losing_moves = game_knowledge[int(not winning_ind)]

                    winning_moves.set_all_weights(5)
                    losing_moves.set_all_weights(-5)

                    self.cpu_knowledge.merge(winning_moves)
                    self.cpu_knowledge.merge(losing_moves)
                else:
                    tie_moves_1 = game_knowledge[0]
                    tie_moves_2 = game_knowledge[1]

                    tie_moves_1.set_all_weights(0)
                    tie_moves_2.set_all_weights(0)

                    self.cpu_knowledge.merge(tie_moves_1)
                    self.cpu_knowledge.merge(tie_moves_2)

                # Reset for next round
                self.reset_game()
                game_knowledge = [Graph(), Graph()]
                player = 1

        pbar.close()
        self.reset_game()

    def _play_cli(self):
        msg = '\nWhich piece would you like to be?\n(X or O; Xs will play first):\n'
        player_piece = input(msg).strip().upper()
        cpu_piece = 'O'

        if player_piece in ['O', '0']:
            player_piece = 'O'
            cpu_piece = 'X'
        elif player_piece is not 'X':
            ValueError('Bad piece selection.')

        player_piece = self._piece_map[player_piece]
        cpu_piece = self._piece_map[cpu_piece]

        turn_actions = {
            cpu_piece: lambda: self.cpu_place_piece(cpu_piece),
            player_piece: lambda: self.place_piece(player_piece, position=None),
        }

        turn = 1
        next_turn = {1: 2, 2: 1}
        while not self.game_is_over:
            turn_actions[turn]()
            print(f'\n{self._piece_map[turn]} played:')
            print(self)
            turn = next_turn[turn]
            time.sleep(0.3)

        try:
            display_winner = self._piece_map[self.winner]
        except KeyError:
            display_winner = 'No one'
        print(f'Game Over. {display_winner} wins.')

        self.reset_game()

        while True:
            play_again = input('\nPlay again? (y or n): ').upper() == 'Y'
            if play_again:
                ttt.play()
            else:
                break

    @staticmethod
    def _play_gui():
        NotImplementedError('Come back later...')

    def play(self, cli=True):
        self.cli = cli
        if cli:
            self._play_cli()
        else:
            self._play_gui()


if __name__ == '__main__':
    ttt = TicTacToe()
    ttt.train_cpu(100)
    ttt.play()
