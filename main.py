import chess
board = chess.Board()

# this does not work like that
# engine = chess.engine.SimpleEngine.popen_uci(["python.exe", "D:/Program Files/JetBrains/ChessAI-AI-P-Soham-and-Nick/SimpleEngine.py"])
from new import ChessEngine
engine = ChessEngine


while not board.is_game_over():
    if board.turn:
        print(board)
        print("Enter your move:")
        move = input()
        try:
            board.push_uci(move)
        except:
            print("Invalid move. Please enter a valid move.")
    else:
        result = engine.make_move
        board.push(result)
engine.quit()

