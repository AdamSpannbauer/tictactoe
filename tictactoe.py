import numpy as np
import board_utils


class TicTacToe:
    """Play tic-tac-toe with 1s and 2s instead of Xs and Os"""
    def __init__(self):
        self.board = np.array([[0, 0, 0],
                               [0, 0, 0],
                               [0, 0, 0]])
        self.game_is_over = False
        self.winner = 0
        self.last_played_piece = None
        self.last_played_loc = None

    def __repr__(self):
        return self.board.__repr__()

    def __str__(self):
        return self.board.__str__()

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
        return board_utils.flatten_board(self)

    def reset_game(self):
        """Clear board"""
        self.__init__()

    def place_piece(self, value, position):
        """Place a piece at given coords

        :param value: value of piece to place (either 1 or 2)
        :param position: coordinates to place piece as (x, y) on zero indexed 2d grid

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
