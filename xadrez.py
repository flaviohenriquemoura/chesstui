import chess
from textual.app import App
from textual.widgets import Static
from textual.containers import Grid, Horizontal, Vertical
from rich.style import Style
from rich.text import Text

TORRE = """
▐█▄█▄█▌
▝▜███▛▘
  ███
 ▟███▙ 
▝▀▀▀▀▀▘
"""

CAVALO = """
  ▄▟▟▖
 ▟▛███▖
▝▀▜███▊
 ▗███▛ 
 ▀▀▀▀▀ 
 """
 
BISPO = """
▗▅  ▖
██▍ █
███▍█
▝███▘
▀▀▀▀▀
"""

REI = """
  ▂▃╋▃▂  
 ▐█████▋ 
  ▜███▛  
   ▟█▙   
  ▀▀▀▀▀  
"""

RAINHA = """

▐▙▟█▙▟▌
 ▜███▛ 
 ▗███▖ 
▝▀▀▀▀▀▘
"""

PEAO = """
 ▄▇▄
 ▜█▛
▄███▄
▔▔▔▔▔
 """

VAZIO = """
     
     
     """


ROWS = [
    (TORRE, CAVALO, BISPO, REI, RAINHA, BISPO, CAVALO, TORRE),
    (PEAO,  PEAO,   PEAO,  PEAO, PEAO,   PEAO,  PEAO,   PEAO),
    (VAZIO, VAZIO,  VAZIO, VAZIO, VAZIO,  VAZIO, VAZIO,  VAZIO),
    (VAZIO, VAZIO,  VAZIO, VAZIO, VAZIO,  VAZIO, VAZIO,  VAZIO),
    (VAZIO, VAZIO,  VAZIO, VAZIO, VAZIO,  VAZIO, VAZIO,  VAZIO),
    (VAZIO, VAZIO,  VAZIO, VAZIO, VAZIO,  VAZIO, VAZIO,  VAZIO),
    (PEAO,  PEAO,   PEAO,  PEAO, PEAO,   PEAO,  PEAO,   PEAO),
    (TORRE, CAVALO, BISPO, REI, RAINHA, BISPO, CAVALO, TORRE)  
]


class CTabuleiro(Static):
    pass

class Tabuleiro(App):
    CSS_PATH = "style.tcss"
    def compose(self):



        with Horizontal():
            with Vertical():
                yield Static(Text("Black: 00:00", Style(color="#ffffff", bold=True), justify="center"), classes="timeb")
                yield Static(Text("White: 00:00", Style(color="black", bold=True, bgcolor="#ffffff"), justify="center"), classes="timew")

#        with Horizontal():

            with Grid():
                for i, fileira in enumerate(ROWS):

                    for j, peca in enumerate(fileira):

                        cor_fonte = "black" if i == 0 or i == 1 else "#ffffff"
                        cell = Text(peca, style=Style(color=cor_fonte, bold=True), justify="center")
                    
                        classe_cor = "casa-clara" if (i + j) % 2 == 0 else "casa-escura"

                        yield CTabuleiro(cell, classes=classe_cor)

            pass
app = Tabuleiro()
app.run()
