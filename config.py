### Arquivo que define as constantes de configuracao para o jogo em geral

# Tela
SCREEN_WIDTH = 160      # Largura da janela
SCREEN_HEIGHT = 180     # Altura da janela
FPS = 60                # Frames por segundo
FULLSCREAM = False      # Define se o jogo vai comecar ou nao em tela cheia
     

# Rede
NETWORK_PORT = 5555         # Porta padrao para conexao
MAX_PACKET_SIZE = 4096      # Tamanho maximo dos dados por pacote (em bytes)
TIMEOUT = 3                 # Tempo (em segundos) para dar um Timeout no cliente ou no host, caso a conexao seja perdida
RECONNECT_INTERVAL = 1.0    # Intervalo (em segundos) entre tentativas de reconexao do cliente, caso o host caia
MAX_IP_LENGTH = 15          # Tamanho maximo para um IP
MAX_PORT_LENGTH = 5         # Tamanho maximo para uma Porta
MAX_QUEUED_PACKETS = 30     # Capacidade maxima da fila de dados
NETWORK_PRIORITY = {                # Quanto MENOR o valor, MAIOR a prioridade
    'shot': 0,                      # Tiros (maxima prioridade)
    'life': 1,                      # Atualizacoes de vida
    'hud': 1,                       # HUD (prioridade similar a do 'life')
    'moviment': 2,                  # Posicao do jogador
    'map_chunk': 3,                 # Dados do mapa
    'heartbeat': 4                  # Heartbeats (prioridade mais baixa)
}

# Cores (paleta Pyxel)
COLOR_BG = 0                # Cor de fundo
COLOR_PLAYER = 9            # Cor do jogador
COLOR_PLAYER2_GENERIC = 12  # Cor generica para o segundo jogador
COLOR_TEXT = 7              # Cor do texto
COLOR_BULLET = 7            # Cor do tiro
COLOR_FUEL = 11             # Cor da gasolina (HUD)
COLOR_HEART_FULL = 8        # Cor dos coracoes cheio (HUD)
COLOR_HEART_EMPTY = 1       # Cor dos coracoes vazios (HUD)
COLOR_TEXT_HIGHLIGHT = 9    # Cor para um texto ficar marcado quando eh selecionado em algum menu
COLOR_SUCCESS = 11          # Cor usada para mensagem de Sucesso de conexao
COLOR_ERROR = 8             # Cor usada para mensagens de erro de conexao
COLOR_HUD_LINE = 7          # Cor da linha da HUD que separa a HUD do jogo
COLOR_FUEL_BORDER = 7       # Cor da borda da barra de gasolina da HUD do jogo


# Mensagem de conexao (Menus do Multiplayer)
MESSAGE_DISPLAY_TIME = 60   # Contador de quantos frames uma mensagem de sucesso/erro de conexao vai ficar na tela (em FPS)

# Configuracoes Gerais do Jogo
PLAYER_SPEED = 1        # Velocidade do jogador
# TODO: Modificar ou remover essas duas constantes quando tiver feito as pixel arts dos avioes
PLAYER_WIDTH = 16           # Largura do jogador
PLAYER_HEIGHT = 16          # Altura do jogador
SHOT_COOLDOWN = 0.3         # Intervalo minimo entre tiros (em segundos)
BULLET_SPEED = 4            # Velocidade do tiro (pixels por frame)
BULLET_WIDTH  = 2           # Largura do tiro
BULLET_HEIGHT = 4           # Altura do tiro
MAX_LIVES = 3               # Numero maximo de vidas do jogador
FUEL_CONSUMPTION_RATE = 10  # Unidades de combustivel consumidas por segundo


# HUD
HUD_HEIGHT = 24         # Tamanho da HUD 

# Configuracoes da barra de combustivel (HUD)
FUEL_BAR_W = 100        # Largura total da barra de combustivel (em pixels)
FUEL_BAR_H = 8          # Altura da barra de combustivel (em pixels)
MAX_FUEL = 100          # Valor maximo de combustivel (100% = barra cheia)

# Configuracoes dos coracoes de vida (HUD)
HEART_SIZE = 8          # Tamanho de cada coracao (largura e altura em pixels)
HEART_GAP = 4           # Espaco entre os coracoes (em pixels)

# Espacamentos gerais da interface (HUD)
PADDING = 4             # Espaco padrao entre elementos/bordas (em pixels)