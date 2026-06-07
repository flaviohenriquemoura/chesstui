import chess
from textual.app import App
from textual.widgets import Static, Switch, Collapsible, Label
from textual.containers import Grid, Horizontal, Vertical
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
▐╻█╻█╻▌
▝▜███▛▘
 ▟███▙
 ▗███▖
▝▀▀▀▀▀▘
"""

PEAO = """
 ▄▇▄
 ▜█▛
▄███▄
▔▔▔▔▔"""



VAZIO = """"""


ROWS = [
    (TORRE, CAVALO, BISPO, RAINHA, REI, BISPO, CAVALO, TORRE, VAZIO),
    (PEAO,  PEAO,   PEAO,  PEAO, PEAO,   PEAO,  PEAO,   PEAO, VAZIO),
    (VAZIO, VAZIO,  VAZIO, VAZIO, VAZIO,  VAZIO, VAZIO,  VAZIO, RAINHA),
    (VAZIO, VAZIO,  VAZIO, VAZIO, VAZIO,  VAZIO, VAZIO,  VAZIO, TORRE),
    (VAZIO, VAZIO,  VAZIO, VAZIO, VAZIO,  VAZIO, VAZIO,  VAZIO, BISPO),
    (VAZIO, VAZIO,  VAZIO, VAZIO, VAZIO,  VAZIO, VAZIO,  VAZIO, CAVALO),
    (PEAO,  PEAO,   PEAO,  PEAO, PEAO,   PEAO,  PEAO,   PEAO, VAZIO),
    (TORRE, CAVALO, BISPO, RAINHA, REI, BISPO, CAVALO, TORRE, VAZIO)
]

roques = [
    'e1g1',
    'e1c1',
    'e8g8',
    'e8c8'
]

t_roque_position = [
    'f1',
    'd1',
    'f8',
    'd8'
]

t_roque_orig = [
    'h1',
    'a1',
    'h8',
    'a8'
]

promo_dict = {
    RAINHA: 'q',
    TORRE: 'r',
    BISPO: 'b',
    CAVALO: 'n'
}

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
    promo = []
    w_turn = True
    could_promo = False
    promo_move = None

    promo_old_casa = None
    quero_ler = None

    rei_preto = None
    rei_branco = None
    i_lance = 2
    ord_lance = ""
    old_move = None

    def compose(self):

        with Vertical():
            yield Static(Text("Black: 10:00", Style(color="#ffffff", bold=True), justify="center"), classes="timeb container")


            with Horizontal():

                with Grid(classes="container"):
                    for i, fileira in enumerate(ROWS):

                        for j, peca in enumerate(fileira):

                            cor_fonte = "black" if i == 0 or i == 1 else "#ffffff"
                            if peca == VAZIO:
                                cor_fonte = "white"
 
                        
                            if j == 8:
                                cor_fonte = "white"
                                cell = Text(VAZIO, style=Style(color=cor_fonte, bold=True), justify="center")
                            else:
                                cell = Text.from_markup(peca, style=Style(color=cor_fonte, bold=True), justify="center")

                            classe_cor = "casa-clara" if (i + j) % 2 == 0 else "casa-escura"

                            classe_cor = "" if j == 8 else classe_cor


                            casa = CTabuleiro(cell, classes=classe_cor)
                            casa.coluna = (i-8)*-1
                            casa.linha = j+1
                            casa.text = peca
                            casa.cor_fonte = cor_fonte
                            if casa.linha == 9:
                                self.promo.append(casa)

                            casa.position = conector.number_to_position(casa.linha, casa.coluna)
                            if peca == REI:
                                self.rei_branco = casa if cor_fonte == "#ffffff" else self.rei_branco
                                self.rei_preto = casa if cor_fonte == "black" else self.rei_preto

                            yield casa
                
                with Collapsible(title="Ordem dos lances:", classes="info"):
                    yield Label("", classes="label lances")

            yield Static(Text("White: 10:00", Style(color="black", bold=True, bgcolor="#ffffff"), justify="center"), classes="timew ")

            
            yield Horizontal(
                Static("Auto-flip:", classes="label"),
                Switch(animate=False), classes="container flip"
                )



    @on(CTabuleiro.Clique)
    def casa_clicada(self, event):
        casa = event.casa
        self.promo_old_casa = [self.old_casa, casa] if self.old_casa != None else self.promo_old_casa


        is_selected = False
        move = f"{self.old_casa.position}{casa.position}" if self.old_casa != None else f"{casa.position}"

        if casa in self.promo and casa.text != VAZIO:
            move = f"{self.promo_move}{promo_dict[casa.text]}"
            if self.could_promo:
                self.old_casa = self.promo_old_casa[0]
                self.old_casa.text = casa.text
                casa = self.promo_old_casa[1]

#        self.quero_ler = f"{move} {self.old_casa} {casa.cor_fonte}" # estava usando para ler dados na tela

        if self.old_casa == None:
            for i in self.promo:
                    i.update(Text(VAZIO, style=Style(color=i.cor_fonte, bold=True), justify="center"))

        if self.old_casa != None:
            self.old_casa.remove_class("selected")
            self.old_casa.update(Text(self.old_casa.text, style=Style(color=self.old_casa.cor_fonte, bold=True, blink=False), justify="center"))
            conditional = ((self.promo_old_casa[0].position[0] == self.promo_old_casa[1].position[0] and self.promo_old_casa[1].text == VAZIO) or (self.promo_old_casa[0].position[0] != self.promo_old_casa[1].position[0]))
            if (self.old_casa.text == PEAO and ((self.w_turn and move[-1] == "8")  or (not self.w_turn and move[-1] == "1"))) and conditional:
 
                for i in self.promo:
                    i.update(Text(i.text, style=Style(color=i.cor_fonte, bold=True), justify="center"))
                self.could_promo = True
            else:
                for i in self.promo:
                    i.update(Text(VAZIO, style=Style(color=i.cor_fonte, bold=True), justify="center"))
                self.could_promo = False

        # se a casa for reselecionada, tira a seleção
        if self.old_casa == casa:
            casa.remove_class("selected")
            self.old_casa = None
            is_selected = True
        elif self.old_casa != None and self.old_casa.cor_fonte != casa.cor_fonte and not 'j' in move and self.jogo_tab.lance_legal(f"{move}"):

            # atualiza a casa com a peça escolhida
            self.old_move[0].remove_class("lastcasa") if self.old_move != None else []
            self.old_move[1].remove_class("nowcasa") if self.old_move != None else []
            self.old_move = [self.old_casa, casa]
            casa.update(Text(self.old_casa.text, style=Style(color=self.old_casa.cor_fonte, bold=True), justify="center"))
 
 
            casa.text = self.old_casa.text

            # verifica se o rei está em xeque e adiciona/remove background
            if self.jogo_tab.rei_xeque():
                self.rei_preto.add_class("xeque") if self.w_turn else self.rei_branco.add_class("xeque")
            else:
                self.rei_branco.remove_class("xeque")
                self.rei_preto.remove_class("xeque")


            # atualiza a casa do rei, caso movido
            if casa.text == REI:
                if not self.w_turn:
                  self.rei_preto = casa
                else:
                    self.rei_branco = casa

                if move in roques: # roque aqui
                    torre_position = conector.position_to_number(t_roque_position[roques.index(move)]) 
                    old_torre_position = conector.position_to_number(t_roque_orig[roques.index(move)])

                    torre = self.buscar_casa(torre_position[0], torre_position[1])
                    old_torre = self.buscar_casa(old_torre_position[0], old_torre_position[1])

                    old_torre.update(Text(VAZIO, style=Style(color=casa.cor_fonte, bold=True), justify="center"))
                    torre.update(Text(old_torre.text, style=Style(color=self.old_casa.cor_fonte, bold=True), justify="center"))


                    torre.text = old_torre.text
                    torre.cor_fonte = old_torre.cor_fonte

                    old_torre.text = VAZIO
                    old_torre.cor_fonte = "white"

            casa.cor_fonte = self.old_casa.cor_fonte
            self.old_casa.update(Text(VAZIO, style=Style(color=casa.cor_fonte, bold=True), justify="center"))


            self.old_casa.text = VAZIO
            self.old_casa.cor_fonte = "white"
            self.promo_old_casa[0].add_class("lastcasa")
            self.promo_old_casa[1].add_class("nowcasa")



            if self.w_turn:
                self.ord_lance += f"{self.i_lance//2}.{self.jogo_tab.lance} "
            else:
                self.ord_lance += f"{self.jogo_tab.lance} "
            self.i_lance += 1
            self.query_one(".lances").update(self.ord_lance)

            self.turn = "black" if self.turn == "#ffffff" else "#ffffff"
            self.w_turn = False if self.w_turn else True
        else:
            self.old_casa = None

        if casa.text != VAZIO and self.old_casa == None and casa.cor_fonte == self.turn and not is_selected:
            casa.add_class("selected")
            casa.update(Text(casa.text, style=Style(color=casa.cor_fonte, bold=True, blink=True), justify="center"))
            self.old_casa = casa

        self.promo_move = move

    def buscar_casa(self, linha, coluna):
        for casa in self.query(CTabuleiro):
            if casa.linha == linha and casa.coluna == coluna:
                return casa
        return None

    def relogio(self):
        if self.w_turn:
            minutos = self.tempow//60
            segundos = "00" if self.tempow%60 == 0 else self.tempow%60
            segundos = f"0{self.tempow%60}" if self.tempow%60 < 10 else self.tempow%60
            self.query_one('.timew').update(Text(f"White: {minutos}:{segundos} {self.quero_ler}", Style(color="black", bold=True, bgcolor="#ffffff"), justify="center"))
            self.tempow -=1
        else:
            minutos = self.tempob//60
            segundos = "00" if self.tempob%60 == 0 else self.tempob%60
            segundos = f"0{self.tempob%60}" if self.tempob%60 < 10 else self.tempob%60
            self.query_one('.timeb').update(Text(f"Black: {minutos}:{segundos} {self.quero_ler}", Style(color="#ffffff", bold=True), justify="center"))
            self.tempob -=1


    def inverte_tabuleiro(self):
        pass

    def on_mount(self):
        self.set_interval(1, self.relogio)


app = Tabuleiro()
app.run()
