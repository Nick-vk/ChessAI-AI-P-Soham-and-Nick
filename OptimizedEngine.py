import chess
import chess.polyglot
import chess.svg
import webbrowser
# import chess.pgn
import os
from SpeechToText import SpeechRecognition
from flask import Flask, Response

app = Flask(__name__)

sr = SpeechRecognition
# Change to your file destination
opening_book = "D:/Program Files/chess/opnening books/computer.bin"

# from chessboard import display
# from IPython.display import SVG


# heuristic tables per piece
pawns_table = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, -20, -20, 10, 10, 5,
    5, -5, -10, 0, 0, -10, -5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, 5, 10, 25, 25, 10, 5, 5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0]

knights_table = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50]
bishops_table = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20]
rooks_table = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0]
queens_table = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 5, 5, 5, 5, 5, 0, -10,
    0, 0, 5, 5, 5, 5, 0, -5,
    -5, 0, 5, 5, 5, 5, 0, -5,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20]
kings_table = [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30]


class SimpleEngine:
    def __init__(self):
        self.board = chess.Board()

    @app.route('/board.svg')
    def image(self):
        with open("board.svg", "rb") as f:
            return Response(f.read(), content_type="image/svg+xml")

    if __name__ == '__main__':
        app.run()
    # check end state of game
    def evaluate_board(self):
        if self.board.is_checkmate():
            return float("-inf") if self.board.turn else float("inf")
        elif self.board.is_stalemate() or self.board.is_insufficient_material():
            return 0

        # calculate_pieces
        piece_counts = {chess.PAWN: {chess.WHITE: 0, chess.BLACK: 0},
                        chess.KNIGHT: {chess.WHITE: 0, chess.BLACK: 0},
                        chess.BISHOP: {chess.WHITE: 0, chess.BLACK: 0},
                        chess.ROOK: {chess.WHITE: 0, chess.BLACK: 0},
                        chess.QUEEN: {chess.WHITE: 0, chess.BLACK: 0}}
        for piece_type in piece_counts.keys():
            for color in [chess.WHITE, chess.BLACK]:
                piece_counts[piece_type][color] = len(self.board.pieces(piece_type, color))

        # calculate_scores
        material = 100 * (piece_counts[chess.PAWN][chess.WHITE] - piece_counts[chess.PAWN][chess.BLACK]) + 320 * (
                    piece_counts[chess.KNIGHT][chess.WHITE] - piece_counts[chess.KNIGHT][chess.BLACK]) + 330 * (
                    piece_counts[chess.BISHOP][chess.WHITE] - piece_counts[chess.BISHOP][chess.BLACK]) + 500 * (
                    piece_counts[chess.ROOK][chess.WHITE] - piece_counts[chess.ROOK][chess.BLACK]) + 900 * (
                    piece_counts[chess.QUEEN][chess.WHITE] - piece_counts[chess.QUEEN][chess.BLACK])

        pawn_score = sum([pawns_table[i] for i in self.board.pieces(chess.PAWN, chess.WHITE)])
        pawn_score += sum([-pawns_table[chess.square_mirror(i)] for i in self.board.pieces(chess.PAWN, chess.BLACK)])
        knight_score = sum([knights_table[i] for i in self.board.pieces(chess.KNIGHT, chess.WHITE)])
        knight_score += sum([-knights_table[chess.square_mirror(i)] for i in self.board.pieces(chess.KNIGHT, chess.BLACK)])
        bishop_score = sum([bishops_table[i] for i in self.board.pieces(chess.BISHOP, chess.WHITE)])
        bishop_score += sum([-bishops_table[chess.square_mirror(i)] for i in self.board.pieces(chess.BISHOP, chess.BLACK)])
        rook_score = sum([rooks_table[i] for i in self.board.pieces(chess.ROOK, chess.WHITE)])
        rook_score += sum([-rooks_table[chess.square_mirror(i)] for i in self.board.pieces(chess.ROOK, chess.BLACK)])
        queen_score = sum([queens_table[i] for i in self.board.pieces(chess.QUEEN, chess.WHITE)])
        queen_score += sum([-queens_table[chess.square_mirror(i)] for i in self.board.pieces(chess.QUEEN, chess.BLACK)])
        king_score = sum([kings_table[i] for i in self.board.pieces(chess.KING, chess.WHITE)])
        king_score += sum([-kings_table[chess.square_mirror(i)] for i in self.board.pieces(chess.KING, chess.BLACK)])
        knight_score = knight_score + sum(
            [-knights_table[chess.square_mirror(i)] for i in self.board.pieces(chess.KNIGHT, chess.BLACK)])
        bishop_score = sum([bishops_table[i] for i in self.board.pieces(chess.BISHOP, chess.WHITE)])
        bishop_score = bishop_score + sum(
            [-bishops_table[chess.square_mirror(i)] for i in self.board.pieces(chess.BISHOP, chess.BLACK)])
        rook_score = sum([rooks_table[i] for i in self.board.pieces(chess.ROOK, chess.WHITE)])
        rook_score = rook_score + sum(
            [-rooks_table[chess.square_mirror(i)] for i in self.board.pieces(chess.ROOK, chess.BLACK)])
        queen_score = sum([queens_table[i] for i in self.board.pieces(chess.QUEEN, chess.WHITE)])
        queen_score = queen_score + sum(
            [-queens_table[chess.square_mirror(i)] for i in self.board.pieces(chess.QUEEN, chess.BLACK)])
        king_score = sum([kings_table[i] for i in self.board.pieces(chess.KING, chess.WHITE)])
        king_score = king_score + sum(
            [-kings_table[chess.square_mirror(i)] for i in self.board.pieces(chess.KING, chess.BLACK)])

        # evaluate position
        eval = material + pawn_score + knight_score + bishop_score + rook_score + queen_score + king_score
        return eval if self.board.turn else -eval

    def alphabeta(self, alpha, beta, depthleft):
        # Order moves based on their potential to improve alpha
        moves = self.board.legal_moves
        moves = sorted(moves, key=lambda move: -self.evaluate_move(move))

        best_score = float("-inf")
        if depthleft == 0:
            return self.quiesce(alpha, beta)

        for move in moves:
            self.board.push(move)
            score = -self.alphabeta(-beta, -alpha, depthleft - 1)
            self.board.pop()

            if score >= beta:
                return score
            if score > best_score:
                best_score = score
            if score > alpha:
                alpha = score

            # alpha-beta pruning
            if alpha >= beta:
                break

        return best_score

    def quiesce(self, alpha, beta):
        stand_pat = self.evaluate_board()
        if stand_pat >= beta:
            return beta
        if alpha < stand_pat:
            alpha = stand_pat
        for move in self.board.legal_moves:
            if self.board.is_capture(move):
                self.board.push(move)
                score = -self.quiesce(-beta, -alpha)
                self.board.pop()

                if score >= beta:
                    return beta
                if score > alpha:
                    alpha = score
        return alpha

    def evaluate_move(self, move):
        self.board.push(move)
        score = 0
        # prefer moves that are promotion or capture or checkmate
        if move.promotion or self.board.is_capture(move):
            score += 2
        # prefer moves that are castling
        if self.board.is_castling(move):
            score += 1
        # suspend moves that lead to being checked
        if self.board.is_check():
            score -= 2
        self.board.pop()
        return score

    def try_moves(self, depth):
        # change to your file location
        if not os.path.exists(opening_book):
            print("Opening book not found")
        try:
            # change to your file location
            move = chess.polyglot.MemoryMappedReader(opening_book).weighted_choice(
                self.board).move
            return move
        except:
            best_move = chess.Move.null()
            best_value = float("-inf")
            alpha = float("-inf")
            beta = float("inf")
            for move in self.board.legal_moves:
                self.board.push(move)
                board_value = -self.alphabeta(-beta, -alpha, depth - 1)
                if board_value > best_value:
                    best_value = board_value
                    best_move = move
                if board_value > alpha:
                    alpha = board_value
                self.board.pop()
            return best_move

    def launch(self):
        # depth = int(input("Depth: "))
        # print("Enter the desired depth: ")
        depth = int(sr().speech_to_text())
        print("depth set to", depth)
        # if not depth.isdigit():
        # print("Depth needs to be an integer")

        color = input("Please enter the engine's color: ")
        # print("Please enter the engine's color: ")
        # color = sr().speech_to_text()
        if color == "w":
            print("engine color set to white")
            self.play(depth, "w")
        elif color == "b":
            print("engine color set to black")
            self.play(depth, "b")
        else:
            print("Invalid color, please enter a letter like w or b")
            self.launch()

    def play(self, depth, engine_color, listening_time):
        while not self.board.is_game_over():
            if (self.board.turn == chess.WHITE and engine_color == "b") or (self.board.turn == chess.BLACK and engine_color == "w"):
                # type as move input
                # move = input("Please enter your move: ")
                # speech to text as move input
                move = sr().speech_to_text(listening_time)
                try:
                    self.board.push_san(move)
                    self.display_board(self.board)
                except ValueError:
                    print("Invalid mode, please enter a valid move.")
            else:
                move = self.try_moves(depth)
                print("Engine move: ", move)
                self.board.push(move)
                self.display_board(self.board)
            # print board after each move and result after the game ends
            print(self.board)
            # print(chess.svg.board(self.board, size=350))
            # display.update(move)
        # chess.svg.board(self.board, size=350)
        print(self.board.result)
        # display.update(self.board.fen())

    def display_board(self, board):
        svg = chess.svg.board(board=board)
        with open("board.svg", "w") as f:
            f.write(svg)

        webbrowser.open("board.svg")

# SimpleEngine().launch(listening_time)
