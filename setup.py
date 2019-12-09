from setuptools import setup

version = {}
with open("tictactoe/version.py") as f:
    exec(f.read(), version)

setup(name='tictactoe',
      version=version['__version__'],
      description='TicTacToe with CPU implementation.',
      author='Adam Spannbauer',
      author_email='spannbaueradam@gmail.com',
      url='https://github.com/AdamSpannbauer/tictactoe',
      packages=['tictactoe'],
      license='MIT',
      install_requires=[
          'numpy',
          'mgsub',
          'tqdm',
      ],
      )
