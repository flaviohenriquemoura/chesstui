import chess

class JogoReal():
    board = chess.Board()      

    def lance_legal(self, move):
        lance = chess.Move.from_uci(move)
        if lance in self.board.legal_moves:
            self.board.push(lance)
            return True
        return False
    def rei_xeque(self):
        return self.board.is_check()

def number_to_position(linha, coluna):
        fileiras = "abcdefghj"
        return f"{fileiras[linha+-1]}{coluna}"

def position_to_number(position):
    return [(ord(position[0])-96), int(position[1])]