import chess
board = chess.Board()

# this does not work like that
# engine = chess.engine.SimpleEngine.popen_uci(["python.exe", "D:/Program Files/JetBrains/ChessAI-AI-P-Soham-and-Nick/SimpleEngine.py"])
from new import ChessEngine
engine = ChessEngine


engine.play()
engine.quit()

