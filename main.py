import chess
from OptimizedEngine import SimpleEngine

board = chess.Board()
engine = SimpleEngine()
listening_time = 5

engine.launch(listening_time)
