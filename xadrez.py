import chess
from textual.app import App
from textual.widgets import Static
from textual.containers import Grid, Horizontal
from textual import on, events
from rich.style import Style
from rich.text import Text
import conector

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
    (TORRE, CAVALO, BISPO, RAINHA, REI, BISPO, CAVALO, TORRE),
    (PEAO,  PEAO,   PEAO,  PEAO, PEAO,   PEAO,  PEAO,   PEAO),
    (VAZIO, VAZIO,  VAZIO, VAZIO, VAZIO,  VAZIO, VAZIO,  VAZIO),
    (VAZIO, VAZIO,  VAZIO, VAZIO, VAZIO,  VAZIO, VAZIO,  VAZIO),
    (VAZIO, VAZIO,  VAZIO, VAZIO, VAZIO,  VAZIO, VAZIO,  VAZIO),
    (VAZIO, VAZIO,  VAZIO, VAZIO, VAZIO,  VAZIO, VAZIO,  VAZIO),
    (PEAO,  PEAO,   PEAO,  PEAO, PEAO,   PEAO,  PEAO,   PEAO),
    (TORRE, CAVALO, BISPO, RAINHA, REI, BISPO, CAVALO, TORRE)
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
    jogo_tab = conector.JogoReal()
    old_casa = None
    turn = "#ffffff"
    tempow = 600
    tempob = 600

    w_turn = True


    rei_preto = None
    rei_branco = None

    def compose(self):


        yield Static(Text("Black: 10:00", Style(color="#ffffff", bold=True), justify="center"), classes="timeb")


        with Horizontal():

            with Grid():
                for i, fileira in enumerate(ROWS):

                    for j, peca in enumerate(fileira):

                        cor_fonte = "black" if i == 0 or i == 1 else "#ffffff"
                        if peca == VAZIO:
                            cor_fonte = "white"
                        cell = Text(peca, style=Style(color=cor_fonte, bold=True), justify="center")

                        classe_cor = "casa-clara" if (i + j) % 2 == 0 else "casa-escura"

                        casa = CTabuleiro(cell, classes=classe_cor)
                        casa.coluna = (i-8)*-1
                        casa.linha = j+1
                        casa.text = peca
                        casa.cor_fonte = cor_fonte
                        casa.position = conector.number_to_position(casa.linha, casa.coluna)
                        if peca == REI:
                            self.rei_branco = casa if cor_fonte == "#ffffff" else self.rei_branco
                            self.rei_preto = casa if cor_fonte == "black" else self.rei_preto

                        yield casa
        yield Static(Text("White: 10:00", Style(color="black", bold=True, bgcolor="#ffffff"), justify="center"), classes="timew")

    @on(CTabuleiro.Clique)
    def casa_clicada(self, event):
        casa = event.casa


        for c in self.query(CTabuleiro):
            if "selected" in str(c.classes):
                self.old_casa = c
            c.remove_class("selected")

        if self.old_casa == casa:
            casa.remove_class("selected")
        elif self.old_casa != None and self.old_casa.cor_fonte != casa.cor_fonte and self.jogo_tab.lance_legal(f"{self.old_casa.position}{casa.position}"):


            casa.update(Text(self.old_casa.text, style=Style(color=self.old_casa.cor_fonte, bold=True), justify="center"))
            casa.text = self.old_casa.text
            casa.cor_fonte = self.old_casa.cor_fonte
            self.old_casa.update(Text(VAZIO, style=Style(color=casa.cor_fonte, bold=True), justify="center"))
            self.old_casa.text = VAZIO
            self.old_casa.cor_fonte = "white"

            self.turn = "black" if self.turn == "#ffffff" else "#ffffff"
            self.w_turn = False if self.w_turn else True
        else:
            self.old_casa = None

        if self.old_casa != None:
            self.query_one('.timew').update(self.old_casa.position+casa.position)

        if casa.text != VAZIO and self.old_casa == None and casa.cor_fonte == self.turn:
            casa.add_class("selected")
            self.old_casa = casa

        self.old_casa = None

 
        if self.jogo_tab.rei_xeque():
            self.rei_preto.add_class("xeque") if not self.w_turn else self.rei_branco.add_class("xeque")
        else:
            self.rei_branco.remove_class("xeque")
            self.rei_preto.remove_class("xeque")
        if casa.text == REI:
            self.rei_preto = casa if self.w_turn else self.rei_preto
            self.rei_branco = casa if not self.w_turn else self.rei_branco

    def relogio(self):
        if self.w_turn:
            minutos = self.tempow//60
            segundos = "00" if self.tempow%60 == 0 else self.tempow%60
            segundos = f"0{self.tempow%60}" if self.tempow%60 < 10 else self.tempow%60
            self.query_one('.timew').update(Text(f"White: {minutos}:{segundos} {self.rei_branco.position}", Style(color="black", bold=True, bgcolor="#ffffff"), justify="center"))
            self.tempow -=1
        else:
            minutos = self.tempob//60
            segundos = "00" if self.tempob%60 == 0 else self.tempob%60
            segundos = f"0{self.tempob%60}" if self.tempob%60 < 10 else self.tempob%60
            self.query_one('.timeb').update(Text(f"Black: {minutos}:{segundos}", Style(color="#ffffff", bold=True), justify="center"))
            self.tempob -=1


    def inverte_tabuleiro(self):
        pass

    def on_mount(self):
        self.set_interval(1, self.relogio)

app = Tabuleiro()
app.run()
