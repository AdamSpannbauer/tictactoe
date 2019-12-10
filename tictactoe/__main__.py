import argparse
from .tictactoe import TicTacToe

ap = argparse.ArgumentParser()
ap.add_argument('-d', '--cpu_difficulty', type=int, default=100,
                help='Number in range [0, 100] to set CPU skill level.')
ap.add_argument('-k', '--knowledge', default='cpu_knowledge.pickle',
                help="Path to pickled file to read/save for CPU's knowledge. Ignored if use_saved_knowledge==0")
ap.add_argument('-s', '--use_saved_knowledge', type=int, default=1,
                help='Should knowledge be read/saved to pickled file? (0 if not)')
ap.add_argument('-t', '--train_n_games', type=int, default=0,
                help='Number of games to add to CPU knowledge before playing User.')
ap.add_argument('-c', '--cli', type=int, default=1,
                help='Should CLI be used? (0 if not)')
args = vars(ap.parse_args())
use_saved_knowledge = args['use_saved_knowledge'] != 0
use_cli = args['cli'] != 0

ttt = TicTacToe()
ttt.play(cpu_difficulty=args['cpu_difficulty'],
         use_saved_knowledge=use_saved_knowledge,
         knowledge=args['knowledge'],
         train_n_games=args['train_n_games'],
         cli=use_cli)
