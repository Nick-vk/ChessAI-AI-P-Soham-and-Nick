import chess
import random


def make_move(board):
    """
    Makes a move for the chess engine.
    """
    # get all legal moves
    legal_moves = list(board.legal_moves)

    # heuristic 1: prefer captures and checkmating moves
    for move in legal_moves:
        if move.promotion or board.is_capture(move) or board.is_checkmate():
            return move

    # heuristic 2: prefer moves that open up the center
    center_squares = ["d4", "d5", "e4", "e5"]
    for move in legal_moves:
        if board.piece_at(move.from_square).symbol() in ["P", "N", "B", "R"]:
            if chess.square_name(move.to_square) in center_squares:
                return move

    # heuristic 3: Avoid moving into check
    for move in legal_moves:
        board.push(move)
        if board.is_check():
            board.pop()
            continue
        board.pop()

    # heuristic 4:  Prioritize development of minor pieces: Prioritize moves that develop minor pieces (control more
    # squares on the board)
    for move in legal_moves:
        if board.piece_at(move.from_square).symbol() in ["N", "B"]:
            return move

    # heursistic 5: Control the center: Prioritize moves that increase control over the center squares
    center_squares = ["d4", "d5", "e4", "e5"]
    for move in legal_moves:
        if chess.square_name(move.to_square) in center_squares:
            return move

    # heursictic 6: Prioritize moves that improves the king safety by castling or moving the king to a safer place.
    if board.is_castling(move) or board.piece_at(move.from_square).symbol() == "K":
        return move

    # heuristic 7: move a random piece
    return random.choice(legal_moves)


# create a chess board
board = chess.Board()

while not board.is_game_over():
    # check if it's the engine's turn to move
    if board.turn == chess.WHITE:
        move = make_move(board)
        print("Engine move:", move)
        board.push(move)
    else:
        # get the human's move
        move = input("Please enter your move (e.g. e2e4): ")
        board.push_san(move)

    # Print board after each move
    print(board)

# print the result of the game
result = board.result()
print(result)
