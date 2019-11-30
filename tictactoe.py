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
        return board_utils.flatten_board(self.board)

    def reset_game(self):
        """Clear board"""
        self.__init__()

    def place_piece(self, value, position):
        """Place a piece at given coords

        :param value: value of piece to place (either 1 or 2)
        :param position: coordinates to place piece as (x, y) on zero indexed 2d grid
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
        """Place a piece on any open space on board"""
        open_spaces = np.where(self.board == 0)

        if not open_spaces:
            self.game_is_over = True
        else:
            n = len(open_spaces[0])
            i = np.random.choice(n + 1)
            position = open_spaces[1][i], open_spaces[0][i]

            self.place_piece(value, position)

    @staticmethod
    def _three_in_a_row(values):
        """Check if set of 3 has all same nonzero value in it"""
        return len(np.unique(values)) == 1 and not np.all(values == 0)

    def _game_over(self):
        """Check if game has ended via victory or tie"""

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
