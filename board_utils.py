from mgsub import mgsub


def flatten_board(self):
    """Convert numpy array board to str

          2d board              1d board
    np.array([[0, 0, 0],
              [0, 0, 0],  --> '000000000'
              [0, 0, 0]]
    """
    return ''.join(self.board.astype('str').flatten())


def invert_board(flat_board):
    """Used to change all Xs to Os and vice versa

    Used by `first_person_board()` and `second_person_board()` functions.
    Implemented so 'AI' can 'learn' from every move rather than every other move
    (i.e. AI will always see itself as piece 1 regardless of if its X or O).

    >>> invert_board('110200000')
    '220100000'
    """
    return mgsub([flat_board], ['1', '2'], ['2', '1'])[0]


def first_person_board(flat_board, piece_value=1):
    """Ensure board is in first person view for piece_value of interest

    First person view of the board here means the player of interest's pieces are all 1s.
    The other player's pieces are all 2s. POV indicates what piece of interest we are.

    >>> first_person_board('110200000', 1)
    '110200000'
    >>> first_person_board('110200000', 2)
    '220100000'
    """
    if piece_value == 1:
        return flat_board
    else:
        return invert_board(flat_board)


def second_person_board(flat_board, pov=1):
    """Ensure board is in first person view for pov of interest

    First person view of the board here means the player of interest's pieces are all 1s.
    The other player's pieces are all 2s.  POV indicates what piece of interest we are.

    >>> second_person_board('110200000', 1)
    '220100000'
    >>> second_person_board('110200000', 2)
    '110200000'
    """
    if pov == 2:
        return flat_board
    else:
        return invert_board(flat_board)


def board_diff(prev, cur):
    """Find location in board where a new piece was added

    Looks for a place where prev board equals 0 and cur board is non zero.
    Assumes strings to both be len 9 (to match tictactoe board).

    Input is 1d but output is based on position in 2d grid.
    For example, the output of board_diff('110200000', '112200000') is (2, 0).
    This corresponds to the 3rd column 1st row where the 2 differ if mapped to
    a 2d (3x3) tictactoe grid.  Below is the 2d representation of the example
    comparison where (2, 0) is the expected output.

    array([[1, 1, 2],       array([[1, 1, 0],
           [2, 0, 0],              [2, 0, 0],
           [0, 0, 0]])             [0, 0, 0]])

    :param prev: flattened board string (i.e. '110200000')
    :param cur: flattened board string (i.e. '112200000')
    :return: position in 2d (3x3) np array where boards are different.
             If multiple places where different, only the first is returned.
             If no differences, then None is returned.

    >>> board_diff('110200000', '112200000')
    (2, 0)
    >>> board_diff('110200000', '110200000')

    """
    i = 0
    for row in range(3):
        for col in range(3):
            if prev[i] == '0' and not cur[i] == '0':
                return col, row
            else:
                i += 1
