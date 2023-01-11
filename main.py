
import chess.engine
board = chess.Board()

engine = chess.engine.SimpleEngine.popen_uci(["python.exe", "D:/Program Files/JetBrains/ChessAI-AI-P-Soham-and-Nick/SimpleEngine.py"])

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
        result = engine.play(board, chess.engine.Limit(time=0.1))
        board.push(result.move)
engine.quit()

