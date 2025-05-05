### Arquivo que define as constantes de configuracao para o jogo em geral

# Tela
SCREEN_WIDTH = 160      # Largura da janela
SCREEN_HEIGHT = 180     # Altura da janela
FPS = 60                # Frames por segundo
FULLSCREAM = False          # Define se o jogo vai comecar ou nao em tela cheia

# Rede
NETWORK_PORT = 5555         # Porta padrao para conexao
MAX_PACKET_SIZE = 4096        # Tamanho maximo dos dados por pacote (em bytes)
TIMEOUT = 3                 # Tempo (em segundos) para dar um Timeout no cliente ou no host, caso a conexao seja perdida
RECONNECT_INTERVAL = 1.0    # Intervalo (em segundos) entre tentativas de reconexao do cliente, caso o host caia
MAX_IP_LENGTH = 15          # Tamanho maximo para um IP
MAX_PORT_LENGTH = 5         # Tamanho maximo para uma Porta

# Cores (paleta Pyxel)
COLOR_BG = 0                # Cor de fundo
COLOR_PLAYER = 9            # Cor do jogador
COLOR_PLAYER2_GENERIC = 12  # Cor generica para o segundo jogador
COLOR_TEXT = 7              # Cor do texto
COLOR_TEXT_HIGHLIGHT = 9    # Cor para um texto ficar marcado quando eh selecionado em algum menu
COLOR_SUCCESS = 11          # Cor usada para mensagem de Sucesso de conexao
COLOR_ERROR = 8             # Cor usada para mensagens de erro de conexao
COLOR_HUD_LINE = 7          # Cor da linha da HUD que separa a HUD do jogo
COLOR_FUEL_BORDER = 7       # Cor da borda da barra de gasolina da HUD do jogo
COLOR_FUEL = 11             # Cor da gasolina (HUD)
COLOR_HUD_LINE = 7          # Cor da linha da HUD que separa a HUD do jogo
COLOR_FUEL_BORDER = 7       # Cor da borda da barra de gasolina da HUD do jogo
COLOR_FUEL = 11             # Cor da gasolina (HUD)

# Mensagem de conexao (Menus do Multiplayer)
MESSAGE_DISPLAY_TIME = 60   # Contador de quantos frames uma mensagem de sucesso/erro de conexao vai ficar na tela (em FPS)

# Configuracoes Gerais do Jogo
PLAYER_SPEED = 1        # Velocidade do jogador
# TODO: Modificar ou remover essas duas constantes quando tiver feito as pixel arts dos avioes
PLAYER_WIDTH = 16       # Largura do jogador
PLAYER_HEIGHT = 16      # Altura do jogador

# HUD
MAX_LIVES = 3               # Quantidade maxima de vida de um jogador
MAX_FUEL = 100              # Quantidade maxima de gasolina de um jogador
FUEL_CONSUMPTION_RATE = 50  # Unidades de combustivel consumidas por segundo
HUD_HEIGHT = 30             # Tamanho da HUD 
PADDING = 4             # Espaco padrao entre elementos/bordas (em pixels)
FUEL_BAR_H = 8          # Altura da barra de combustivel (em pixels)
FUEL_BAR_W = 100        # Largura total da barra de combustivel (em pixels)
HEART_SIZE = 8          # Tamanho de cada coracao (largura e altura em pixels)
HEART_GAP = 4           # Espaco entre os coracoes (em pixels)