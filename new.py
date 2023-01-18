import chess
import random
import SpeechRecognition


class ChessEngine:
    def __init__(self):
        self.board = chess.Board()

    def make_move(self):
        """
        Makes a move for the chess engine.
        """
        # get all legal moves
        legal_moves = list(self.board.legal_moves)

        # heuristic 1: prefer captures and checkmating moves
        for move in legal_moves:
            if move.promotion or self.board.is_capture(move) or self.board.is_checkmate():
                return move

        # heuristic 2: prefer moves that open up the center
        center_squares = ["d4", "d5", "e4", "e5"]
        for move in legal_moves:
            if self.board.piece_at(move.from_square).symbol() in ["P", "N", "B", "R"]:
                if chess.square_name(move.to_square) in center_squares:
                    return move

        # heuristic 3: Avoid moving into check
        for move in legal_moves:
            self.board.push(move)
            if self.board.is_check():
                self.board.pop()
                continue
            self.board.pop()

        # heuristic 4:  Prioritize development of minor pieces: Prioritize moves that develop minor pieces (control more
        # squares on the board)
        for move in legal_moves:
            if self.board.piece_at(move.from_square).symbol() in ["N", "B"]:
                return move

        # heursistic 5: Control the center: Prioritize moves that increase control over the center squares
        center_squares = ["d4", "d5", "e4", "e5"]
        for move in legal_moves:
            if chess.square_name(move.to_square) in center_squares:
                return move

        # heursictic 6: Prioritize moves that improves the king safety by castling or moving the king to a safer place.
        if self.board.is_castling(move) or self.board.piece_at(move.from_square).symbol() == "K":
            return move

        # heuristic 7: move a random piece
        return random.choice(legal_moves)

    def play(self):
        while not self.board.is_game_over():
            # check if it's the engine's turn to move
            if self.board.turn == chess.WHITE:
                move = self.make_move()
                print("Engine move:", move)
                self.board.push(move)
            else:
                # get the human's move
                # move = input("Please enter your move (e.g. e2e4): ")
                SpeechRecognition
                try:
                    self.board.push_san(move)
                except ValueError:
                    print("Invalid move, please enter a valid move.")
                    continue

            # Print board after each move
            print(self.board)

        # print the result of the game
        result = self.board.result()
        print(result)

engine = ChessEngine()
engine.play()
