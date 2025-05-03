### Modulo de estados do jogo. Contem:
### - Telas de menu e submenus
### - Estados de jogo para singleplayer/multiplayer
### - Transicoes entre telas

# Bibliotecas
import pyxel            # Engine do jogo
from config import *    # Importa constantes e configuracoes do arquivo "config.py"
from entities import *  # Importa as classes de entidades do jogo (jogador, arvores, etc.)

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

# Classe que tem o menu de Conexao com algum Host SCREEN_HEIGHT
class ConnectState: 
    # Construtor
    def __init__(self, game): # "game" eh passado no construtor da classe "Game" do "main.py", sendo a instancia do jogo
        self.game = game # Recebe a instancia do jogo
        self.ip_input = "" # Ip digitado pelo usuario
        self.port_input = "" # Porta digitado pelo usuario
        self.waiting_for_connection = False  # Declara se o usuario apertou "Enter" e o jogo estah esperando conectar com o host
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
        
        # Se o usuario apertou "Enter" e nao estah esperando alguma outra conexao ser confirmada, tenta conectar
        if pyxel.btnp(pyxel.KEY_RETURN) and not self.waiting_for_connection:
            # Se o usuario digitou o IP e a Porta no formato correto
            if self.validate_inputs():
                # Tenta conectar com o Host
                ok = self.game.network.connect(self.ip_input, self.port_input)
                
                # Se a conexao for estabelecida, imprime uma mensagem para o usuario
                if ok:
                    self.waiting_for_connection = True # Marca como esperando conexao
                    self.message = "Conectando..." # Mensagem para o usuario
                
                # Se a tentavida de conexao falhou, escreve uma mensagem para o usuario
                else:
                    self.message = "Falha na conexão" # Mensagem para o usuario
                
                # Independente, se falou ou deu certo a conaxao, define um tempo para o texto para o usuario aparecer na tela
                self.message_timer = MESSAGE_DISPLAY_TIME

        # Se a conexao foi perdida durante a espera, permite nova tentativa
        if self.message_timer == 0 and self.waiting_for_connection and not self.game.network.connected:
            self.waiting_for_connection = False # Reseta a variavel de o usuario estar esperando uma conexao
            self.message = "Conexao perdida. Tente novamente." # Mensagem para o usuario
            self.message_timer = MESSAGE_DISPLAY_TIME / 2 # Tempo em que a mensagem vai ficar na tela

        # Quando a primeixa conexao for confirmada (uma especie de 'ACK'), entra no jogo
        if self.waiting_for_connection and self.game.network.connected:
            self.game.change_state(WaitingForHostState(self.game))  # Entra para um submenu que espera o Host iniciar o jogo

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
        
        # "key" recebe os valores das teclas numericas (0 ateh 9) do teclado numerico
        for key in range(pyxel.KEY_KP_1, pyxel.KEY_KP_0 + 1):
            # Se alguma tecla numerica (teclado numerico) for pressionada, atualiza o campo correspondente
            if pyxel.btnp(key):
                # TODO: Tentar melhorar essa logica de mapeamento do teclado numerico
                # Pega o valor numerico digitado e subtrai com o valor um (em relacao a como sao definidos pelo Pyxel) 
                # para receber o valor real que foi digitado (de 0 ateh 9)
                char = str(key - pyxel.KEY_KP_1 + 1) # Pega o valor digitado e converte para caractere
                
                # Se o usuario digitou "0", pega o valor correspondente e converte para caractere
                if key == pyxel.KEY_KP_0:
                    char = str(pyxel.KEY_KP_0 - pyxel.KEY_KP_0)

                self.update_field(char) # Atualiza no campo correspondete

        # Especifico para o IP:
        # Se o usuario digitar ponto '.' e o campo selecionado for o IP
        if pyxel.btnp(pyxel.KEY_PERIOD) and self.current_input == "ip":
            self.update_field('.') # Atualiza o campo com o ponto digitado
    
    # Atualiza o campo correspondente (ip ou porta) com o valor digitado
    def update_field(self, char):
        # Se o campo atual for IP
        if self.current_input == "ip":
            # Se o tamanho do campo for menor do que 15 (Tamanho maximo de caracteres de um IPv4)
            if len(self.ip_input) < MAX_IP_LENGTH: 
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

# Classe que tem o submenu em que o cliente aguarda o host iniciar o jogo
class WaitingForHostState:
    def __init__(self, game):
        self.game = game
        self.message = "Aguardando host iniciar o jogo..."
        self.waiting = True

    def update(self):
        d = self.game.network.data
        if isinstance(d, dict) and d.get('type') == 'game_start':
            self.game.change_state(GameState(
                self.game,
                is_multiplayer=True,
                is_host=False,
                initial_seed=d.get('seed'),
                initial_rio_centro=d.get('rio_centro')
            ))
            return

        if self.game.network.connected:
            self.game.network.send({'type': 'heartbeat'})

        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self.game.network.stop()
            self.game.change_state(MenuState(self.game))

    # Desenha informacoes para o usario na tela
    def draw(self):
        # Limpa a tela
        pyxel.cls(COLOR_BG)
        
        # Escreve mensagens para o usuario para informar ele que o Host ainda nao iniciou o jogo
        pyxel.text(20, 50, self.message, COLOR_TEXT)
        pyxel.text(20, 70, "Pressione ESC para cancelar", COLOR_TEXT)

# Classe que contem o submenu para 'Hostear' um jogo
class HostGameState:
    def __init__(self, game):
        self.game = game
        self.message = ""
        self.message_timer = 0
        
        if self.game.network.start_host():
            self.ip = self.game.network.local_ip
            self.port = self.game.network.port
        else:
            self.ip = "—"
            self.port = "—"
            self.message = "Erro ao iniciar host"
            self.message_timer = MESSAGE_DISPLAY_TIME

    def update(self):
        if self.game.network.connected:
            self.game.network.send({'type': 'heartbeat'})

        if pyxel.btnp(pyxel.KEY_RETURN):
            # Cria o estado do jogo primeiro
            game_state = GameState(self.game, is_multiplayer=True, is_host=True)
            
            # Envia dados iniciais
            initial_data = {
                'type': 'game_start',
                'seed': game_state.background.tree_manager.random_seed,
                'rio_centro': game_state.background.centro_rio_x
            }
            self.game.network.send(initial_data)
            
            self.game.change_state(game_state)

        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self.game.network.stop()
            self.game.change_state(MultiplayerMenuState(self.game))

        if self.message_timer > 0:
            self.message_timer -= 1
    

        
    # Controla inicio do jogo e saida do menu
    def update(self):
        # mantem cliente vivo (envia heartbeat) para evitar timeout
        if self.game.network.connected:
            self.game.network.send({'type': 'heartbeat'})

        # Se o usuario apertar "Enter", vai para o jogo normal e ativa o multiplayer (de forma assincrona)
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.game.network.send({'type': 'game_start'})
            self.game.change_state(GameState(self.game, is_multiplayer=True, is_host=True)) # Entra no jogo (com multiplayer ativo)
        
        # Se o usuario apertar "Esc", volta para a tela de menu do multiplayer
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self.game.network.stop()  # Fecha a conexao
            self.game.change_state(MultiplayerMenuState(self.game))

        # Atualiza timer da mensagem a cada frame ateh chegar em zero (nao vai mostrar mais)
        if self.message_timer > 0:
            self.message_timer -= 1
    
    # Mostra informacoes do IP e Porta para outros jogadores poderem se conectar
    def draw(self):
        # Limpa a tela
        pyxel.cls(COLOR_BG)
        # Imprime informacoes sobre o IP e a porta do usuario (para ele passar para outra pessoa conectar)
        pyxel.text(20, 20, "Hosting Game", COLOR_TEXT)
        pyxel.text(20, 40, f"IP: {self.ip}", COLOR_TEXT)
        pyxel.text(20, 60, f"Port: {self.port}", COLOR_TEXT)


        # Mostra status da conexao
        if self.game.network.connected:
            pyxel.text(20, 80, "Cliente conectado", COLOR_SUCCESS)
        # Se nao tiver nenhum cliente conectado
        else:
            pyxel.text(20, 80, "Aguardando cliente...", COLOR_TEXT)

        # Mensagens de navegacao entre menus/jogo
        pyxel.text(10, 90, "Pressione ENTER para comecar o jogo", COLOR_TEXT_HIGHLIGHT)
        pyxel.text(10, 100, "Pressione ESC para voltar", COLOR_TEXT)

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
        # Mantem a rede ativa durante o pause (jogo continua funcionando) se estiver no modo online
        if isinstance(self.game.previous_state, GameState) and self.game.previous_state.is_multiplayer:
            self.game.previous_state.send_data()  # Continua enviando dados
            self.game.previous_state.receive_data()  # Continua recebendo dados


        # Navega entre as opcoes do menu de pause
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
                # Se o jogo estiver no modo Multiplayer, fecha a conexao
                if isinstance(self.game.previous_state, GameState) and self.game.previous_state.is_multiplayer:
                    self.game.network.stop() # Fecha a conexao
                
                self.game.change_state(MenuState(self.game)) # Volta para o menu principal
        
        # Se o usuario apertar "Esc" no menu de pause
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
from collections import deque

# Classe que gerencia o jogo principal (todos os estados, players, comunicacao via rede, etc.)
class GameState:
    def __init__(self, game, is_multiplayer=False, is_host=False, initial_seed=None, initial_rio_centro=None):
        self.game = game
        self.is_multiplayer = is_multiplayer
        self.is_host = is_host

        if is_host:
            self.player_x, self.player_y = 59, 104
            self.player2_x, self.player2_y = 79, 104
        else:
            self.player_x, self.player_y = 79, 104
            self.player2_x, self.player2_y = 59, 104

        self.background = Background(is_host=is_host)
        
        # Sincronização inicial
        if initial_seed:
            self.background.tree_manager.random_seed = initial_seed
            random.seed(initial_seed)
            self.background.tree_manager.reset_arvores()
        
        if initial_rio_centro and not is_host:
            self.background.centro_rio_x = initial_rio_centro
            self.background.target_centro_x = initial_rio_centro
                # Gerencia a logica do jogo
    def update(self):
        
        self.background.update()  

        # Envia e recebe dados do jogo se estiver no modo Multiplayer
        if self.is_multiplayer:
            self.send_data()  # Envia dados
            self.receive_data()  # Atualiza dados do segundo jogador

        # Se o usuario apertar "Esc", pausa o jogo
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self.game.previous_state = self  # Guarda estado atual do jogo (passando a instancia)
            self.game.change_state(PauseMenuState(self.game)) # Troca o estado para o menu de pause
            return  # Sai da atualizacao

        if not self.is_multiplayer or (self.is_multiplayer and self.game.network.connected):
            if pyxel.btn(pyxel.KEY_A):
                self.player_x -= PLAYER_SPEED
            if pyxel.btn(pyxel.KEY_D):
                self.player_x += PLAYER_SPEED
            if pyxel.btn(pyxel.KEY_W):
                self.player_y -= PLAYER_SPEED
            if pyxel.btn(pyxel.KEY_S):
                self.player_y += PLAYER_SPEED

        # Colisão com as bordas da tela 
        self.player_x = max(0, min(self.player_x, SCREEN_WIDTH - PLAYER_WIDTH))
        self.player_y = max(0, min(self.player_y, SCREEN_HEIGHT - PLAYER_HEIGHT))

        # Verifica todas as colisões
        self.check_all_collisions()

    def check_all_collisions(self):
        # Colisão com margens do rio
        # self.check_river_collision(self.player_x, self.player_y, "Jogador 1")
        # if self.is_multiplayer:
        #     self.check_river_collision(self.player2_x, self.player2_y, "Jogador 2")

        # Colisão com árvores para ambos os jogadores
        check_tree_collision(self.player_x, self.player_y, self.background.tree_manager.arvores, "Jogador 1")
        if self.is_multiplayer:
            check_tree_collision(self.player2_x, self.player2_y, self.background.tree_manager.arvores, "Jogador 2")

        
    
    def check_river_collision(self, x, y, player_name):
        """Verifica se o jogador está fora das margens do rio."""
        # Obtém as margens na posição Y do jogador
        margem_esq, margem_dir = self.background.obter_margens_rio(y)
        
        # Verifica se o jogador está fora do rio (considerando a largura do sprite)
        if (x < margem_esq) or (x + PLAYER_WIDTH > margem_dir):
            print(f"{player_name} colidiu com a margem do rio!")
            print(f"Posição: ({x}, {y})")

    def send_data(self):
        if self.is_multiplayer and self.game.network.connected:
            data = {
                'player': [self.player_x, self.player_y],
                'rio_centro': self.background.centro_rio_x,
                'seed': self.background.tree_manager.random_seed,
                'type': 'game_update'
            }
            self.game.network.send(data)

    def receive_data(self):
        if self.is_multiplayer and isinstance(self.game.network.data, dict):
            data = self.game.network.data
            try:
                self.player2_x, self.player2_y = data['player']
                
                if not self.is_host:
                    self.background.centro_rio_x = data['rio_centro']
                    self.background.target_centro_x = data['rio_centro']
                
                if 'seed' in data and data['seed'] != self.background.tree_manager.random_seed:
                    self.background.tree_manager.random_seed = data['seed']
                    random.seed(data['seed'])
                    self.background.tree_manager.reset_arvores()
                    
            except (KeyError, TypeError):
                print("Erro na sincronização dos dados")


    # Renderiza mapa, jogador e elementos do jogo
    def draw(self):
        # Limpa a tela
        pyxel.cls(COLOR_BG)
        self.background.draw()
        
        # Desenha o jogador local
        if self.is_multiplayer:
            if self.is_host:
                # Host: avião (48,0)
                pyxel.blt(self.player_x, self.player_y, 0, 48, 0, PLAYER_WIDTH, PLAYER_HEIGHT, colkey=0)

            else:
                # Cliente: helicóptero (0,16)
                pyxel.blt(self.player_x, self.player_y, 0, 0, 16, PLAYER_WIDTH, PLAYER_HEIGHT, colkey=0)
        else:
            # Singleplayer: avião padrão
            pyxel.blt(self.player_x, self.player_y, 0, 48, 0, PLAYER_WIDTH, PLAYER_HEIGHT, colkey=0)

        # Desenha o outro jogador (multiplayer)
        if self.is_multiplayer and self.game.network.connected:
            pyxel.text(10, 10, "Multiplayer - Conectado", COLOR_TEXT_HIGHLIGHT)
            if self.is_host:
                # Host vê cliente como helicóptero
                pyxel.blt(self.player2_x, self.player2_y, 0, 0, 16, PLAYER_WIDTH, PLAYER_HEIGHT, colkey=0)
            else:
                # Cliente vê host como avião
                pyxel.blt(self.player2_x, self.player2_y, 0, 48, 0, PLAYER_WIDTH, PLAYER_HEIGHT, colkey=0)
        elif self.is_multiplayer:
            pyxel.text(10, 10, "Multiplayer - Desconectado", COLOR_TEXT_HIGHLIGHT)
        
        # Debug: mostra posições claramente
        pyxel.text(10, 20, f"Host: {self.player_x},{self.player_y}", 7)
        pyxel.text(10, 30, f"Cliente: {self.player2_x},{self.player2_y}", 7)

        # Desenha o outro jogador
        if self.is_multiplayer:
            if self.game.network.connected:
                pyxel.text(10, 10, "Multiplayer - Conectado", 0)
                # Inverte a skin para o outro jogador
                if self.is_host:
                    # Host vê o cliente como helicóptero
                    pyxel.blt(self.player2_x, self.player2_y, 0, 0, 16, PLAYER_WIDTH, PLAYER_HEIGHT, colkey=0)
                else:
                    # Cliente vê o host como avião
                    pyxel.blt(self.player2_x, self.player2_y, 0, 48, 0, PLAYER_WIDTH, PLAYER_HEIGHT, colkey=0)
            else:
                pyxel.text(10, 10, "Multiplayer - Desconectado", 0)

        # Desenha hitbox das árvores (debug)
        for arvore in self.background.tree_manager.arvores:
            arv_left, arv_top, arv_right, arv_bottom = arvore.hitbox
            pyxel.rectb(arv_left, arv_top, arv_right - arv_left, arv_bottom - arv_top, 8)

from collections import deque
import pyxel, random

class Background:
    def __init__(self, is_host=False):  # Linha modificada
        self.is_host = is_host  # Nova linha
        # Configurações do rio
        self.velocidade_scroll = 1
        self.deslocamento = 0
        self.largura_rio = 45
        self.cor_borda = 15
        self.centro_rio_x = pyxel.width / 2
        self.target_centro_x = self.centro_rio_x
        self.curve_speed = 1.0
        self.centros_hist = deque([self.centro_rio_x] * pyxel.height, maxlen=pyxel.height)
        self.pontos_brancos = [(3, 2), (10, 5), (15, 8), (25, 3), (30, 7), (5, 14), (20, 12), (28, 16), (12, 20), (18, 18)]
        
        # Gerenciador de árvores
        self.tree_manager = TreeManager(self)  # Usa o TreeManager do entities.py

    def obter_margens_rio(self, screen_y):
        centro = self.centros_hist[screen_y]
        meia = self.largura_rio / 2
        return centro - meia, centro + meia

    def update(self):
        # Controle do rio (mantido)
        if pyxel.btnp(pyxel.KEY_1):
            self.target_centro_x = min(self.target_centro_x + 30, pyxel.width - self.largura_rio/2)
        if pyxel.btnp(pyxel.KEY_2):
            self.target_centro_x = max(self.target_centro_x - 30, self.largura_rio/2)

        # Animação suave do rio
        diff = self.target_centro_x - self.centro_rio_x
        if abs(diff) > self.curve_speed:
            self.centro_rio_x += self.curve_speed * (1 if diff > 0 else -1)
        else:
            self.centro_rio_x = self.target_centro_x

        self.centros_hist.appendleft(self.centro_rio_x)
        self.deslocamento += self.velocidade_scroll

        # Atualiza árvores via TreeManager
        self.tree_manager.update_arvores(self.velocidade_scroll)

    def draw(self):
        # Desenho do rio (mantido)
        pyxel.rect(0, 0, pyxel.width, pyxel.height, 9)
        for screen_y in range(pyxel.height):
            esq, dir = self.obter_margens_rio(screen_y)
            for i in range(4):
                pyxel.line(int(esq)-i, screen_y, int(esq), screen_y, self.cor_borda)
                pyxel.line(int(dir), screen_y, int(dir)+i, screen_y, self.cor_borda)
            pyxel.line(int(esq), screen_y, int(dir), screen_y, 12)
            for dx, dy in self.pontos_brancos:
                pattern_y = (screen_y - self.deslocamento + dy) % 24
                if pattern_y == dy:
                    x = esq + (dx % (dir - esq))
                    if esq < x < dir:
                        pyxel.pset(int(x), screen_y, 7)
        
        # Desenha árvores via TreeManager
        self.tree_manager.draw_arvores()