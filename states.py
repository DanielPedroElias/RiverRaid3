### Modulo de estados do jogo. Contem:
### - Telas de menu e submenus
### - Estados de jogo para singleplayer/multiplayer
### - Transicoes entre telas

# Bibliotecas
import time
import pyxel            # Engine do jogo
from config import *    # Importa constantes e configuracoes do arquivo "config.py"
from entities import *         # Importa entidades do jogo (tiro, inimigo, vida, etc.)
# Importa estrutura de dados deque
from collections import deque

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
        pyxel.text(50, 60, "River Raid 3", COLOR_TEXT)

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
            pyxel.text(50, 90 + (i*20), opt, color)

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
        pyxel.text(50, 60, "Multiplayer", COLOR_TEXT)

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
            pyxel.text(50, 90 + (i*20), opt, color)

        # Escreve na tela "Pressione ESC para voltar"
        pyxel.text(20, 150, "Pressione ESC para voltar", COLOR_TEXT)

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
        pyxel.text(20, 30, "Conecte a um Host", COLOR_TEXT)
        
        # Imprime o campo IP
        pyxel.text(20, 60, "IP:", COLOR_TEXT)
        # Se o IP estiver selecionado, deixa ele marcado, caso contrario, deixa ele com a cor normal
        border_color = COLOR_TEXT_HIGHLIGHT if self.current_input == "ip" else COLOR_TEXT
        pyxel.rectb(40, 60, 100, 8, border_color) # Desenha um retangulo apenas com a borda
        pyxel.text(42, 62, self.ip_input, COLOR_TEXT) # Desenha o que o usuario ja digitou ateh o momento no IP
        
        # Imprime o campo Porta
        pyxel.text(20, 90, "Port:", COLOR_TEXT)
        # Se a Porta estiver selecionada, deixa ela marcada, caso contrario, deixa ela com a cor normal
        border_color = COLOR_TEXT_HIGHLIGHT if self.current_input == "port" else COLOR_TEXT
        pyxel.rectb(40, 90, 50, 8, border_color) # Desenha um retangulo apenas com a borda
        pyxel.text(42, 92, self.port_input, COLOR_TEXT) # Desenha o que o usuario ja digitou ateh o momento na Porta
        
        # Mensagem de status
        if self.message_timer > 0: # Se o timer for maior do que zero, desenha a mensagem de sucesso/erro de conexao
            # Se estiver escrito "Sucesso" dentro da mensagem, coloca na cor para suceso
            # Caso contrario colocar a cor para falha
            color = COLOR_SUCCESS if "Sucesso" in self.message else COLOR_ERROR
            pyxel.text(20, 120, self.message, color) # Desenha a mensagem na tela
        
        # Campos de ajuda de navegacao no menu
        pyxel.text(10, 135, "TAB: Troca de Campo", COLOR_TEXT)
        pyxel.text(10, 150, "ENTER: Connectar", COLOR_TEXT)
        pyxel.text(10, 165, "ESC: Voltar", COLOR_TEXT)

# Classe que tem o submenu em que o cliente aguarda o host iniciar o jogo
class WaitingForHostState:
    # Método de inicialização da classe
    def __init__(self, game):
        self.game = game  # Referência para o objeto principal do jogo
        self.message = "Aguardando host iniciar o jogo..."  # Mensagem exibida ao usuário
        self.waiting = True  # Flag indicando que está aguardando

    # Método chamado a cada frame para atualizar o estado
    def update(self):
        # Processa TODOS os pacotes na fila
        while self.game.network.received_packets:
            pkt = self.game.network.received_packets.pop(0)
            
            # Verifica se o host enviou sinal para iniciar o jogo
            # 1 - Se o host nao iniciou ainda, espera ele iniciar o jogo
            if pkt.get('type') == 'game_start':
                self.game.change_state(GameState(self.game, is_multiplayer=True))
                return
            
            # 2 - Se vier um pacote de "moviment" (payload como lista), o host ja comecou o jogo antes do cliente entrar
            elif pkt.get('type') == 'moviment':
                self.game.change_state(GameState(self.game, is_multiplayer=True))
                return

        # Se estiver conectado, envia um sinal de "heartbeat" para manter a conexão
        if self.game.network.connected:
            self.game.network.send('heartbeat', {})

        # Se pressionar ESC, cancela e volta ao menu
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self.game.network.stop()  # Encerra a conexão
            self.game.change_state(MenuState(self.game))  # Volta ao menu principal

    # Método para desenhar a tela
    def draw(self):
        # Limpa a tela com a cor de fundo
        pyxel.cls(COLOR_BG)
        
        # Escreve mensagens para o usuario para informar ele que o Host ainda nao iniciou o jogo
        pyxel.text(20, 75, self.message, COLOR_TEXT)
        pyxel.text(20, 105, "Pressione ESC para cancelar", COLOR_TEXT)

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
            self.game.network.send('heartbeat', {})

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
            
            # Muda para o estado de jogo
            self.game.change_state(game_state)

        # Se o usuario apertar "Esc", volta para a tela de menu do multiplayer
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
        # Imprime informacoes sobre o IP e a porta do usuario (para ele passar para outra pessoa conectar)
        pyxel.text(20, 30, "Hosting Game", COLOR_TEXT)
        pyxel.text(20, 60, f"IP: {self.ip}", COLOR_TEXT)
        pyxel.text(20, 90, f"Port: {self.port}", COLOR_TEXT)


        # Exibe status da conexão
        if self.game.network.connected:
            pyxel.text(20, 120, "Cliente conectado", COLOR_SUCCESS)
        # Se nao tiver nenhum cliente conectado
        else:
            pyxel.text(20, 120, "Aguardando cliente...", COLOR_TEXT)

        # Mensagens de navegacao entre menus/jogo
        pyxel.text(10, 135, "Pressione ENTER para comecar o jogo", COLOR_TEXT_HIGHLIGHT)
        pyxel.text(10, 150, "Pressione ESC para voltar", COLOR_TEXT)


# Classe para o menu de pause do jogo
class PauseMenuState:
    # Método de inicialização
    def __init__(self, game):
        self.game = game  # Referência para o objeto principal do jogo
        self.selected = 0  # Opção selecionada no menu (0 = Continuar, 1 = Menu Principal)
        self.options = ["Continuar", "Menu Principal"]  # Opções do menu

    # Método para atualizar o estado a cada frame
    def update(self):
        # Se estava em jogo multiplayer, mantém a rede ativa
        if isinstance(self.game.previous_state, GameState) and self.game.previous_state.is_multiplayer:
            # TODO: Arruamar essa logica para se for o host, ele enviar todos os dados necessarios para o jogo funcionar, mesmo na tela de pause
            # TODO: Se for o cliente, ele deve enviar todos os seus dados tamebm na tela de pause (ele pode tomar dano enquanto esta no pause)
            self.game.previous_state.send_data('moviment', {'payload': [self.game.previous_state.player_x, self.game.previous_state.player_y]})  # Continua enviando dados
            self.game.previous_state.receive_data()  # Continua recebendo dados

        # Navegação pelo menu com teclas DOWN/S ou UP/W
        if pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_S):
            self.selected = (self.selected + 1) % 2  # Alterna entre opções
        elif pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W):
            self.selected = (self.selected - 1) % 2  # Alterna entre opções
            
        # Confirmação com ENTER
        if pyxel.btnp(pyxel.KEY_RETURN):
            if self.selected == 0:  # Continuar
                self.game.change_state(self.game.previous_state)  # Volta ao jogo
            else:  # Menu Principal
                # Se estava em multiplayer, encerra a conexão
                if isinstance(self.game.previous_state, GameState) and self.game.previous_state.is_multiplayer:
                    self.game.network.stop()
                # Volta ao menu principal
                self.game.change_state(MenuState(self.game))
        
        # Se pressionar ESC, também volta ao jogo (atalho para Continuar)
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self.game.change_state(self.game.previous_state)
    
    # Método para desenhar o menu
    def draw(self):
        # Limpa a tela
        pyxel.cls(COLOR_BG)

        # Escreve "Jogo Pausado" na tela
        pyxel.text(50, 60, "Jogo Pausado", COLOR_TEXT)

        # Desenha as opções do menu
        for i, opt in enumerate(self.options):
            # Define a cor (destaque para opção selecionada)
            color = COLOR_TEXT if i != self.selected else COLOR_TEXT_HIGHLIGHT

            # Pinta as opcoes do menu com as suas respectivas cores
            # "i * 20" calcula a posicao em Y de cada opcao.
            #   - 1 opcao: (i = 0): 60 + (0*20) = 60
            #   - 2 opcao: (i = 1): 60 + (1*20) = 80
            # "opt" recebe o texto de cada opcao
            pyxel.text(50, 90 + (i*20), opt, color)

# Classe que gerencia o jogo principal (todos os estados, players, comunicacao via rede, etc.)
class GameState:
    # Construtor
    # Estado principal onde o jogo acontece
    def __init__(self, game, is_multiplayer=False, is_host=False, initial_seed=None, initial_rio_centro=None , initial_rio_largura=None): # "game" eh passado no construtor da classe "Game" do "main.py", sendo a instancia do jogo
        self.game = game # Recebe a instancia do jogo

        # Multiplayer
        self.is_multiplayer = is_multiplayer # Recebe se o jogo estah com multiplayer ativo ou nao
        
        self.is_host = is_host  # Flag para identificar se é o host

        # Posicoes dos jogadores
        self.player_x = 70 # Posicao inicial em X do jogador
        self.player_y = 130 # Posicao inicial em Y do jogador
        self.player2_x = 0 # Posicao inicial em X do segundo jogador
        self.player2_y = 0 # Posicao inicial em Y do segundo jogador 

        # Tiro
        self.bullets = []          # Tiros locais
        self.remote_bullets = []   # Tiros recebidos pela rede
        self._last_shot = 0        # controla o cooldown

        # HUD
        # Valores (exemplo inicial)
        self.current_fuel = MAX_FUEL
        self.current_lives = MAX_LIVES
        # Valores para o jogador 2 (jogador 2)
        self.current_fuel_p2 = MAX_FUEL
        self.current_lives_p2 = MAX_LIVES

        # Controle do draw/update para a tela de pause:
        # Esse atributo ajuda a forcar o pyxel a rodar o draw depois do update
        # Evita que o jogo desenhe objetos em um estado "prematuro" antes do jogo atualizar a real posicao deles com o update
        # Isso eh basicamente usado no momento que o jogo sai da tela de pause (problemas com a engine do Pyxel)        
        self.last_update_frame = -1

    
    # Gerencia a logica do jogo
    def update(self):
        # Envia e recebe dados do jogo se estiver no modo Multiplayer
        if self.is_multiplayer:
            self.send_data()  # Envia dados
            self.receive_data()  # Atualiza dados do segundo jogador

        # Lógica de pausa
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self.game.previous_state = self  # Salva estado atual
            self.game.change_state(PauseMenuState(self.game))  # Vai para menu de pause
            return  # Sai da atualização

        # Atualiza logica do jogo (movimento, colisoes, rede)
        if pyxel.btn(pyxel.KEY_A):
            self.player_x -= PLAYER_SPEED
        if pyxel.btn(pyxel.KEY_D):
            self.player_x += PLAYER_SPEED
        if pyxel.btn(pyxel.KEY_W):
            self.player_y -= PLAYER_SPEED
        if pyxel.btn(pyxel.KEY_S):
            self.player_y += PLAYER_SPEED

        ## Trava o player dentro da tela
        # TODO: Trocar 'PLAYER_WIDTH' e 'PLAYER_HEIGHT' pela altura e largura do player quando tiver uma pixel art dos avioes
        # Player nao sai da tela no eixo X
        # - min(self._player_x, self.largura_tela - PLAYER_WIDTH): impede que o jogador va alem do lado direito da tela
        # - max(0, ...): impede que o jogador va alem do lado esquerdo da tela
        # - PLAYER_WIDTH eh a largura do jogador (mudar depois)
        self.player_x = max(0, min(self.player_x, SCREEN_WIDTH - PLAYER_WIDTH))

        # Player nao sai da tela no eixo Y
        # - min(self._player_y, self.altura_tela - PLAYER_HEIGHT): impede que o jogador va alem da parte inferior da tela
        # - max(0, ...): impede que o jogador va alem da parte superior da tela
        # - PLAYER_HEIGHT eh a altura do jogador (mudar depois)
        self.player_y = max(0, min(self.player_y, SCREEN_HEIGHT - PLAYER_HEIGHT))
    
    # Envia dados do jogador para a rede
    def send_data(self):
        # Enviar dados se estiver em multiplayer e conectados (tanto host quanto cliente)
        if self.is_multiplayer and self.game.network.connected:
            self.game.network.send([self.player_x, self.player_y])

    # Processa dados recebidos da rede
    def receive_data(self):
        # Apenas interpreta os dados se tiver no Multiplayer,
        # vier uma lista/tupla de pelo menos 2 numeros (de tamanho maior ou igual a 2)
        if self.is_multiplayer and isinstance(self.game.network.data, (list, tuple)) and len(self.game.network.data) >= 2:
            try:
                # Atualiza a posicao do segundo jogador
                self.player2_x = self.game.network.data[0]
                self.player2_y = self.game.network.data[1]
            
            # Se ocorrer um erro, imprime no terminal
            except (IndexError, TypeError):
                print("Dados recebidos inválidos")

    # Renderiza mapa, jogador e elementos do jogo
    def draw(self):
        # Limpa a tela
        pyxel.cls(COLOR_BG)

        # TODO: Mudar isso mais na frente para uma pixel art do jogador (um aviao)
        # Desenha o jogador
        pyxel.rect(self.player_x, self.player_y, PLAYER_WIDTH, PLAYER_HEIGHT, COLOR_PLAYER)

        # TODO: Ajustar ou remover essa parte quando o multiplayer estiver funcionando
        # Texto de status (DEBUG)
        # Desenha outro jogador (se estiver em multiplayer e houver dados)
        if self.is_multiplayer:
            if self.game.network.connected:
                pyxel.text(10, 10, "Multiplayer - Conectado", COLOR_TEXT_HIGHLIGHT)
                pyxel.rect(self.player2_x, self.player2_y, PLAYER_WIDTH, PLAYER_HEIGHT, COLOR_PLAYER2_GENERIC) # Cor diferente para diferenciar
        
            else:
                pyxel.text(10, 10, "Multiplayer - Desconectado", COLOR_TEXT_HIGHLIGHT)