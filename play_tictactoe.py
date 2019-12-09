from tictactoe import TicTacToe

ttt = TicTacToe()
ttt.play(cpu_difficulty=100,
         knowledge='cpu_knowledge.pickle',
         train_n_games=100)
