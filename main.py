# program by Soham Nanwani (sXXXXXXX) & Nick van Koeverden (s2880709)
# using python-chess
# using speech-recognition
    # using PyAudio
# using webbrowser
# using os

# sources of code and inspiration:
# https://www.chessprogramming.org/Alpha-Beta
# https://en.wikipedia.org/wiki/Quiescence_search
# https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
# https://en.wikipedia.org/wiki/Negamax
# https://www.freecodecamp.org/news/simple-chess-ai-step-by-step-1d55a9266977/
# https://medium.com/dscvitpune/lets-create-a-chess-ai-8542a12afef

from OptimizedEngine import SimpleEngine

engine = SimpleEngine()
board = engine.board

engine.launch()
