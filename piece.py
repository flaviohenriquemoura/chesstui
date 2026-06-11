
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


DAMA = """
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
    (TORRE, CAVALO, BISPO, DAMA, REI, BISPO, CAVALO, TORRE, VAZIO),
    (PEAO,  PEAO,   PEAO,  PEAO, PEAO,   PEAO,  PEAO,   PEAO, VAZIO),
    (VAZIO, VAZIO,  VAZIO, VAZIO, VAZIO,  VAZIO, VAZIO,  VAZIO, DAMA),
    (VAZIO, VAZIO,  VAZIO, VAZIO, VAZIO,  VAZIO, VAZIO,  VAZIO, TORRE),
    (VAZIO, VAZIO,  VAZIO, VAZIO, VAZIO,  VAZIO, VAZIO,  VAZIO, BISPO),
    (VAZIO, VAZIO,  VAZIO, VAZIO, VAZIO,  VAZIO, VAZIO,  VAZIO, CAVALO),
    (PEAO,  PEAO,   PEAO,  PEAO, PEAO,   PEAO,  PEAO,   PEAO, VAZIO),
    (TORRE, CAVALO, BISPO, DAMA, REI, BISPO, CAVALO, TORRE, VAZIO)
]

GAME_OVER = """
 ▗▄▄▖ ▗▄▖ ▗▖  ▗▖▗▄▄▄▖ 
▐▌   ▐▌ ▐▌▐▛▚▞▜▌▐▌       
▐▌▝▜▌▐▛▀▜▌▐▌  ▐▌▐▛▀▀▘    
▝▚▄▞▘▐▌ ▐▌▐▌  ▐▌▐▙▄▄▖    
 ▗▄▖ ▗▖  ▗▖▗▄▄▄▖▗▄▄▖ 
▐▌ ▐▌▐▌  ▐▌▐▌   ▐▌ ▐▌
▐▌ ▐▌▐▌  ▐▌▐▛▀▀▘▐▛▀▚▖
▝▚▄▞▘ ▝▚▞▘ ▐▙▄▄▖▐▌ ▐▌
"""

WINS = """
▗▖ ▗▖▗▄▄▄▖▗▖  ▗▖ ▗▄▄▖
▐▌ ▐▌  █  ▐▛▚▖▐▌▐▌   
▐▌ ▐▌  █  ▐▌ ▝▜▌ ▝▀▚▖
▐▙█▟▌▗▄█▄▖▐▌  ▐▌▗▄▄▞▘                  
"""



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
    DAMA: 'q',
    TORRE: 'r',
    BISPO: 'b',
    CAVALO: 'n'
}
