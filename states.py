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


        # Se o usuario apertar "Enter" vai para o proximo menu
        if pyxel.btnp(pyxel.KEY_RETURN):
            # Se estava na opcao "Host Game", vai para o menu de Host
            if self.selected == 0:
                self.game.change_state(HostGameState(self.game))

            # Se estava na opcao "Join Game", vai para o menu de conexao com algum host
            else:
                self.game.change_state(ConnectState(self.game))
    
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
    def __init__(self, game): # "game" eh passado no construtor da classe "Game" do "main.py", sendo a instancia do jogo
        self.game = game # Recebe a instancia do jogo
        self.ip_input = "" # Ip digitado pelo usuario
        self.port_input = "" # Porta digitado pelo usuario
        self.current_input = "ip"  # Campo atual que o usuario estah selecionando (IP ou Porta)
        self.message = "" # Mensagem de sucesso/erro de conexao 
        self.message_timer = 0 # Quanto tempo (frames) a mensagem de sucesso/erro de conexao ficara sendo exibida
    
    # Captura input do usuario para dados de conexao
    def update(self):
        # Se o usuario apertar "Esc" volta para o Menu de multiplayer
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self.game.change_state(MultiplayerMenuState(self.game))
        
        # Navegacao entre os campos de IP e de porta
        if pyxel.btnp(pyxel.KEY_TAB):
            # Se o input atual estiver em "ip", ao pressionar TAB, pula para "port"
            # Caso contrario, volta para "ip"
            self.current_input = "port" if self.current_input == "ip" else "ip"
        
        # Se o usuario apagar o que ele escreveu, atualiza o campo de input
        if pyxel.btnp(pyxel.KEY_BACKSPACE):
            # Se o input atual estiver selcionado em ip e tem texto no campo do ip
            if self.current_input == "ip" and self.ip_input:
                self.ip_input = self.ip_input[:-1] # Remove o ultimo caractere do ip
            
            # Se o input atual estiver em porta e tem texto na porta
            elif self.current_input == "port" and self.port_input:
                self.port_input = self.port_input[:-1] # Remove o ultimo caractere da porta
        
        # Se o usuario apertar "Enter", tenta conexao
        if pyxel.btnp(pyxel.KEY_RETURN):
            # Se conectar, coloca uma mensagem de sucesso, atualiza o timer da mensagem e entra no jogo
            if self.validate_inputs():
                # TODO: Fazer a conexao em rede antes de chamar o jogo
                # TODO: Atualizar a logica de atualizacao da mensagem de conexao sucedida (nao estah mostrando na tela)
                self.message = "Conectado com Sucesso"
                self.message_timer = MESSAGE_DISPLAY_TIME # Exibe mensagem por X frames (olhar em config.py)
                self.game.change_state(GameState(self.game, is_multiplayer=True)) # Entra no jogo
            
            # Se a conexao falhar, coloca uma mensagem de erro e atualiza o timer da mensagem
            else:
                self.message = "Dados de Conexao Invalidos"
                self.message_timer = MESSAGE_DISPLAY_TIME # Exibe mensagem por X frames (olhar em config.py)
        
        # Captura a entrada de texto digitado pelo usuario
        self.handle_text_input()

        # Atualiza timer da mensagem a cada frame ateh chegar em zero (nao vai mostrar mais)
        if self.message_timer > 0:
            self.message_timer -= 1
    
    # Faz uma validacao basica no imput do IP e da Porta
    def validate_inputs(self):
        # Verifica se porta nao eh numerica
        if not self.port_input.isdigit():
            return False # Falha se nao for
            
        # Verifica formato basico de IP
        parts = self.ip_input.split('.') # Divide o ip em uma lista de strings, separando por ponto
        # Se a lista das partes nao tiver tamanho 4 (logo nao tem 4 pontos, que eh o formato esperado de um IP)
        print(parts)
        if len(parts) != 4:
            return False # Erro
        # Se o IP o tamanho correto
        else:
            # Passa por cada parte
            for part in parts:
                # Verifica se cada parte tem algum digito escrito nela
                if not part.isdigit():
                    return False # Falha se nao tiver digito
            

        return True # Sucesso (todas as verificacoes foram sucedidas)

    # Captura a entrada de texto
    def handle_text_input(self):        
        # "key" recebe os valores das teclas numericas (0 ateh 9)
        for key in range(pyxel.KEY_0, pyxel.KEY_9 + 1):
            # Se alguma tecla numerica for pressionada, atualiza o campo correspondente
            if pyxel.btnp(key):
                # Pega o valor numerico digitado e subtrai com o valor zero (em relacao a como sao definidos pelo Pyxel) 
                # para receber o valor real que foi digitado (de 0 ateh 9)
                char = str(key - pyxel.KEY_0) # Pega o valor digitado e converte para caractere
                self.update_field(char) # Atualiza no campo correspondete
        
        # Especifico para o IP:
        # Se o usuario digitar ponto '.' e o campo selecionado for o IP
        if pyxel.btnp(pyxel.KEY_PERIOD) and self.current_input == "ip":
            self.update_field('.') # Atualiza o campo com o ponto digitado
    
    # Atualiza o campo correspondente (ip ou porta) com o valor digitado
    def update_field(self, char):
        # Se o campo atual for IP
        if self.current_input == "ip":
            # Se o tamanho do campo for menor do que 16 (Tamanho maximo de caracteres de um IPv4)
            if len(self.ip_input) < 15: # "15" por causa que o vetor comeca a partir de "0"
                self.ip_input += char # Atualiza o campo do IP com o caractere digitado
        
        # Se o campo atual for a Porta
        else:
            if len(self.port_input) < 5:  # Porta vai ateh 65535 (5 digitos)
                self.port_input += char # Atualiza o campo da porta com o valor numerico digitado


    # Exibe campos de texto e instrucoes
    def draw(self):
        # Limpa a tela
        pyxel.cls(COLOR_BG)
        # Imprime mensagem
        pyxel.text(20, 20, "Conecte a um Host", COLOR_TEXT)
        
        # Imprime o campo IP
        pyxel.text(20, 40, "IP:", COLOR_TEXT)
        # Se o IP estiver selecionado, deixa ele marcado, caso contrario, deixa ele com a cor normal
        border_color = COLOR_TEXT_HIGHLIGHT if self.current_input == "ip" else COLOR_TEXT
        pyxel.rectb(40, 40, 100, 8, border_color) # Desenha um retangulo apenas com a borda
        pyxel.text(42, 42, self.ip_input, COLOR_TEXT) # Desenha o que o usuario ja digitou ateh o momento no IP
        
        # Imprime o campo Porta
        pyxel.text(20, 60, "Port:", COLOR_TEXT)
        # Se a Porta estiver selecionada, deixa ela marcada, caso contrario, deixa ela com a cor normal
        border_color = COLOR_TEXT_HIGHLIGHT if self.current_input == "port" else COLOR_TEXT
        pyxel.rectb(40, 60, 50, 8, border_color) # Desenha um retangulo apenas com a borda
        pyxel.text(42, 62, self.port_input, COLOR_TEXT) # Desenha o que o usuario ja digitou ateh o momento na Porta
        
        # Mensagem de status
        if self.message_timer > 0: # Se o timer for maior do que zero, desenha a mensagem de sucesso/erro de conexao
            # Se estiver escrito "Sucesso" dentro da mensagem, coloca na cor para suceso
            # Caso contrario colocar a cor para falha
            color = COLOR_SUCCESS if "Sucesso" in self.message else COLOR_ERROR
            pyxel.text(20, 80, self.message, color) # Desenha a mensagem na tela
        
        # Campos de ajuda de navegacao no menu
        pyxel.text(10, 90, "TAB: Troca de Campo", COLOR_TEXT)
        pyxel.text(10, 100, "ENTER: Connectar", COLOR_TEXT)
        pyxel.text(10, 110, "ESC: Voltar", COLOR_TEXT)


# TODO: Implementar essa classe apos se certificar que "network.py" esta totalmente implementado
class HostGameState:
    # Construtor
    # Configura estado de hospedagem do jogo
    def __init__(self, game): # "game" eh passado no construtor da classe "Game" do "main.py", sendo a instancia do jogo
        self.game = game # Recebe a instancia do jogo
        # TODO: Modificar isso aqui depois
        self.message = "" # Mensagem de sucesso/erro de conexao 
        self.message_timer = 0 # Quanto tempo (frames) a mensagem de sucesso/erro de conexao ficara sendo exibida
        # TODO: Implementar depois no network.py
        self.ip = "IP Generico"
        self.port = NETWORK_PORT # Porta padrao
    

    # Controla inicio do jogo e saida do menu
    def update(self):
        # Se o usuario apertar "Enter", vai para o jogo normal e ativa o multiplayer (de forma assincrona)
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.game.change_state(GameState(self.game, is_multiplayer=True))
        
        # Se o usuario apertar "Esc", volta para a tela de menu do multiplayer
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self.game.change_state(MultiplayerMenuState(self.game))

        # Atualiza timer da mensagem a cada frame ateh chegar em zero (nao vai mostrar mais)
        if self.message_timer > 0:
            self.message_timer -= 1
    
    # Mostra informacoes de conexao para outros jogadores
    def draw(self):
        # Limpa a tela
        pyxel.cls(COLOR_BG)
        # Imprime informacoes sobre o IP e a porta do usuario (para ele passar para outra pessoa conectar)
        pyxel.text(20, 20, "Hosting Game", COLOR_TEXT)
        pyxel.text(20, 40, f"IP: {self.ip}", COLOR_TEXT)
        pyxel.text(20, 60, f"Port: {self.port}", COLOR_TEXT)

        # Mensagens de navegacao entre menus/jogo
        pyxel.text(10, 90, "Pressione ENTER para comecar o jogo", COLOR_TEXT_HIGHLIGHT)
        pyxel.text(10, 100, "Pressione ESC para voltar", COLOR_TEXT)


# TODO: Apos se certificar que "network.py" esta totalmente implementado, ajustar a parte do funcionamento do multiplayer
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
        