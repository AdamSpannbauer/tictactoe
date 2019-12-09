import os
import pickle
from tictactoe import TicTacToe

# Saved off game knowledge of CPU
CPU_KNOWLEDGE_PATH = 'cpu_knowledge.pickle'
TRAIN_N_GAMES = 0

# Read saved knowledge if it exists
cpu_knowledge = None
if os.path.exists(CPU_KNOWLEDGE_PATH):
    with open(CPU_KNOWLEDGE_PATH, 'rb') as f:
        cpu_knowledge = pickle.load(f)

# Add N games to CPU knowledge and play vs user
ttt = TicTacToe(cpu_knowledge=cpu_knowledge)
ttt.train_cpu(TRAIN_N_GAMES)
ttt.play()

# Save what CPU learned
with open(CPU_KNOWLEDGE_PATH, 'wb') as f:
    pickle.dump(ttt.cpu_knowledge, f, protocol=pickle.HIGHEST_PROTOCOL)
