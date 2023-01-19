import chess
import chess.polyglot
import chess.svg
import chess.pgn
import os
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

    # check end state of game
    def evaluate_board(self):
        if self.board.is_checkmate():
            return -9999 if self.board.turn else 9999
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
        material = 100 * (piece_counts[chess.PAWN][chess.WHITE] - piece_counts[chess.PAWN][chess.BLACK]) + 320 * (piece_counts[chess.KNIGHT][chess.WHITE] - piece_counts[chess.KNIGHT][chess.BLACK]) + 330 * (piece_counts[chess.BISHOP][chess.WHITE] - piece_counts[chess.BISHOP][chess.BLACK]) + 500 * (piece_counts[chess.ROOK][chess.WHITE] - piece_counts[chess.ROOK][chess.BLACK]) + 900 * (piece_counts[chess.QUEEN][chess.WHITE] - piece_counts[chess.QUEEN][chess.BLACK])

        pawnsq = sum([pawns_table[i] for i in self.board.pieces(chess.PAWN, chess.WHITE)])
        pawnsq += sum([-pawns_table[chess.square_mirror(i)] for i in self.board.pieces(chess.PAWN, chess.BLACK)])
        knightsq = sum([knights_table[i] for i in self.board.pieces(chess.KNIGHT, chess.WHITE)])
        knightsq += sum([-knights_table[chess.square_mirror(i)] for i in self.board.pieces(chess.KNIGHT, chess.BLACK)])
        bishopsq = sum([bishops_table[i] for i in self.board.pieces(chess.BISHOP, chess.WHITE)])
        bishopsq += sum([-bishops_table[chess.square_mirror(i)] for i in self.board.pieces(chess.BISHOP, chess.BLACK)])
        rooksq = sum([rooks_table[i] for i in self.board.pieces(chess.ROOK, chess.WHITE)])
        rooksq += sum([-rooks_table[chess.square_mirror(i)] for i in self.board.pieces(chess.ROOK, chess.BLACK)])
        queensq = sum([queens_table[i] for i in self.board.pieces(chess.QUEEN, chess.WHITE)])
        queensq += sum([-queens_table[chess.square_mirror(i)] for i in self.board.pieces(chess.QUEEN, chess.BLACK)])
        kingsq = sum([kings_table[i] for i in self.board.pieces(chess.KING, chess.WHITE)])
        kingsq += sum([-kings_table[chess.square_mirror(i)] for i in self.board.pieces(chess.KING, chess.BLACK)])
        knightsq = knightsq + sum([-knights_table[chess.square_mirror(i)] for i in self.board.pieces(chess.KNIGHT, chess.BLACK)])
        bishopsq = sum([bishops_table[i] for i in self.board.pieces(chess.BISHOP, chess.WHITE)])
        bishopsq = bishopsq + sum([-bishops_table[chess.square_mirror(i)] for i in self.board.pieces(chess.BISHOP, chess.BLACK)])
        rooksq = sum([rooks_table[i] for i in self.board.pieces(chess.ROOK, chess.WHITE)])
        rooksq = rooksq + sum([-rooks_table[chess.square_mirror(i)] for i in self.board.pieces(chess.ROOK, chess.BLACK)])
        queensq = sum([queens_table[i] for i in self.board.pieces(chess.QUEEN, chess.WHITE)])
        queensq = queensq + sum([-queens_table[chess.square_mirror(i)] for i in self.board.pieces(chess.QUEEN, chess.BLACK)])
        kingsq = sum([kings_table[i] for i in self.board.pieces(chess.KING, chess.WHITE)])
        kingsq = kingsq + sum([-kings_table[chess.square_mirror(i)] for i in self.board.pieces(chess.KING, chess.BLACK)])

        # evaluate position
        eval = material + pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq
        return eval if self.board.turn else -eval

    def alphabeta(self, alpha, beta, depthleft):
        bestscore = -9999
        if depthleft == 0:
            return self.quiesce(alpha, beta)

        for move in self.board.legal_moves:
            self.board.push(move)
            score = -self.alphabeta(-beta, -alpha, depthleft - 1)
            self.board.pop()

            if score >= beta:
                return score
            if score > bestscore:
                bestscore = score
            if score > alpha:
                alpha = score

            # alpha-beta pruning
            if alpha >= beta:
                break

        return bestscore

    def quiesce(self, alpha, beta):
        stand_pat = self.evaluate_board()
        if (stand_pat >= beta):
            return beta
        if (alpha < stand_pat):
            alpha = stand_pat

        # Order moves based on their potential to improve alpha
        moves = self.board.legal_moves
        moves = sorted(moves, key=lambda move: -self.evaluate_move(move))

        for move in moves:
            if self.board.is_capture(move):
                self.board.push(move)
                score = -self.quiesce(-beta, -alpha)
                self.board.pop()

                if (score >= beta):
                    return beta
                if (score > alpha):
                    alpha = score
        return alpha

    def evaluate_move(self, move):
        self.board.push(move)
        score = self.evaluate_board()
        self.board.pop()
        return score

    def try_moves(self, depth):
        if os.path.exists("D:/Program Files/JetBrains/PythonBooks/human.bin"):
            with chess.polyglot.MemoryMappedReader("D:/Program Files/JetBrains/PythonBooks/human.bin") as reader:
                move = reader.weighted_choice(self.board).move
                return move
        bestMove = chess.Move.null()
        bestValue = float("-inf")
        alpha = float("-inf")
        beta = float("inf")
        for move in self.board.legal_moves:
            self.board.push(move)
            boardValue = -self.alphabeta(-beta, -alpha, depth - 1)
            if boardValue > bestValue:
                bestValue = boardValue
                bestMove = move
            if (boardValue > alpha):
                alpha = boardValue
            self.board.pop()
        return bestMove

    def play(self):
        while not self.board.is_game_over():
            if self.board.turn == chess.WHITE:
                # display.start(self.board.fen())
                move = input("Please enter your move: ")
                try:
                    self.board.push_san(move)
                except ValueError:
                    print("Invalid mode, please enter a valid move.")
            else:
                move = self.try_moves(depth=5)
                print("Engine move: ", move)
                self.board.push(move)

            # print board after each move and result after the game ends
            print(self.board)
            # print(chess.svg.board(self.board, size=350))
            # display.update(self.board.fen())
        # chess.svg.board(self.board, size=350)
        print(self.board.result)
        # display.update(self.board.fen())


SimpleEngine().play()
