### Maquina de estados do jogo. Contem:
### - Telas de menu e submenus
### - Estados de jogo singleplayer/multiplayer
### - Transicoes entre telas

# Bibliotecas
import pyxel
from config import *

# Classe para o Menu Principal do jogo
class MenuState:
    # Construtor
    # Prepara menu principal com opcoes basicas
    def __init__(self, game): # "game" eh passado no construtor da classe "Game" do "main.py", sendo a instancia do jogo
        self.game = game # Recebe a instancia do jogo
        self.selected = 0 # Recebe a posicao que o jogador vai selecionar ("Singleplayer" ou "Multiplayer"). Comeca com "Singleplayer"
        self.options = ["Singleplayer", "Multiplayer"] # Opcoes do menu principal
    
    # Processa selecao de opcoes do menu principal
    def update(self):
        # Pula para a proxima opcao do menu principal
        if pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_S) :
            # Se estava na opcao 0: 0 + 1 = 1 -> 1 % 2 = 1 (segunda opcao)
            # Se estava na opcao 1: 1 + 1 = 2 -> 2 % 2 = 0 (volta para a primeira opcao)
            self.selected = (self.selected + 1) % 2 
        elif pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W):
            # Se estava na opcao 0: 0 - 1 = -1 -> -1 % 2 = 1 (segunda opcao) -> Resto de divisao negativa em python sempre retorna valor positivo
            # Se estava na opcao 1: 1 - 1 = 0 -> 0 % 2 = 0 (primeira opcao)
            self.selected = (self.selected - 1) % 2
        
        # Se o usuario apertar "Enter" vai para o proximo menu
        if pyxel.btnp(pyxel.KEY_RETURN):
            # Se estava na opcao "Singleplayer", vai para o jogo normal
            if self.selected == 0:
                self.game.change_state(GameState(self.game))

            # Se estava na opcao "Multiplayer", vai para o menu do multiplayer
            else:
                self.game.change_state(MultiplayerMenuState(self.game))

        # Se o usuario apertar "Esc", fecha o jogo
        if pyxel.btnp(pyxel.KEY_ESCAPE):  
            pyxel.quit() # Fecha o jogo no menu principal
            
    # Renderiza texto e botoes do menu principal
    def draw(self):
        # Limpa a tela
        pyxel.cls(COLOR_BG)
        # Escreve o titulo do jogo
        pyxel.text(50, 40, "River Raid 3", COLOR_TEXT)

        # Marca a opcao em que o jogador esta selecionando no menu
        for i, opt in enumerate(self.options): # faz um looping pelas opcoes
            # "color" recebe:
            #   - Se "i" nao for a opcao selecionada, coloca a cor normal de texto.
            #   - Se "i" for a opcao selecionada, coloca uma cor de destaque nele
            color = COLOR_TEXT if i != self.selected else COLOR_TEXT_HIGHLIGHT

            # Pinta as opcoes do menu com as suas respectivas cores
            # "i * 20" calcula a posicao em Y de cada opcao.
            #   - 1 opcao: (i = 0): 60 + (0*20) = 60
            #   - 2 opcao: (i = 1): 60 + (1*20) = 80
            # "opt" recebe o texto de cada opcao
            pyxel.text(50, 60 + (i*20), opt, color)

# Classe para o menu de multiplayer (escolhe entre host ou join game)
class MultiplayerMenuState:
    # Construtor
    # Prepara menu de multiplayer (host/client)
    def __init__(self, game): # "game" eh passado no construtor da classe "Game" do "main.py", sendo a instancia do jogo
        self.game = game # Recebe a instancia do jogo
        self.selected = 0 # Recebe a posicao que o jogador vai selecionar ("Host Game" ou "Join Game"). Comeca com "Host Game"
        self.options = ["Host Game", "Join Game"] # Opcoes do menu de multiplayer
    
    # Gerencia escolha entre hospedar ou conectar em um jogo
    def update(self):
        # Se o usuario apertar "Esc", volta para o menu principal
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self.game.change_state(MenuState(self.game))
        
        # Pula para a proxima opcao do menu de multiplayer
        if pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_S) :
            # Se estava na opcao 0: 0 + 1 = 1 -> 1 % 2 = 1 (segunda opcao)
            # Se estava na opcao 1: 1 + 1 = 2 -> 2 % 2 = 0 (volta para a primeira opcao)
            self.selected = (self.selected + 1) % 2 
        elif pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W):
            # Se estava na opcao 0: 0 - 1 = -1 -> -1 % 2 = 1 (segunda opcao) -> Resto de divisao negativa em python sempre retorna valor positivo
            # Se estava na opcao 1: 1 - 1 = 0 -> 0 % 2 = 0 (primeira opcao)
            self.selected = (self.selected - 1) % 2
    
    # Mostra opcoes de multiplayer na tela
    def draw(self):
        # Limpa a tela
        pyxel.cls(COLOR_BG)
        
        # Escreve "Multiplayer" na tela
        pyxel.text(50, 40, "Multiplayer", COLOR_TEXT)

        # Marca a opcao em que o jogador esta selecionando no menu
        for i, opt in enumerate(self.options): # faz um looping pelas opcoes
            # "color" recebe:
            #   - Se "i" nao for a opcao selecionada, coloca a cor normal de texto.
            #   - Se "i" for a opcao selecionada, coloca uma cor de destaque nele
            color = COLOR_TEXT if i != self.selected else COLOR_TEXT_HIGHLIGHT

            # Pinta as opcoes do menu com as suas respectivas cores
            # "i * 20" calcula a posicao em Y de cada opcao.
            #   - 1 opcao: (i = 0): 60 + (0*20) = 60
            #   - 2 opcao: (i = 1): 60 + (1*20) = 80
            # "opt" recebe o texto de cada opcao
            pyxel.text(50, 60 + (i*20), opt, color)

        # Escreve na tela "Pressione ESC para voltar"
        pyxel.text(20, 100, "Pressione ESC para voltar", COLOR_TEXT)

# Classe para o menu de pause do jogo
class PauseMenuState:
    # Construtor
    # Prepara o menu de pause
    def __init__(self, game): # "game" eh passado no construtor da classe "Game" do "main.py", sendo a instancia do jogo
        self.game = game # Recebe a instancia do jogo
        self.selected = 0 # Recebe a posicao que o jogador vai selecionar ("Continuar", "Menu Principal"). Comeca com "Continuar"
        self.options = ["Continuar", "Menu Principal"] # Opcoes do menu de pause
    
    # Gerencia escolha entre continuar o jogo ou voltar para o menu principal
    def update(self):
        # Pula para a proxima opcao do menu de multiplayer
        if pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_S) :
            # Se estava na opcao 0: 0 + 1 = 1 -> 1 % 2 = 1 (segunda opcao)
            # Se estava na opcao 1: 1 + 1 = 2 -> 2 % 2 = 0 (volta para a primeira opcao)
            self.selected = (self.selected + 1) % 2 
        elif pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W):
            # Se estava na opcao 0: 0 - 1 = -1 -> -1 % 2 = 1 (segunda opcao) -> Resto de divisao negativa em python sempre retorna valor positivo
            # Se estava na opcao 1: 1 - 1 = 0 -> 0 % 2 = 0 (primeira opcao)
            self.selected = (self.selected - 1) % 2
            
        # Se o usuario apertar "Enter" no menu de pause:
        if pyxel.btnp(pyxel.KEY_RETURN):
            # Se tiver na primeira opcao "Continuar"
            if self.selected == 0:
                self.game.change_state(self.game.previous_state) # Continua o jogo
            
            # Se tiver na segunda opcao "Menu Principal"
            else:
                self.game.change_state(MenuState(self.game)) # Volta para o menu principal
        
        # Se o usuario apertar "Esc" no menu de pause:
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self.game.change_state(self.game.previous_state) # Continua o jogo
    
    # Mostra opcoes do menu de pause na tela
    def draw(self):
        # Limpa a tela
        pyxel.cls(COLOR_BG)

        # Escreve "Jogo Pausado" na tela
        pyxel.text(50, 40, "Jogo Pausado", COLOR_TEXT)

        # Marca a opcao em que o jogador esta selecionando no menu
        for i, opt in enumerate(self.options): # faz um looping pelas opcoes
            # "color" recebe:
            #   - Se "i" nao for a opcao selecionada, coloca a cor normal de texto.
            #   - Se "i" for a opcao selecionada, coloca uma cor de destaque nele
            color = COLOR_TEXT if i != self.selected else COLOR_TEXT_HIGHLIGHT

            # Pinta as opcoes do menu com as suas respectivas cores
            # "i * 20" calcula a posicao em Y de cada opcao.
            #   - 1 opcao: (i = 0): 60 + (0*20) = 60
            #   - 2 opcao: (i = 1): 60 + (1*20) = 80
            # "opt" recebe o texto de cada opcao
            pyxel.text(50, 60 + (i*20), opt, color)

# TODO: Implementar essa classe apos se certificar que "network.py" esta totalmente implementado
class ConnectState:
    # Construtor
    # Tela para inserir IP/porta do servidor
    def __init__(self, game):
        pass
    
    # Captura input do usuario para dados de conexao
    def update(self):
        pass
    
    # Exibe campos de texto e instrucoes
    def draw(self):
        pass

# TODO: Implementar essa classe apos se certificar que "network.py" esta totalmente implementado
class HostGameState:
    # Construtor
    # Configura estado de hospedagem do jogo
    def __init__(self, game):
        pass
    
    # Controla inicio do jogo e saida do menu
    def update(self):
        pass
    
    # Mostra informacoes de conexao para outros jogadores
    def draw(self):
        pass

# TODO: # TODO: Apos se certificar que "network.py" esta totalmente implementado, ajustar a parte do funcionamento do multiplayer
class GameState:
    # Construtor
    # Estado principal onde o jogo acontece
    def __init__(self, game, is_multiplayer=False): # "game" eh passado no construtor da classe "Game" do "main.py", sendo a instancia do jogo
        self.game = game # Recebe a instancia do jogo
        self.player_x = 50 # Recebe a posicao em X do jogador
        self.player_y = 50 # Recebe a posicao em Y do jogador
        self.is_multiplayer = is_multiplayer # Recebe se o jogo estah com multiplayer ativado ou nao
    
    # Gerencia a logica do jogo
    def update(self):
       # Pausa o jogo com ESC
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self.game.previous_state = self  # Guarda estado atual
            self.game.change_state(PauseMenuState(self.game)) # Troca o estado para o menu de pause
            return  # Sai da atualizacao


        # Atualiza logica do jogo (movimento, colisoes, rede)
        if pyxel.btn(pyxel.KEY_A):
            self.player_x -= 1
        if pyxel.btn(pyxel.KEY_D):
            self.player_x += 1
        if pyxel.btn(pyxel.KEY_W):
            self.player_y -= 1
        if pyxel.btn(pyxel.KEY_S):
            self.player_y += 1

        ## Trava o player dentro da tela
        # TODO: Trocar "16" pela altura e largura do player quando tiver o modelo dos avioes
        # Player nao sai da tela no eixo X
        # - min(self._player_x, self.largura_tela - 16): impede que o jogador va alem do lado direito da tela
        # - max(0, ...): impede que o jogador va alem do lado esquerdo da tela
        # - "16" eh a largura do jogador (mudar depois)
        self.player_x = max(0, min(self.player_x, SCREEN_WIDTH - 16))

        # Player nao sai da tela no eixo Y
        # - min(self._player_y, self.altura_tela - 16): impede que o jogador va alem da parte inferior da tela
        # - max(0, ...): impede que o jogador va alem da parte superior da tela
        # - "16" eh a altura do jogador (mudar depois)
        self.player_y = max(0, min(self.player_y, SCREEN_HEIGHT - 16))
    
    # Renderiza mapa, jogador e elementos do game
    def draw(self):
        # Limpa a tela
        pyxel.cls(COLOR_BG)

        # TODO: Mudar isso mais na frente para um modelo do jogador mesmo (um aviao)
        # Desenha o jogador
        pyxel.rect(self.player_x, self.player_y, 16, 16, COLOR_PLAYER)
        