import chess


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





dicionarioPecas = {
   'r':TORRE,
   'n':CAVALO,
   'b':BISPO,
   'k':REI,
   'q':RAINHA,
   'p':PEAO,
   'R':TORRE,
   'N':CAVALO,
   'B':BISPO,
   'K':REI,
   'Q':RAINHA,
   'P':PEAO,
   'None':VAZIO
}

board = chess.Board()      
lista = []

#Jogo em si
while True:
    print('\r',ROWS)
    
    #Loop que identifica se o movimento é correto ou não 
    while True:
        try:
            print("Vez das brancas!" if board.turn else "Vez das pretas!")
            lance = chess.Move.from_uci(input("Digite seu lance: "))

	    #Se movimento for legal ele parte para a próxima iteração (rodada)
            if lance in board.legal_moves:
                board.push(lance)
                break
            else:
                print("Lance ilegal, tente novamente!")

        except ValueError:
            print("Formato inválido! Use a notação UCI (ex: e2e4)")
        
    #Sistema para renderizar o tabuleiro da GUI com base no FEN atual
    for i in range(8):
        linha = []
        for j in range(8):
           linha.append(dicionarioPecas[str(board.piece_at((i*8)+j))])
        lista.append(tuple(linha))
    ROWS = lista 
