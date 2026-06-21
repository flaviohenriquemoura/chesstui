import chess

class JogoReal():
    board = chess.Board()      
    lance = None
    def lance_legal(self, move):
        lance = chess.Move.from_uci(move)
  
        if lance in self.board.legal_moves:
            self.lance = self.board.san(lance)
            self.board.push(lance)
            return True
        return False
        
    def rei_xeque(self):
        return self.board.is_check()


class JogoReal():
    board = chess.Board()      
    lance = None
    def fazer_lance(self, move):
        lance = chess.Move.from_uci(move)

        self.lance = self.board.san(lance)
        self.board.push(lance)

    

    def lance_legal(self, move):
        if move == None or move[:2] == move[2:4] or len(move) not in [4, 5]:
            return False
        lance = chess.Move.from_uci(move)
        if lance in self.board.legal_moves:

            return True
        return False

    def rei_xeque(self):
        return self.board.is_check()

def number_to_position(linha, coluna):
        fileiras = "abcdefgh"
        return f"{fileiras[linha+-1]}{coluna}"

def position_to_number(position):
    return [(ord(position[0])-96), int(position[1])]


def number_to_position(linha, coluna):
        fileiras = "abcdefgh"
        return f"{fileiras[linha+-1]}{coluna}"

def position_to_number(position):
    return [(ord(position[0])-96), int(position[1])]

def draws(board):
    return (
        board.is_variant_draw() or
        board.is_insufficient_material() or
        board.is_stalemate() or
        board.is_seventyfive_moves() or 
        board.is_fivefold_repetition() or 
        board.is_fifty_moves() or
        board.is_repetition()
    ) 

        