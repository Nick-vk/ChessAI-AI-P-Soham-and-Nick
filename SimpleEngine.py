import chess
import chess.polyglot
import chess.svg
import chess.pgn
from chessboard import display
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
            if self.board.turn:
                return -9999
            else:
                return 9999
        if self.board.is_stalemate():
            return 0
        if self.board.is_insufficient_material():
            return 0

    # calculate_pieces
        wp = len(self.board.pieces(chess.PAWN, chess.WHITE))
        bp = len(self.board.pieces(chess.PAWN, chess.BLACK))
        wn = len(self.board.pieces(chess.KNIGHT, chess.WHITE))
        bn = len(self.board.pieces(chess.KNIGHT, chess.BLACK))
        wb = len(self.board.pieces(chess.BISHOP, chess.WHITE))
        bb = len(self.board.pieces(chess.BISHOP, chess.BLACK))
        wr = len(self.board.pieces(chess.ROOK, chess.WHITE))
        br = len(self.board.pieces(chess.ROOK, chess.BLACK))
        wq = len(self.board.pieces(chess.QUEEN, chess.WHITE))
        bq = len(self.board.pieces(chess.QUEEN, chess.BLACK))

    # calculate_scores
        material = 100 * (wp - bp) + 320 * (wn - bn) + 330 * (wb - bb) + 500 * (wr - br) + 900 * (wq - bq)

        pawnsq = sum([pawns_table[i] for i in self.board.pieces(chess.PAWN, chess.WHITE)])
        pawnsq = pawnsq + sum([-pawns_table[chess.square_mirror(i)]
                               for i in self.board.pieces(chess.PAWN, chess.BLACK)])
        knightsq = sum([knights_table[i] for i in self.board.pieces(chess.KNIGHT, chess.WHITE)])
        knightsq = knightsq + sum([-knights_table[chess.square_mirror(i)]
                                   for i in self.board.pieces(chess.KNIGHT, chess.BLACK)])
        bishopsq = sum([bishops_table[i] for i in self.board.pieces(chess.BISHOP, chess.WHITE)])
        bishopsq = bishopsq + sum([-bishops_table[chess.square_mirror(i)]
                                   for i in self.board.pieces(chess.BISHOP, chess.BLACK)])
        rooksq = sum([rooks_table[i] for i in self.board.pieces(chess.ROOK, chess.WHITE)])
        rooksq = rooksq + sum([-rooks_table[chess.square_mirror(i)]
                               for i in self.board.pieces(chess.ROOK, chess.BLACK)])
        queensq = sum([queens_table[i] for i in self.board.pieces(chess.QUEEN, chess.WHITE)])
        queensq = queensq + sum([-queens_table[chess.square_mirror(i)]
                                 for i in self.board.pieces(chess.QUEEN, chess.BLACK)])
        kingsq = sum([kings_table[i] for i in self.board.pieces(chess.KING, chess.WHITE)])
        kingsq = kingsq + sum([-kings_table[chess.square_mirror(i)]
                               for i in self.board.pieces(chess.KING, chess.BLACK)])

    # evaluate position
        eval = material + pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq
        if self.board.turn:
            return eval
        else:
            return -eval

    def alphabeta(self, alpha, beta, depthleft):
        bestscore = -9999
        if (depthleft == 0):
            return self.quiesce(alpha, beta)
        for move in self.board.legal_moves:
            self.board.push(move)
            score = -self.alphabeta(-beta, -alpha, depthleft - 1)
            self.board.pop()
            if (score >= beta):
                return score
            if (score > bestscore):
                bestscore = score
            if (score > alpha):
                alpha = score
        return bestscore

    def quiesce(self, alpha, beta):
        stand_pat = self.evaluate_board()
        if (stand_pat >= beta):
            return beta
        if (alpha < stand_pat):
            alpha = stand_pat
        for move in self.board.legal_moves:
            if self.board.is_capture(move):
                self.board.push(move)
                score = -self.quiesce(-beta, -alpha)
                self.board.pop()

                if (score >= beta):
                    return beta
                if (score > alpha):
                    alpha = score
        return alpha

    def try_moves(self, depth):
        # openings we have to download this
        try:
            # change to your file location
            move = chess.polyglot.MemoryMappedReader("D:/Program Files/JetBrains/PythonBooks/human.bin").weighted_choice(self.board).move
            return move
        except:
            bestMove = chess.Move.null()
            bestValue = -99999
            alpha = -100000
            beta = 100000
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
                display.start(self.board.fen())
                move = input("Please enter your move: ")
                try:
                    self.board.push_san(move)
                except ValueError:
                    print("Invalid mode, please enter a valid move.")
            else:
                move = self.try_moves(depth=1)
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
