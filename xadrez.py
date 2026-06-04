import chess
from textual.app import App
from textual.widgets import Static
from textual.containers import Grid
from rich.style import Style
from rich.text import Text

ROWS = [
    ('♖','♘','♗','♔','♕','♗','♘','♖'),
    ('♙','♙','♙','♙','♙','♙','♙','♙'),
    ('','','','','','','',''),
    ('','','','','','','',''),
    ('','','','','','','',''),
    ('','','','','','','',''),
    ('♙','♙','♙','♙','♙','♙','♙','♙'),
    ('♖','♘','♗','♔','♕','♗','♘','♖')  
]

#board = chess.Board(ROWS[1:])

class CTabuleiro(Static):
    pass

class Tabuleiro(App):
    CSS_PATH = "style.tcss"
    def compose(self):

        with Grid():
            for i, fileira in enumerate(ROWS):
                fileira_style = []
                for j, peca in enumerate(fileira):
                    peca = f" {peca} " if peca else "   "
                    if (i+j)%2==0:
                        cell = Text(peca, style=Style(bgcolor="#f0d9b5", color="black"), justify="center")

                    else:                    
                        cell = Text(peca, style=Style(bgcolor="#b58863", color="white"), justify="center")
                    fileira_style.append(cell)
                    yield CTabuleiro(cell)
app = Tabuleiro()
app.run()