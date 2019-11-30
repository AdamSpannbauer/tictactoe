import numpy as np


class TicTacToe:
    def __init__(self):
        self.board = np.array([[0, 0, 0],
                               [0, 0, 0],
                               [0, 0, 0]])
        self.game_is_over = False
        self.winner = 0

    def __str__(self):
        return self.board.__str__()

    def reset_game(self):
        self.__init__()

    def place_piece(self, value, position):
        if self.game_is_over:
            raise ValueError('Game is over.')

        x, y = position
        if self.board[y, x] == 0:
            self.board[y, x] = value
        else:
            raise IndexError('A piece is already placed at that position.')

        self.winner = self._game_over()

    def place_random_piece(self, value):
        open_spaces = np.where(self.board == 0)

        if not open_spaces:
            self.game_is_over = True
        else:
            i = np.random.choice(range(len(open_spaces[0])))
            position = open_spaces[1][i], open_spaces[0][i]

            self.place_piece(value, position)

    @staticmethod
    def _three_in_a_row(values):
        return len(np.unique(values)) == 1 and not np.all(values == 0)

    def _game_over(self):
        if np.all(self.board == 0):
            return 0
        if np.all(self.board != 0):
            self.game_is_over = True
            return 0

        diags = [
            self.board.diagonal(),
            np.fliplr(self.board).diagonal()
        ]

        for diag in diags:
            if self._three_in_a_row(diag):
                self.game_is_over = True
                return np.unique(diag)[0]

        for row in self.board:
            if self._three_in_a_row(row):
                self.game_is_over = True
                return np.unique(row)[0]

        for col in self.board.T:
            if self._three_in_a_row(col):
                self.game_is_over = True
                return np.unique(col)[0]

        return 0
