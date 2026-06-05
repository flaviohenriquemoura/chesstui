import chess
from textual.app import App
from textual.widgets import Static
from textual.containers import Grid, Horizontal
from textual import on, events
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
    class Clique(events.Event):
        pass

    def on_click(self, event: events.Click):
        event.stop()
        message = self.Clique()
        message.casa = self
        self.post_message(message)

class Tabuleiro(App):
    CSS_PATH = "style.tcss"
    old_casa = None
    turn = "#ffffff"
    tempow = 600
    tempob = 600
    w_turn = True

    def compose(self):

        yield Static(Text("Black: 10:00", Style(color="#ffffff", bold=True), justify="center"), classes="timeb")


        with Horizontal():

            with Grid():
                for i, fileira in enumerate(ROWS):

                    for j, peca in enumerate(fileira):

                        cor_fonte = "black" if i == 0 or i == 1 else "#ffffff"
                        cell = Text(peca, style=Style(color=cor_fonte, bold=True), justify="center")
                    
                        classe_cor = "casa-clara" if (i + j) % 2 == 0 else "casa-escura"

                        casa = CTabuleiro(cell, classes=classe_cor)
                        casa.linha = (i-8)*-1
                        casa.coluna = j+1
                        casa.text = peca
                        casa.cor_fonte = cor_fonte

                        yield casa
        yield Static(Text("White: 10:00", Style(color="black", bold=True, bgcolor="#ffffff"), justify="center"), classes="timew")

    @on(CTabuleiro.Clique)
    def casa_clicada(self, event):
        casa = event.casa

        for c in self.query(CTabuleiro):
            if "selected" in str(c.classes):
                self.old_casa = c
            c.remove_class("selected")

        if self.old_casa != None:
            casa.update(Text(self.old_casa.text, style=Style(color=self.old_casa.cor_fonte, bold=True), justify="center"))
            casa.text = self.old_casa.text
            casa.cor_fonte = self.old_casa.cor_fonte
            self.old_casa.update(Text(VAZIO, style=Style(color=casa.cor_fonte, bold=True), justify="center"))
            self.old_casa.text = VAZIO
            self.turn = "black" if self.turn == "#ffffff" else "#ffffff"
            self.w_turn = False if self.w_turn else True


        if casa.text != VAZIO and self.old_casa == None and casa.cor_fonte == self.turn:
            casa.add_class("selected")
            self.old_casa = casa

        self.old_casa = None

        outra_casa = self.buscar_casa(linha=4, coluna=4)

    def buscar_casa(self, linha, coluna):
        for casa in self.query(CTabuleiro):
            if casa.linha == linha and casa.coluna == coluna:
                return casa
        return None
    
    def relogio(self):
        if self.w_turn:
            minutos = f"{self.tempow/60:.0f}"
            segundos = self.tempow%60
            self.query_one('.timew').update(Text(f"White: {minutos}:{segundos}", Style(color="black", bold=True, bgcolor="#ffffff"), justify="center"))
            self.tempow -=1
        else:
            minutos = f"{self.tempob/60:.0f}"
            segundos = self.tempob%60
            self.query_one('.timeb').update(Text(f"Black: {minutos}:{segundos}", Style(color="#ffffff", bold=True), justify="center"))
            self.tempob -=1

    def on_mount(self):
        self.set_interval(1, self.relogio)

app = Tabuleiro()
app.run()
