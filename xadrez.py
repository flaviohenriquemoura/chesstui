import chess
from textual.app import App
from textual.widgets import Static, Switch, Collapsible, Label
from textual.containers import Grid, Horizontal, Vertical, VerticalScroll
from textual import on, events
from rich.style import Style
from rich.text import Text
import conector
from piece import *

# classe para cada casa do tabuleiro 
class CTabuleiro(Static):
    class Clique(events.Event):
        pass

    #função para capturar o clique na casa
    def on_click(self, event: events.Click):
        event.stop()
        message = self.Clique()
        message.casa = self
        self.post_message(message)

class Cpromo(Static):
    class Clique(events.Event):
        pass

# função para capturar clique nas peças laterais de promoção

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
    tempoW = 600
    tempoB = 600
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

    inverter = False


    def compose(self):
# with vertical determina que haverá uma disposição vertical dos elementos na tela 
        with Vertical():
            # relógio branco
            yield Static(Text("Black: 10:00", Style(color="#ffffff", bold=True), justify="center"), classes="timeb container")

# with vertical determina que haverá uma disposição horizontal dos elementos na tela 

            with Horizontal():

                with Grid(classes="container tab"):
                    # for para percorrer cada fileira da disposição inical de peças
                    for i, fileira in enumerate(ROWS):
                        #for para percorrer cada peça da fileira do for anterior
                        for j, peca in enumerate(fileira):

                            #determina pela fórmula que se a fileira for uma das primeiras pelo lado de cima, terá peças pretas
                            cor_fonte = "black" if i <=1 else "#ffffff"

                            # é a cor padrão de casas vazias; "white" != "#ffffff"
                            if peca == VAZIO:
                                cor_fonte = "white"


                            # texto estilizado da peça
                            cell = Text(peca, style=Style(color=cor_fonte, bold=True), justify="center")

                            # formula para determinar a cor da casa
                            classe_cor = "casa-clara" if (i + j) % 2 == 0 else "casa-escura"

                            # cada casa é um objeto da classe Ctabuleiro e recebe seus atributos
                            casa = CTabuleiro(cell, classes=classe_cor)
                            casa.coluna = (i-8)*-1
                            casa.linha = j+1
                            casa.text = peca
                            casa.cor_fonte = cor_fonte

                            # posição da peça em notação de xadrez
                            casa.position = conector.number_to_position(casa.linha, casa.coluna)
                            # se a peça percorrida for igual ao rei, guarda a referenciação da casa
                            if peca == REI:
                                self.rei_branco = casa if cor_fonte == "#ffffff" else self.rei_branco
                                self.rei_preto = casa if cor_fonte == "black" else self.rei_preto

                            # coloca a casa no tabuleiro
                            yield casa

                # peças que serão usadas lateralmente ao tabuleiro para promoção
                with Horizontal():
                    with Grid(classes="pecas_promo"):
                        for pecas in [DAMA, TORRE, BISPO, CAVALO]:
                            peca = Cpromo(Text(VAZIO, style=Style(color="white", bold=True)), classes="peca")
                            peca.cor_fonte = "white"
                            peca.text = pecas
                            self.promo.append(peca)
                            yield peca


                # Ordem dos lances
                with Vertical():
                    with VerticalScroll(classes="rolavel"):
                        with Collapsible(title="Ordem dos lances:", classes="info"):
                            yield Label("1. ", classes="label lances")

#                    yield(Static(Text(GAME_OVER, style=Style(color="red", bold=True))))
#                    yield(Static(Text(WINS, style=Style(color="green", bold=True))))

            # relógio preto
            yield Static(Text("White: 10:00", Style(color="black", bold=True, bgcolor="#ffffff"), justify="center"), classes="timew ")


            #botão de auto-flip
            with Horizontal(classes="container flip"):

                yield Static("Auto-flip:", classes="label")
                self.switch = Switch(animate=False)
                yield self.switch


    # quando a casa lateral de promoção for clicada, acionará casa_clicada() com a respectiva peça desejada
    @on(Cpromo.Clique)
    def promo_clique(self, event):
        # variavel para
        self.could_promo = True
        self.casa_clicada(event)
        pass

    #função que captura os cliques no tabuleiro propriamente dito e os trata
    @on(CTabuleiro.Clique)
    def casa_clicada(self, event):
        casa = event.casa

        # variável importante para guardar o antepenúltimo movimento, em casos de promoção
        self.promo_old_casa = [self.old_casa, casa] if self.old_casa != None else self.promo_old_casa


        is_selected = False

        # caso a casa clicada não seja uma das laterais de promoção, ele recebe o movimento 
        if not casa in self.promo:
            move = f"{self.old_casa.position}{casa.position}" if self.old_casa != None else f"{casa.position}"

        # caso seja, recebe valor diferente com a casa desejada no final
        else:
            move = f"{self.promo_move}{promo_dict[casa.text]}"
            if self.could_promo:
                self.old_casa = self.promo_old_casa[0]
                self.old_casa.text = casa.text
                casa = self.promo_old_casa[1]

#        self.quero_ler = f"{casa.position}" # estava usando para ler dados na tela

        # se a casa antiga selecionada tiver valor nulo, a barra lateral de promoção some
        if self.old_casa == None:
            for i in self.promo:
                    i.update(Text(VAZIO, style=Style(color=i.cor_fonte, bold=True), justify="center"))

        # se ela tiver um valor, remove a seleção visual da casa anterior
        else :
            self.old_casa.remove_class("selected")
            self.old_casa.update(Text(self.old_casa.text, style=Style(color=self.old_casa.cor_fonte, bold=True, blink=False), justify="center"))

            # se for um movimento de peão e válido como para promoção, libera a barra lateral de promoção
            if self.old_casa.text == PEAO and self.jogo_tab.lance_legal(f"{move}q"):
                for i in self.promo:
                    i.update(Text(i.text, style=Style(color=i.cor_fonte, bold=True), justify="center"))
                self.could_promo = True
            #caso contrário, esconde a barra lateral
            else:
                for i in self.promo:
                    i.update(Text(VAZIO, style=Style(color=i.cor_fonte, bold=True), justify="center"))
                self.could_promo = False


        # se a casa for reselecionada, tira a seleção visual da peça

        if self.old_casa == casa:
            casa.remove_class("selected")
            self.old_casa = None
            is_selected = True
        # se for um movimento válido, trata todos os aspectos de atualização do tabuleiro
        elif self.jogo_tab.lance_legal(f"{move}"):

            # faz o lance no tabuleiro da biblioteca chess
            self.jogo_tab.fazer_lance(move)
            # remove os backgrounds das peças envolvidas com cores de última/atual casa
            self.old_move[0].remove_class("lastcasa") if self.old_move != None else []
            self.old_move[1].remove_class("nowcasa") if self.old_move != None else []

            # variável que recebe os valores da última casa movimentada e casa atual
            self.old_move = [self.old_casa, casa]
            # atualiza a casa selecionada para movimentar com a casa anteriormente selecionada
            casa.update(Text(self.old_casa.text, style=Style(color=self.old_casa.cor_fonte, bold=True), justify="center"))


            # a casa atual agora recebe atributos da casa anterior
            casa.text = self.old_casa.text
            casa.cor_fonte = self.old_casa.cor_fonte

            # os valores da casa antiga são atualizadas para o padrão de casa vazia
            self.old_casa.update(Text(VAZIO, style=Style(color=casa.cor_fonte, bold=True), justify="center"))


            self.old_casa.text = VAZIO
            self.old_casa.cor_fonte = "white"

            # atualiza os backgrounds das peças envolvidas com cores de última/atual casa
            self.old_move[0].add_class("lastcasa")
            self.old_move[1].add_class("nowcasa")


            # inverte o tabuleiro e atualiza a referenciação da casa atual
            if self.switch.value:
                casa = self.inverte_tabuleiro(casa)


            # verifica se o rei está em xeque e adiciona/remove background
            if self.jogo_tab.rei_xeque():
                self.rei_preto.add_class("xeque") if self.w_turn else self.rei_branco.add_class("xeque")
            else:
                self.rei_branco.remove_class("xeque")
                self.rei_preto.remove_class("xeque")


            if casa.text == REI:
            # atualiza a casa do rei, caso movido
                if not self.w_turn:
                  self.rei_preto = casa
                else:
                    self.rei_branco = casa

                if move in roques: # caso um dos movimentos seja de roque, captura a posição da torre e atualiza tanto o rei quanto a torre
                    torre_position = conector.position_to_number(t_roque_position[roques.index(move)])
                    old_torre_position = conector.position_to_number(t_roque_orig[roques.index(move)])

                    torre = self.buscar_casa(torre_position[0], torre_position[1])
                    old_torre = self.buscar_casa(old_torre_position[0], old_torre_position[1])

                    old_torre.update(Text(VAZIO, style=Style(color="white", bold=True), justify="center"))
                    torre.update(Text(old_torre.text, style=Style(color=casa.cor_fonte, bold=True), justify="center"))


                    torre.text = old_torre.text
                    torre.cor_fonte = old_torre.cor_fonte

                    old_torre.text = VAZIO
                    old_torre.cor_fonte = "white"

            # atualiza o texto de ordem de lances
            if self.w_turn:
                self.ord_lance += f"{self.i_lance//2}.{VAZIO:<1}{self.jogo_tab.lance:<8} "
            else:
                self.ord_lance += f"{self.jogo_tab.lance}\n"

            # o contador de lances é somado +1
            self.i_lance += 1
            # atualiza a seção de ordem de lances
            self.query_one(".lances").update(self.ord_lance)

            # inverte o turno e a cor das peças que podem ser selecionadas
            self.turn = "black" if self.turn == "#ffffff" else "#ffffff"
            self.w_turn = False if self.w_turn else True

            return True


        else:
            self.old_casa = None

        # se a casa não for vazia, a casa antiga selecionada não 'existir', 
        # a cor da peça for coerente com das peças que podem ser selecionadas e não haver peça selecionada atualmente,
        # a casa é atualizada visualmente como selecionada
        if casa.text != VAZIO and self.old_casa == None and casa.cor_fonte == self.turn and not is_selected:
            casa.add_class("selected")
            casa.update(Text(casa.text, style=Style(color=casa.cor_fonte, bold=True, blink=True), justify="center"))
            self.old_casa = casa

        # guarda o movimento anterior para casos de promoção
        self.promo_move = move



    # função para buscar uma casa específica no tabuleiro por linha/coluna
    def buscar_casa(self, linha, coluna):
        for casa in self.query(CTabuleiro):
            if casa.linha == linha and casa.coluna == coluna:
                return casa
        return None

    # função dos relógios
    def relogio(self):
        if self.w_turn:
            minutos = self.tempoW//60
            segundos = "00" if self.tempoW%60 == 0 else self.tempoW%60
            segundos = f"0{self.tempoW%60}" if self.tempoW%60 < 10 else self.tempoW%60
            self.query_one('.timew').update(Text(f"White: {minutos}:{segundos} {self.quero_ler}", Style(color="black", bold=True, bgcolor="#ffffff"), justify="center"))
            self.tempoW -=1
        else:
            minutos = self.tempoB//60
            segundos = "00" if self.tempoB%60 == 0 else self.tempoB%60
            segundos = f"0{self.tempoB%60}" if self.tempoB%60 < 10 else self.tempoB%60
            self.query_one('.timeb').update(Text(f"Black: {minutos}:{segundos} {self.quero_ler}", Style(color="#ffffff", bold=True), justify="center"))
            self.tempoB -=1

    # função para inverter o tabuleiro
    def inverte_tabuleiro(self, casa):
        copy_board = list(self.query(CTabuleiro))
        n = len(copy_board)

        # se tiver algum rei em xeque, já remove o efeito visual
        self.rei_branco.remove_class("xeque")
        self.rei_preto.remove_class("xeque")
        # percorre metade do tabuleiro, sendo que haverá duas variáveis, uma que:
        # percorre as primeiras 32 casas e a outra percorre as últimas 32
        # dessa forma o tabuleiro consegue ser espelhado, atualizando o primeiro pelo último e assim sucessivamente
        for i in range(n//2):
            cpy_casa_antiga = copy_board[i]
            cpy_casa_nova = copy_board[n-i-1]



            # substitui todas as propriedades das casas, uma pelas outras
            cpy_casa_antiga.text, cpy_casa_nova.text = cpy_casa_nova.text, cpy_casa_antiga.text
            cpy_casa_antiga.cor_fonte, cpy_casa_nova.cor_fonte = cpy_casa_nova.cor_fonte, cpy_casa_antiga.cor_fonte

            cpy_casa_antiga.position, cpy_casa_nova.position = cpy_casa_nova.position, cpy_casa_antiga.position
            cpy_casa_antiga.linha, cpy_casa_nova.linha = cpy_casa_nova.linha, cpy_casa_antiga.linha
            cpy_casa_antiga.coluna, cpy_casa_nova.coluna = cpy_casa_nova.coluna, cpy_casa_antiga.coluna

            # atualiza o texto visual
            cpy_casa_antiga.update(Text(cpy_casa_antiga.text, style=Style(color=cpy_casa_antiga.cor_fonte, bold=True), justify="center"))
            cpy_casa_nova.update(Text(cpy_casa_nova.text, style=Style(color=cpy_casa_nova.cor_fonte, bold=True), justify="center"))

            # remove outras quaisquerr casas
            cpy_casa_antiga.remove_class("lastcasa")
            cpy_casa_antiga.remove_class("nowcasa")
            cpy_casa_nova.remove_class("lastcasa")
            cpy_casa_nova.remove_class("nowcasa")

            # se a casa antiga tiver algum background de movimento, parra pra casa nova
            if cpy_casa_antiga == self.old_move[0]:
                cpy_casa_antiga.remove_class("lastcasa")
                cpy_casa_nova.add_class("lastcasa")

            elif cpy_casa_nova == self.old_move[0]:
                cpy_casa_nova.remove_class("lastcasa")
                cpy_casa_antiga.add_class("lastcasa")

            if cpy_casa_antiga == self.old_move[1]:
                cpy_casa_antiga.remove_class("nowcasa")
                cpy_casa_nova.add_class("nowcasa")
            elif cpy_casa_nova == self.old_move[1]:
                cpy_casa_nova.remove_class("nowcasa")
                cpy_casa_antiga.add_class("nowcasa")

            # se uma das casas for a última a ser tratada, guarda a referenciação para retornar no final da função
            if cpy_casa_antiga == casa:
                orig = cpy_casa_nova
            elif cpy_casa_nova == casa:
                orig = cpy_casa_antiga

            # se uma das casas for do rei, atualiza a nova posição do rei no tabuleiro
            if cpy_casa_antiga.text == REI:
                self.rei_branco = cpy_casa_antiga if cpy_casa_antiga.cor_fonte == "#ffffff" else self.rei_branco
                self.rei_preto = cpy_casa_antiga if cpy_casa_antiga.cor_fonte == "black" else self.rei_preto
            if cpy_casa_nova.text == REI:
                self.rei_branco = cpy_casa_nova if cpy_casa_nova.cor_fonte == "#ffffff" else self.rei_branco
                self.rei_preto = cpy_casa_nova if cpy_casa_nova.cor_fonte == "black" else self.rei_preto

        # volta a ser None para corrigir o bug de duplo clique para seleção
        self.old_casa = None
        return orig


    def on_mount(self):
        self.set_interval(1, self.relogio)


app = Tabuleiro()
app.run()
