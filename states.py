### Modulo de estados do jogo. Contem:
### - Telas de menu e submenus
### - Estados de jogo para singleplayer/multiplayer
### - Transicoes entre telas

# Bibliotecas
from time import sleep
import pyxel            # Engine do jogo
from config import *    # Importa constantes e configuracoes do arquivo "config.py"
from entities import *  # Importa as classes de entidades do jogo (jogador, arvores, etc.)
from map_generator import Background
import music

# Classe para o Menu Principal do jogo
class MenuState:
    # Construtor
    # Prepara menu principal com opcoes basicas
    def __init__(self, game): # "game" eh passado no construtor da classe "Game" do "main.py", sendo a instancia do jogo
        self.game = game # Recebe a instancia do jogo
        self.selected = 0 # Recebe a posicao que o jogador vai selecionar ("Singleplayer" ou "Multiplayer"). Comeca com "Singleplayer"
        self.options = ["Singleplayer", "Multiplayer"] # Opcoes do menu principal
        music.play_menu_music() # Toca a musica dos menus
    
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
                self.game.change_state(GameState(self.game, is_multiplayer= False))

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
    # Método de inicialização da classe
    def __init__(self, game):
        self.game = game  # Referência para o objeto principal do jogo
        self.message = "Aguardando host iniciar o jogo..."  # Mensagem exibida ao usuário
        self.waiting = True  # Flag indicando que está aguardando

    # Método chamado a cada frame para atualizar o estado
    def update(self):
        d = self.game.network.data  # Obtém dados recebidos da rede

            
        # Verifica se recebeu um sinal de início de jogo do host
        if isinstance(d, dict) and d.get('type') == 'game_start':
            # Muda para o estado de jogo com os parâmetros recebidos
            self.game.change_state(GameState(
                self.game,
                is_multiplayer=True,
                is_host=False,
                initial_seed=d.get('seed'),
                initial_rio_centro=d.get('rio_centro'),
                initial_rio_largura=d.get('rio_largura')
            ))
            return

        # Se estiver conectado, envia um sinal de "heartbeat" para manter a conexão
        if self.game.network.connected and len(d) == 1:
            self.game.network.send({'type': 'heartbeat'})

        # Se pressionar ESC, cancela e volta ao menu
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self.game.network.stop()  # Encerra a conexão
            self.game.change_state(MenuState(self.game))  # Volta ao menu principal

    # Método para desenhar a tela
    def draw(self):
        # Limpa a tela com a cor de fundo
        pyxel.cls(COLOR_BG)
        
        # Exibe mensagens para o usuário
        pyxel.text(20, 50, self.message, COLOR_TEXT)  # Mensagem principal
        pyxel.text(20, 70, "Pressione ESC para cancelar", COLOR_TEXT)  # Instrução


# Classe que contem o submenu para 'Hostear' um jogo
class HostGameState:
    # Método de inicialização
    def __init__(self, game):
        self.game = game  # Referência para o objeto principal do jogo
        self.message = ""  # Mensagem de status
        self.message_timer = 0  # Temporizador para mensagens
        
        # Tenta iniciar o servidor host
        if self.game.network.start_host():
            # Se conseguir, obtém IP e porta
            self.ip = self.game.network.local_ip
            self.port = self.game.network.port
        else:
            # Se falhar, mostra mensagem de erro
            self.ip = "—"
            self.port = "—"
            self.message = "Erro ao iniciar host"
            self.message_timer = MESSAGE_DISPLAY_TIME  # Define tempo para mostrar mensagem

    # Método para atualizar o estado a cada frame
    def update(self):
        # Mantém a conexão ativa enviando heartbeats
        if self.game.network.connected:
            self.game.network.send({'type': 'heartbeat'})

        # Se pressionar ENTER, inicia o jogo
        if pyxel.btnp(pyxel.KEY_RETURN):
            # Cria o estado do jogo primeiro
            game_state = GameState(self.game, is_multiplayer=True, is_host=True)
            
            # Prepara dados iniciais para sincronização
            initial_data = {
                'type': 'game_start',
                'seed': game_state.background.tree_manager.random_seed,  # Semente aleatória
                'rio_centro': game_state.background.centro_rio_x,  # Posição do rio
                'rio_largura': game_state.background.largura_rio  # Largura do rio
            }
            # Envia dados para o cliente
            self.game.network.send(initial_data)
            
            sleep(0.1)

            # Muda para o estado de jogo
            self.game.change_state(game_state)

        # Se pressionar ESC, volta ao menu multiplayer
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self.game.network.stop()  # Encerra a conexão
            self.game.change_state(MultiplayerMenuState(self.game))

        # Atualiza temporizador da mensagem
        if self.message_timer > 0:
            self.message_timer -= 1
    
    # Método para desenhar a tela
    def draw(self):
        # Limpa a tela
        pyxel.cls(COLOR_BG)
        # Exibe informações do host
        pyxel.text(20, 20, "Hosting Game", COLOR_TEXT)  # Título
        pyxel.text(20, 40, f"IP: {self.ip}", COLOR_TEXT)  # Endereço IP
        pyxel.text(20, 60, f"Port: {self.port}", COLOR_TEXT)  # Porta

        # Exibe status da conexão
        if self.game.network.connected:
            pyxel.text(20, 80, "Cliente conectado", COLOR_SUCCESS)  # Conectado
        else:
            pyxel.text(20, 80, "Aguardando cliente...", COLOR_TEXT)  # Aguardando

        # Exibe instruções
        pyxel.text(10, 90, "Pressione ENTER para comecar o jogo", COLOR_TEXT_HIGHLIGHT)
        pyxel.text(10, 100, "Pressione ESC para voltar", COLOR_TEXT)


# Classe para o menu de pause do jogo
class PauseMenuState:
    # Método de inicialização
    def __init__(self, game):
        self.game = game
        self.selected = 0
        self.options = ["Continuar", "Menu Principal"]

    # Método para atualizar o estado a cada frame
    def update(self):
        # Só faz sentido em cima de um GameState
        if not isinstance(self.game.previous_state, GameState):
            return
        
        gs = self.game.previous_state
        if self.game.previous_state.is_multiplayer:    
            if gs.invincible_timer_j1 > 0:
                gs.invincible_timer_j1 -= 1
            if gs.invincible_timer_j2 > 0:
                gs.invincible_timer_j2 -= 1

            # 1) mantém o scroll do rio
            gs.background.update()

            # 2) rede continua ativa em multiplayer
            if gs.is_multiplayer:
                gs.send_data()
                gs.receive_data()

            # 3) tiros continuam voando
            gs.update_shots()

            # 4) barcos continuam navegando (apenas UMA chamada)
            gs.boat_manager.update()

            # 5) colisões continuam sendo testadas
            gs.check_all_collisions()

            # 6) explosões continuam animando
            for exp in gs.explosions:
                exp.update()
            gs.explosions = [e for e in gs.explosions if not e.is_dead()]

            for exp in gs.remote_explosions:
                exp.update()
            gs.remote_explosions = [e for e in gs.remote_explosions if not e.is_dead()]

        # 7) navegação do menu de pause
        if pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_S):
            self.selected = (self.selected + 1) % len(self.options)
        elif pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W):
            self.selected = (self.selected - 1) % len(self.options)

        # 8) confirmação de opção
        if pyxel.btnp(pyxel.KEY_RETURN):
            if self.selected == 0:  # Continuar
                self.game.change_state(gs)
            else:  # Menu Principal
                if gs.is_multiplayer:
                    self.game.network.stop()
                self.game.change_state(MenuState(self.game))

        # atalho Esc = Continuar
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self.game.change_state(gs)

    # Método para desenhar o menu
    def draw(self):
        pyxel.cls(COLOR_BG)  # Limpa a tela
        pyxel.text(50, 40, "Jogo Pausado", COLOR_TEXT)  # Título

        
        # Desenha as opções do menu
        for i, opt in enumerate(self.options):
            # Define a cor (destaque para opção selecionada)
            color = COLOR_TEXT if i != self.selected else COLOR_TEXT_HIGHLIGHT
            pyxel.text(50, 60 + (i*20), opt, color)  # Desenha cada opção

# Classe principal que gerencia o estado do jogo (singleplayer/multiplayer)
class GameState:
    # Método de inicialização
    def __init__(self, game, is_multiplayer=False, is_host=False, initial_seed=None, initial_rio_centro=None , initial_rio_largura=None):
        self.game = game  # Referência para o objeto principal do jogo
        self.is_multiplayer = is_multiplayer  # Flag para modo multiplayer
        self.is_host = is_host  # Flag para identificar se é o host
        
        # Toca a musica do jogo
        music.play_game_music()

        # Fim de jogo
        self.death_delay = False        # Verifica se estah aguardando para entrar no game over 
        self.death_delay_timer = 0      # quantos frames faltam para o delay de morte acabar
        self.game_over = False          # flag de fim de jogo
        self.game_over_timer = 0        # temporizador em frames

        # Fila de sons que a instancia vai enviar ao outro (cliente para servidor ou servidor para cliente)
        self.pending_sounds = []  
        
        # Posicionamento inicial dos jogadores (host vs cliente)
        if is_host:
            # Host controla jogador 1 (esquerda)
            self.player_x, self.player_y = 55, 130  
            # Jogador 2 (cliente) começa à direita
            self.player2_x, self.player2_y = 90, 130  
        else:
            # Cliente controla jogador 2 (direita)
            self.player_x, self.player_y = 90, 130
            # Jogador 1 (host) começa à esquerda
            self.player2_x, self.player2_y = 55, 130  

        # Inicializa o cenário de fundo
        self.background = Background(is_host=is_host , is_multiplayer=is_multiplayer) 

        # HUD
        self.life_player1 = MAX_LIVES  # Vida do jogador 1 (host)
        self.fuel_player1 = MAX_FUEL # Gasolina do jogador 1 (Host)
        self.life_player2 = MAX_LIVES  # Vida do jogador 2 (cliente)
        self.fuel_player2 = MAX_FUEL # Gasolina do jogador 2 (Cliente)
        self.invincible_timer_j1 = 0  # Temporizador de invencibilidade do jogador 1
        self.invincible_timer_j2 = 0  # Temporizador de invencibilidade do jogador 2
        self.INVINCIBILITY_DURATION = 90  # Duração em frames (1.5s a 60FPS)
        self.score_player1 = 0  # Pontuação do jogador 1
        self.score_player2 = 0  # Pontuação do jogador 2

        # Sincronização inicial do jogo (apenas multiplayer)
        if initial_seed:
            # Sincroniza a seed aleatória para árvores
            self.background.tree_manager.random_seed = initial_seed
            random.seed(initial_seed)
            self.background.tree_manager.reset_arvores()
        
        if initial_rio_centro and not is_host:
            # Sincroniza a posição do rio para clientes
            self.background.centro_rio_x = initial_rio_centro
            self.background.target_centro_x = initial_rio_centro
        
        if initial_rio_largura is not None and not is_host:
            self.background.largura_rio     = initial_rio_largura
            self.background.target_largura  = initial_rio_largura

        if is_multiplayer and not is_host:  # Apenas clientes multiplayer não atualizam
            self.background.tree_manager.update_arvores = lambda _: None  # Desabilita atualização de árvores para clientes

        # lista de tiros locais e da outra tela
        self.shots = []          # tiros deste jogador
        self.remote_shots = []   # tiros vindos pela rede

        self.explosions = []   # lista de Explosion ativos
        self.remote_explosions = []  # explosões vindas pela rede

        self.boat_manager = BoatManager(self.background)    # barcos locais (host gera)
        self.remote_boats = []                             # barcos sincronizados via rede



    def _collide_player(self, hitbox, px, py):
        left, top, right, bottom = hitbox
        return (px+PLAYER_WIDTH>left and px<right and
                py+PLAYER_HEIGHT>top and py<bottom)
    
    # Método para atualizar o estado do jogo a cada frame
    def update(self):
        # Apenas atualiza a lógica do jogo se não estiver em pause
        if not isinstance(self.game.current_state, PauseMenuState):
            self.background.update()  # ← Movido para fora da verificação de pause

        # Comunicação em rede (apenas multiplayer)
        if self.is_multiplayer:
            self.send_data()  # Envia dados do jogador local
            self.receive_data()  # Recebe dados do outro jogador

        # Se estiver em Game Over, apenas decrementa o timer
        if self.game_over:
            self.game_over_timer -= 1
            if self.game_over_timer <= 0:
                # volta ao menu principal
                self.game.network.stop()  # Encerra a conexao
                self.game.change_state(MenuState(self.game))
            return
        
        # Se estiver no “delay de morte”, decrementa o seu timer,
        # mas continuar rodando o jogo normalmente ateh acabar o timer:
        if self.death_delay:
            self.death_delay_timer -= 1
            if self.death_delay_timer <= 0:
                # passado o delay, o Game Over eh ativado
                self.death_delay      = False
                self.game_over        = True
                self.game_over_timer  = 5 * FPS   # 5 segundos de tela preta
                pyxel.play(0, 1) # Som de fim de jogo
                

        # Lógica de pausa
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self.game.previous_state = self  # Salva estado atual
            self.game.change_state(PauseMenuState(self.game))  # Vai para menu de pause
            return  # Sai da atualização

        # Controles do jogador (WASD)
        if not self.is_multiplayer or (self.is_multiplayer):
            if pyxel.btn(pyxel.KEY_A):
                self.player_x -= PLAYER_SPEED  # Move para esquerda
            if pyxel.btn(pyxel.KEY_D):
                self.player_x += PLAYER_SPEED  # Move para direita
            if pyxel.btn(pyxel.KEY_W):
                self.player_y -= PLAYER_SPEED  # Move para cima
            if pyxel.btn(pyxel.KEY_S):
                self.player_y += PLAYER_SPEED  # Move para baixo
            # Disparo: cria um tiro quando apertar SPACE
            if pyxel.btnp(pyxel.KEY_SPACE) and (not self.death_delay and not self.game_over):
                if (self.is_host or not self.is_multiplayer) and self.life_player1 > 0:
                    # inicia no centro horizontal do avião, um pouco acima dele
                    shot_x = self.player_x + PLAYER_WIDTH // 2 - 1
                    shot_y = self.player_y
                    self.shots.append(Shot(shot_x, shot_y))
                    pyxel.play(0, 0) # Som de tiro
                    self.pending_sounds.append((0, 0)) # Envia para Cliente/Servidor o som de tiro
                elif not self.is_host and self.life_player2 > 0:
                    # inicia no centro horizontal do avião, um pouco acima dele
                    shot_x = self.player_x + PLAYER_WIDTH // 2 - 1
                    shot_y = self.player_y
                    self.shots.append(Shot(shot_x, shot_y))
                    pyxel.play(0, 0) # Som de tiro
                    self.pending_sounds.append((0, 0)) # Envia para Cliente/Servidor o som de tiro


        # Limites da tela
        self.player_x = max(0, min(self.player_x, SCREEN_WIDTH - PLAYER_WIDTH))

        game_area_height = SCREEN_HEIGHT - HUD_HEIGHT
        self.player_y = max(0, min(self.player_y, game_area_height - PLAYER_HEIGHT))

        # Gasolina:
        consumption_per_frame = FUEL_CONSUMPTION_RATE / FPS # Calcula qtd de gasolina para consumir neste frame (unidades por frame)
        # Atualizacao para o modo Singleplayer da gasolina:
        if not self.is_multiplayer:
            self.fuel_player1 = max(0, self.fuel_player1 - consumption_per_frame) # Decrementa, garantindo que nunca fique negativo
        if self.is_host:
            self.fuel_player1 = max(0, self.fuel_player1 - consumption_per_frame) # Decrementa, garantindo que nunca fique negativo
        else:
            self.fuel_player2 = max(0, self.fuel_player2 - consumption_per_frame) # Decrementa, garantindo que nunca fique negativo

        # Atualiza temporizadores de invencibilidade
        if self.invincible_timer_j1 > 0:
            self.invincible_timer_j1 -= 1 # Invencibilidade do jogador 1
        if self.invincible_timer_j2 > 0:
            self.invincible_timer_j2 -= 1 # Invencibilidade do jogador 2

        self.update_shots()
        
        # local
        for exp in self.explosions:
            exp.update()
        self.explosions = [e for e in self.explosions if not e.is_dead()]

        # remota
        for exp in self.remote_explosions:
            exp.update()
        self.remote_explosions = [
            e for e in self.remote_explosions if not e.is_dead()
        ]

        # atualiza barcos (host gera; ambos movem)
        self.boat_manager.update()
        # recebe remote_boats já populada em receive_data
        for b in self.remote_boats:
            b.update()

        
        # Verificação de colisões
        self.check_all_collisions()

    # Método para verificar colisões
    def check_all_collisions(self):
        if self.is_multiplayer:
            # Lógica do host para jogador 1
            if self.is_host and self.invincible_timer_j1 <= 0:
                colisoes = check_tree_collision( # Verifica colisão com árvores
                    self.player_x, self.player_y, # Posição do jogador 1
                    self.background.tree_manager.arvores, # Lista de árvores
                    "Jogador 1" # Nome do jogador (para debug)
                )
                if colisoes > 0:
                    self.life_player1 = max(0, self.life_player1 - 1)  # Perde vida 
                    self.invincible_timer_j1 = self.INVINCIBILITY_DURATION  # Ativa invencibilidade
                    if not self.death_delay and not self.game_over and self.life_player1 > 0:
                        pyxel.play(1, 2) # Som de colisao
                        self.pending_sounds.append((1, 2)) # Envia para Cliente o som

            # Lógica do cliente para jogador 2
            elif not self.is_host and self.invincible_timer_j2 <= 0:
                colisoes = check_tree_collision(
                    self.player_x, self.player_y,
                    self.background.tree_manager.arvores,
                    "Jogador 2"
                )
                if colisoes > 0:
                    self.life_player2 = max(0, self.life_player2 - 1)  # Perde vida
                    self.invincible_timer_j2 = self.INVINCIBILITY_DURATION  # Ativa invencibilidade
                    if not self.death_delay and not self.game_over and self.life_player2 > 0:
                        pyxel.play(1, 2) # Som de colisao
                        self.pending_sounds.append((1, 2)) # Envia para Cliente o som
        else:
            # Lógica singleplayer
            if self.invincible_timer_j1 <= 0:
                colisoes = check_tree_collision(
                    self.player_x, self.player_y,
                    self.background.tree_manager.arvores,
                    "Jogador 1"
                )
                if colisoes > 0:
                    self.life_player1 = max(0, self.life_player1 - 1)  # Perde vida
                    self.invincible_timer_j1 = self.INVINCIBILITY_DURATION  # Ativa invencibilidade
                    if self.life_player1 > 0:
                        pyxel.play(1, 2) # Som de colisao
        
        ## ————— Colisão Tiro × Árvore (host destrói; ambos removem tiro no primeiro hit) —————
        for shot_list in (self.shots, self.remote_shots):
            for shot in shot_list.copy():
                hit = False

                for tree in self.background.tree_manager.arvores:
                    # ignora árvores já destruídas
                    if not tree.visible:
                        continue

                    # calcula hitboxes
                    left, top, right, bottom = tree.hitbox
                    s_left = shot.x
                    s_right = shot.x + shot.width
                    s_top = shot.y
                    s_bottom = shot.y + shot.height
                    
                    if (s_right > left and s_left < right and
                        s_bottom > top and s_top < bottom):
                        # host marca a árvore como destruída
                        if (self.is_host or not self.is_multiplayer):
                            tree.visible = False

                            # Host destruiu uma arvore, aumenta a pontuacao
                            self.score_player1 += 2
                            # cria explosão no centro da árvore
                            cx = (left + right) // 2 - 16 // 2
                            cy = (top  + bottom) // 2 - 16 // 2
                            self.explosions.append(
                                Explosion(cx, cy, 16, 16, 16, 16, duration=8)
                            )

                            pyxel.play(2, 3) # Som de colisao de tiro
                            if self.is_multiplayer:
                                self.pending_sounds.append((2, 3)) # Envia para Cliente o som
                        else:
                            # Cliente destruiu uma arvore, aumenta a pontuacao
                            self.score_player2 += 2
                            pyxel.play(2, 3) # Som de colisao
                            self.pending_sounds.append((2, 3)) # Envia para Host o som
                        # qualquer um remove o tiro no primeiro contato
                        shot_list.remove(shot)
                        hit = True
                        break

                if hit:
                    # já tratou esse tiro—vai para o próximo
                    continue

                # se não colidiu e saiu da tela, também remove
                if shot.is_off_screen():
                    shot_list.remove(shot)

        ## ————— Colisão Tiro × Barco —————
        # percorre cada lista de tiros
        for shot_list in (self.shots, self.remote_shots):
            for shot in shot_list.copy():
                for boat in (self.boat_manager.boats if (self.is_host or not self.is_multiplayer) else self.remote_boats):
                    # só colisão em barcos visíveis
                    if not boat.visible:
                        continue
                    # hitbox do barco e do tiro
                    b_left, b_top, b_right, b_bottom = boat.hitbox
                    s_left = shot.x
                    s_right = shot.x + shot.width
                    s_top = shot.y
                    s_bottom = shot.y + shot.height

                    if (s_right > b_left and s_left < b_right and
                        s_bottom > b_top   and s_top < b_bottom):
                        # host é fonte da verdade: destrói o barco
                        if (self.is_host or not self.is_multiplayer):
                            boat.visible = False

                            # Host destruiu um barco, aumenta a pontuacao
                            self.score_player1 += 4
                            # spawn de explosão no centro do barco
                            cx = (b_left + b_right)//2 - 8   # metade de 16px
                            cy = (b_top  + b_bottom)//2 - 8
                            self.explosions.append(
                                Explosion(cx, cy, 16, 16, 16, 16, duration=8)
                            )

                            pyxel.play(2, 4) # Som de colisao de tiro
                            if self.is_multiplayer:
                                self.pending_sounds.append((2, 4)) # Envia para Cliente o som
                        else:
                            # Cliente destruiu um barco, aumenta a pontuacao
                            self.score_player2 += 4
                            pyxel.play(2, 4) # Som de colisao de tiro
                            self.pending_sounds.append((2, 4)) # Envia para Cliente o som
                        # em qualquer caso, remove o tiro no primeiro hit
                        shot_list.remove(shot)
                        break

        ## ————— Colisão Jogador × Barco —————
        # verifica invencibilidade e colisão para cada jogador
        # Jogador 1 (host)  
        if (self.is_host or not self.is_multiplayer) and self.invincible_timer_j1 <= 0:
            for boat in self.boat_manager.boats:
                if boat.visible:
                    left, top, right, bottom = boat.hitbox
                    j_left = self.player_x
                    j_right = self.player_x + PLAYER_WIDTH
                    j_top = self.player_y
                    j_bottom = self.player_y + PLAYER_HEIGHT
                    if (j_right > left and j_left < right and
                        j_bottom > top   and j_top < bottom):
                        # colisão: perde vida e fica invencível
                        self.life_player1 = max(0, self.life_player1 - 1)
                        self.invincible_timer_j1 = self.INVINCIBILITY_DURATION
                        if not self.death_delay and not self.game_over and self.life_player1 > 0:
                            pyxel.play(1, 2) # Som de colisao
                            if self.is_multiplayer:
                                self.pending_sounds.append((1, 2)) # Envia para Cliente o som
                            break
        # Jogador 2 (cliente)  
        if not self.is_host and self.invincible_timer_j2 <= 0:
            for boat in self.remote_boats:
                if boat.visible:
                    left, top, right, bottom = boat.hitbox
                    j_left = self.player_x
                    j_right = self.player_x + PLAYER_WIDTH
                    j_top = self.player_y
                    j_bottom = self.player_y + PLAYER_HEIGHT
                    if (j_right > left and j_left < right and
                        j_bottom > top   and j_top < bottom):
                        self.life_player2 = max(0, self.life_player2 - 1)
                        self.invincible_timer_j2 = self.INVINCIBILITY_DURATION
                        if not self.death_delay and not self.game_over and self.life_player2 > 0:
                            pyxel.play(1, 2) # Som de colisao
                            self.pending_sounds.append((1, 2)) # Envia para Cliente o som
                        break
        
        # Jogador 1 morreu?
        if self.life_player1 == 0 and not getattr(self, "_exploded_j1", False) and (self.is_host or not self.is_multiplayer):
            # marca que já acionou explosão
            self._exploded_j1 = True
            # centro do avião 1

            cx = self.player_x + PLAYER_WIDTH//2 - 8
            cy = self.player_y + PLAYER_HEIGHT//2 - 8
            self.explosions.append(
                Explosion(cx, cy, 16, 16, 16, 16, duration=30)
            )

            pyxel.play(1, 2) # Som de explosao
            self.pending_sounds.append((1, 2)) # Envia para Cliente o som

        # Jogador 2 morreu?
        if self.is_multiplayer and self.life_player2 == 0 and not getattr(self, "_exploded_j2", False):
            self._exploded_j2 = True
            # posição do avião 2 depende se host ou client
            px, py = (self.player2_x, self.player2_y) if self.is_host else (self.player_x, self.player_y)
            cx = px + PLAYER_WIDTH//2 - 8
            cy = py + PLAYER_HEIGHT//2 - 8
            self.explosions.append(
                Explosion(cx, cy, 16, 16, 16, 16, duration=30)
            )

            pyxel.play(1, 2) # Som de explosao
            self.pending_sounds.append((1, 2)) # Envia para Cliente o som

        # Fim de jogo:
        # Condição SINGLEPLAYER
        if not self.is_multiplayer and self.life_player1 == 0 and not self.death_delay:
            self.death_delay = True
            self.death_delay_timer = 2 * FPS   # 2 segundos de delay
            music.stop_music() # Para a musica

        # Condição MULTIPLAYER
        elif self.is_multiplayer and self.life_player1 == 0 and (not self.game.network.connected or self.life_player2 == 0) and not self.death_delay:
            self.death_delay = True
            self.death_delay_timer = 2 * FPS    # 2 segundos de delay
            music.stop_music() # Para a musica

       

    def update_shots(self):
        """Atualiza posição e descarta tiros fora da tela — usado tanto em play quanto em pause."""
        # locais
        for shot in self.shots:
            shot.update()
        self.shots = [s for s in self.shots if not s.is_off_screen()]

        # remotos
        for shot in self.remote_shots:
            shot.update()
        self.remote_shots = [s for s in self.remote_shots if not s.is_off_screen()]
        
    # Método para enviar dados pela rede
    def send_data(self):
        if self.is_multiplayer and self.game.network.connected:
            if self.is_host:
                data = {
                    'player': [self.player_x, self.player_y],  # Posição atual
                    'rio_centro': self.background.centro_rio_x,  # Posição do rio
                    'rio_largura': self.background.largura_rio,       # ← NOVO
                    'seed': self.background.tree_manager.random_seed,  # Seed aleatória
                    'invincible': self.invincible_timer_j1 if self.is_host else self.invincible_timer_j2,  # Timer de invencibilidade
                    'type': 'game_update', # Tipo de mensagem
                    'arvores': self.background.tree_manager.get_tree_states() , # Adicione esta linha
                    'shots': [shot.to_dict() for shot in self.shots],
                    'explosions': [exp.to_dict() for exp in self.explosions],
                    'boats': self.boat_manager.get_states(),
                    'player_type': 'host',
                    'fuel': self.fuel_player1,
                    'lives': self.life_player1,
                    "sounds": self.pending_sounds,
                }
            else:
                data = {
                    'player': [self.player_x, self.player_y],  # Posição atual
                    'rio_centro': self.background.centro_rio_x,  # Posição do rio
                    'rio_largura': self.background.largura_rio,       # ← NOVO
                    'seed': self.background.tree_manager.random_seed,  # Seed aleatória
                    'invincible': self.invincible_timer_j1 if self.is_host else self.invincible_timer_j2,  # Timer de invencibilidade
                    'type': 'game_update', # Tipo de mensagem
                    'arvores': self.background.tree_manager.get_tree_states() , # Adicione esta linha
                    'shots': [shot.to_dict() for shot in self.shots],
                    'explosions': [exp.to_dict() for exp in self.explosions],
                    'boats': self.boat_manager.get_states(),
                    'player_type': 'client',
                    'fuel': self.fuel_player2,
                    'lives': self.life_player2,
                    "sounds": self.pending_sounds,
                }

            self.pending_sounds = []  # limpa a fila de sons
                                
            self.game.network.send(data)  # Envia os dados

    # Método para receber dados da rede
    def receive_data(self):
        # Define a função receive_data como método da classe (self é a referência ao objeto)
        
        if self.is_multiplayer and isinstance(self.game.network.data, dict):
            # Verifica se o jogo está no modo multiplayer E se os dados recebidos da rede são um dicionário
            
            data = self.game.network.data
            # Armazena os dados recebidos da rede na variável local 'data' para facilitar acesso
            if (len(data) > 1): # ignora heartbeat
                try:
                    # Inicia um bloco try para capturar possíveis erros no processamento dos dados
                    
                    # Atualiza posição do outro jogador
                    self.player2_x, self.player2_y = data['player']
                    # Extrai as coordenadas x e y do outro jogador do dicionário de dados
                    ## tanto host quanto cliente atualizam os remote_shots
                    if 'shots' in data:
                        self.remote_shots = [Shot.from_dict(d) for d in data['shots']]

                    if 'explosions' in data:
                            # reconstrói explosões que vieram do outro lado
                            self.remote_explosions = [
                                Explosion.from_dict(d) for d in data['explosions']
                            ]

                    # Atualiza barcos remotos (apenas cliente recebe)
                    if 'boats' in data and not self.is_host:
                        # cliente reconstrói lista de barcos
                        self.remote_boats = [Boat.from_dict(d) for d in data['boats']]

                
                    # Sincroniza temporizador de invencibilidade
                    if self.is_host:   
                        # Pega gasolina e vida se o host recebe um pacote do cliente
                        if data.get('player_type', -1) == 'client':
                            self.fuel_player2 = data.get('fuel', self.fuel_player2)
                            self.life_player2 = data.get('lives', self.life_player2)
                            # Toca os sons recebidos pelo cliente (se tiver)
                            for channel, sound_id in data.get("sounds", []): 
                                pyxel.play(channel, sound_id)
                        
                        # Verifica se esta instância é o host (jogador 1)
                        self.invincible_timer_j2 = data.get('invincible', 0)
                        # Host recebe o timer de invencibilidade do cliente (jogador 2)
                        # Usa .get() para evitar KeyError, retornando 0 se 'invincible' não existir
                    
                    else:
                        # Pega gasolina e vida se o cliente recebe um pacote do host
                        if data.get('player_type', -1) == 'host':
                            self.fuel_player1 = data.get('fuel', self.fuel_player1)
                            self.life_player1 = data.get('lives', self.life_player1)
                            # Toca os sons recebidos pelo host (se tiver)
                            for channel, sound_id in data.get("sounds", []): 
                                pyxel.play(channel, sound_id)

                        # Caso contrário (se for o cliente)
                        self.invincible_timer_j1 = data.get('invincible', 0)
                        # Cliente recebe o timer de invencibilidade do host (jogador 1)
                        
                    # Clientes sincronizam posição do rio
                    if not self.is_host:
                        # Verifica se NÃO é o host (ou seja, é o cliente)
                        self.background.centro_rio_x = data['rio_centro']
                        # Atualiza a posição central atual do rio no background
                        self.background.target_centro_x = data['rio_centro']
                        # Atualiza também a posição alvo (target) do rio para sincronizar a animação
                    
                    if not self.is_host and 'rio_largura' in data:
                        self.background.largura_rio    = data['rio_largura']
                        self.background.target_largura = data['rio_largura']
                        
                    # Sincroniza seed aleatória se necessário
                    if 'seed' in data and data['seed'] != self.background.tree_manager.random_seed:
                        # Verifica se existe uma seed nos dados E se é diferente da seed atual
                        self.background.tree_manager.random_seed = data['seed']
                        # Atualiza a seed aleatória no gerenciador de árvores
                        random.seed(data['seed'])
                        # Define a seed global do módulo random para manter consistência
                        self.background.tree_manager.reset_arvores()
                        # Reinicia as árvores com a nova seed para sincronizar a geração aleatória
                    # Sincroniza árvores
                    if 'arvores' in data and not self.is_host:
                        self.background.tree_manager.set_tree_states(data['arvores'])
                except (KeyError, TypeError):
                    # Captura exceções caso haja erro ao acessar chaves do dicionário ou tipos incorretos
                    print("Erro na sincronização dos dados")
                    # Imprime mensagem de erro (poderia ser tratado de forma mais robusta em produção)

    # Método para desenhar o jogo
    def draw(self):
        # Se o jogo acabou
        if self.game_over:
            # pinta tudo de preto
            pyxel.cls(0)
            # escreve no centro
            txt = "FIM DE JOGO"
            w = len(txt) * 4   # aprox largura em px de cada caractere
            x = (SCREEN_WIDTH  - w) // 2
            y = (SCREEN_HEIGHT - 8) // 2  # 8px de altura de texto
            pyxel.text(x, y, txt, 7)
            return

        pyxel.cls(COLOR_BG)                                   # Limpa a tela com a cor de fundo definida
        
        # Separador da HUD (linha que divide o jogo da interface)
        sep_y = SCREEN_HEIGHT - HUD_HEIGHT # Posicao em 'Y' = Separador eh igual a altura da tela menos a altura da HUD
        pyxel.clip(0, 0, SCREEN_WIDTH, sep_y) # Define o clip para a área de jogo

        self.background.draw()                                # Desenha o cenário de fundo

        # desenha barcos locais e remotos
        self.boat_manager.draw()
        for b in self.remote_boats:
            b.draw()

        # desenha tiros locais
        for shot in self.shots:
            shot.draw()
        # desenha tiros vindos pela rede
        for shot in self.remote_shots:
            shot.draw()

        # desenha explosões locais
        for exp in self.explosions:
            exp.draw()
        # desenha explosões vindas pela rede
        for exp in self.remote_explosions:
            exp.draw()

        # Lógica de piscar durante invencibilidade
        should_draw_j1 = (self.invincible_timer_j1 // 5) % 2 == 0 if self.invincible_timer_j1 > 0 else True  # Define se o jogador 1 deve piscar (quando invencível)
        should_draw_j2 = (self.invincible_timer_j2 // 5) % 2 == 0 if self.invincible_timer_j2 > 0 else True  # Define se o jogador 2 deve piscar (quando invencível)

        if self.is_multiplayer:
            if self.life_player1 > 0:
                # Renderização do jogador 1
                if should_draw_j1:             # Verifica se é multiplayer E se deve desenhar o jogador 1
                    if self.is_host:                                  # Se for o host (jogador 1)
                        pyxel.blt(self.player_x, self.player_y, 0, 32, 0, PLAYER_WIDTH, PLAYER_HEIGHT, colkey=0)  # Desenha o avião (host)
                    else:                                              # Se for o cliente
                        pyxel.blt(self.player2_x, self.player2_y, 0, 32, 0, PLAYER_WIDTH, PLAYER_HEIGHT, colkey=0)  # Desenha o avião do host na posição recebida
                
            if self.game.network.connected and self.life_player2 > 0:
                # Renderização do jogador 2 (helicóptero)
                if should_draw_j2:
                    # Animação da hélice (alterna entre dois frames a cada 5 frames)
                    helicopter_frame = (pyxel.frame_count // 5) % 2
                    
                    # Coordenadas dos frames na imagem (48,0) e (0,16)
                    u = 48 if helicopter_frame == 0 else 0
                    v = 0 if helicopter_frame == 0 else 16

                    if self.is_host:
                        pyxel.blt(
                            self.player2_x, self.player2_y,
                            0,            # Banco de imagens
                            u, v,         # Coordenadas do frame
                            PLAYER_WIDTH, PLAYER_HEIGHT,
                            colkey=0
                        )
                    else:
                        pyxel.blt(
                            self.player_x, self.player_y,
                            0,            # Banco de imagens
                            u, v,         # Coordenadas do frame
                            PLAYER_WIDTH, PLAYER_HEIGHT,
                            colkey=0
                        )

            
            # Status da conexão
            if self.game.network.connected:                        # Verifica se há conexão de rede
                pyxel.text(10, 10, "Multiplayer - Conectado", 0)   # Mostra status "Conectado"
            else:                                                  # Se não estiver conectado
                pyxel.text(10, 10, "Multiplayer - Desconectado", 0)  # Mostra status "Desconectado"

        # Modo singleplayer
        else:
            # Se não for multiplayer E deve desenhar o jogador e jogador tem vida maior que zero
            if should_draw_j1 and self.life_player1 > 0:         
                pyxel.blt(self.player_x, self.player_y, 0, 32, 0, PLAYER_WIDTH, PLAYER_HEIGHT, colkey=0)  # Desenha o jogador único

        # Desativa o clip (volta ao desenho em tela cheia)
        pyxel.clip()
        pyxel.line(0, sep_y, SCREEN_WIDTH, sep_y, COLOR_HUD_LINE) # Desenha a linha horizontal da hud
        if self.is_multiplayer:
           # Logica para as duas barras de combustivel (jogador 1 e 2):

            # Calcula largura das barras: (largura_total - (3*padding)) / 2
            # De forma que caiba duas barras + 3 *paddings (de espaco entre elas):
            bar_w = (SCREEN_WIDTH - 3 * PADDING) // 2

            # Posicoes X das duas barras:
            x1 = PADDING # Barra esquerda
            x2 = (PADDING * 2) + bar_w # Barra direita ((padding * 2) + largura da primeira barra)

            # Posicao Y inicial das barras (2px abaixo do separador da HUD)
            y_bar = sep_y + 2
            # Coracoes (vidas) em baixo das barras de gasolina
            y_heart = y_bar + FUEL_BAR_H + 2 # Posicao Y dos coracoes
            # Centraliza coracao abaixo da barra
            total_heart_w = MAX_LIVES * HEART_SIZE + (MAX_LIVES - 1) * HEART_GAP # Largura total dos coracoes
            
            # Desenha HUD do jogador 1 se ele estiver vivo
            if self.life_player1 > 0:
                # Barra de combustivel - Jogador 1
                # desenha barra do jogador 1
                pyxel.rectb(x1, y_bar, bar_w, FUEL_BAR_H, COLOR_FUEL_BORDER) # Desenha borda da barra
                filled1 = int((self.fuel_player1 / MAX_FUEL) * (bar_w - 2)) # Calcula o nivel de preenchimento da barra
                pyxel.rect(x1 + 1, y_bar + 1, filled1, FUEL_BAR_H - 2, COLOR_FUEL) # Preenche proporcionalmente a barra de gasolina

                # Coracao - Jogador 1
                start_x1 = x1 + (bar_w - total_heart_w) // 2 # Calcula posicao inicial para centralizar

                # Desenha cada coracao (cheio ou vazio)
                for i in range(MAX_LIVES):
                    cx = start_x1 + i * (HEART_SIZE + HEART_GAP) # Posicao X do coracao atual

                    if self.life_player1 > i:
                        pyxel.blt(cx, y_heart, 0, 0, 32, HEART_SIZE, HEART_SIZE, colkey=0)  # Desenha coracao cheio
                    else:
                        pyxel.blt(cx, y_heart, 0, 8, 32, HEART_SIZE, HEART_SIZE, colkey=0)  # Desenha coracao vazio
                
                # Pontuação jogador 1
                pyxel.text(
                    x1,                     # x centralizado
                    y_bar + FUEL_BAR_H + HEART_SIZE + 4,   # 1px abaixo dos corações
                    f"Score P1: {self.score_player1}",
                    COLOR_TEXT
                )

            # Desenha HUD do jogador 2 se ele estiver vivo e o jogo conectado
            if self.game.network.connected and self.life_player2 > 0:

                # Barra de combustivel - Jogador 2 
                pyxel.rectb(x2, y_bar, bar_w, FUEL_BAR_H, COLOR_FUEL_BORDER) # Desenha borda da barra
                filled2 = int((self.fuel_player2 / MAX_FUEL) * (bar_w - 2)) # Calcula o nivel de preenchimento da barra
                pyxel.rect(x2 + 1, y_bar + 1, filled2, FUEL_BAR_H - 2, COLOR_FUEL) # Preenche proporcionalmente a barra de gasolina


                # Coracao - Jogador 2 (ja foi calculado a largura total dos coracoes)
                start_x2 = x2 + (bar_w - total_heart_w) // 2 # Calcula posicao inicial para centralizar

                # Desenha cada coracao (cheio ou vazio)
                for i in range(MAX_LIVES):
                    cx = start_x2 + i * (HEART_SIZE + HEART_GAP) # Posicao X do coracao atual

                    if self.life_player2 > i:
                        pyxel.blt(cx, y_heart, 0, 0, 32, HEART_SIZE, HEART_SIZE, colkey=0)  # Desenha coracao cheio
                    else:
                        pyxel.blt(cx, y_heart, 0, 8, 32, HEART_SIZE, HEART_SIZE, colkey=0)  # Desenha coracao vazio

                # Pontuação jogador 2
                pyxel.text(
                    x2,                     # x centralizado
                    y_bar + FUEL_BAR_H + HEART_SIZE + 4,   # 1px abaixo dos corações
                    f"Score P2: {self.score_player2}",
                    COLOR_TEXT
                )

        # HUD para modo singleplayer
        else:
            # HUD centralizada
            cx = (SCREEN_WIDTH - FUEL_BAR_W) // 2 # Centraliza caoracao em 'X' na horizontal
            y_bar = sep_y + 2 # Posicao Y inicial das barras de gasolina (2px abaixo do separador da HUD)

            # Desenha HUD do jogador 1 se ele estiver vivo
            if self.life_player1 > 0:
                # Desenha uma unica barra de combustivel:
                pyxel.rectb(cx, y_bar, FUEL_BAR_W, FUEL_BAR_H, COLOR_FUEL_BORDER) # Desenha borda da barra
                filled = int((self.fuel_player1 / MAX_FUEL) * (FUEL_BAR_W - 2)) # Calcula o nivel de preenchimento da barra
                pyxel.rect(cx+1, y_bar+1, filled, FUEL_BAR_H-2, COLOR_FUEL) # Preenche proporcionalmente a barra de gasolina

                # Coracoes
                y_heart = y_bar + FUEL_BAR_H + 2 # Posicao Y dos coracoes (em baixo da barra de gasolina)
                start_x = (SCREEN_WIDTH - (MAX_LIVES*HEART_SIZE + (MAX_LIVES-1)*HEART_GAP)) // 2 # Calcula posicao inicial dos coracoes para centralizar

                # Desenha cada coracao (cheio ou vazio)
                for i in range(MAX_LIVES): 
                    xh = start_x + i*(HEART_SIZE + HEART_GAP) # Posicao X do coracao atual
                    if self.life_player1 > i:
                        pyxel.blt(xh, y_heart, 0, 0, 32, HEART_SIZE, HEART_SIZE, colkey=0)  # Desenha coracao cheio
                    else:
                        pyxel.blt(xh, y_heart, 0, 8, 32, HEART_SIZE, HEART_SIZE, colkey=0)  # Desenha coracao vazio

                # Pontuação Singleplayer
                pyxel.text(
                    cx,                     # x centralizado
                    y_bar + FUEL_BAR_H + HEART_SIZE + 4,   # 1px abaixo dos corações
                    f"Score: {self.score_player1}",
                    COLOR_TEXT
                )

        # # Debug: mostra posições
        # if self.is_host:                                       # Se for o host
        #     pyxel.text(10, 20, f"Host: {self.player_x},{self.player_y}", 7)  # Mostra posição do host
        #     pyxel.text(10, 30, f"Cliente: {self.player2_x},{self.player2_y}", 7)  # Mostra posição do cliente
        # else:                                                  # Se for o cliente
        #     pyxel.text(10, 20, f"Host: {self.player2_x},{self.player2_y}", 7)  # Mostra posição do host
        #     pyxel.text(10, 30, f"Cliente: {self.player_x},{self.player_y}", 7)  # Mostra posição do cliente        

        # # Debug: hitbox das árvores
        # for arvore in self.background.tree_manager.arvores:    # Itera por todas as árvores
        #     arv_left, arv_top, arv_right, arv_bottom = arvore.hitbox  # Obtém coordenadas da hitbox
        #     pyxel.rectb(arv_left, arv_top, arv_right - arv_left, arv_bottom - arv_top, 8)  # Desenha retângulo da hitbox
        # # debug: hitbox dos barcos
        # for b in self.boat_manager.boats:
        #     bar_left, bar_top, bar_right, bar_bottom = b.hitbox  # Obtém coordenadas da hitbox
        #     pyxel.rectb(bar_left, bar_top, bar_right - bar_left, bar_bottom - bar_top, 8)  # Desenha retângulo da hitbox
        # # # Debug: hitbox do jogador 1
        # pyxel.rectb(self.player_x, self.player_y, PLAYER_WIDTH, PLAYER_HEIGHT, 8)  # Desenha retângulo da hitbox do jogador 1

