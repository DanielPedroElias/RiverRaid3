## Define as constantes de configuracao para o jogo

# Tela
SCREEN_WIDTH = 160      # Largura da janela
SCREEN_HEIGHT = 120     # Altura da janela
FPS = 60                # Frames por segundo

# Rede
NETWORK_PORT = 5555     # Porta padrao para conexao
MAX_PACKET_SIZE = 1024  # Tamanho maximo dos dados por pacote

# Cores (paleta Pyxel)
COLOR_BG = 0                # Cor de fundo
COLOR_PLAYER = 9            # Cor do jogador
COLOR_RIVER = 12            # Cor do rio
COLOR_TEXT = 7              # Cor do texto
COLOR_TEXT_HIGHLIGHT = 9    # Cor que o texto fica marcado quando selecionado em algum menu
COLOR_SUCCESS = 11          # Cor usada para mensagem de Sucesso de conexao
COLOR_ERROR = 8             # Cor usada para mensagens de erro
MESSAGE_DISPLAY_TIME = 60   # Contador de quantos frames uma mensagem de sucesso/erro de conexao vai ficar na tela (em FPS)