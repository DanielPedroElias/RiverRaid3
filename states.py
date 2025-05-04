### Modulo de estados do jogo. Contem:
### - Telas de menu e submenus
### - Estados de jogo para singleplayer/multiplayer
### - Transicoes entre telas

# Bibliotecas
import time
import pyxel            # Engine do jogo
from config import *    # Importa constantes e configuracoes do arquivo "config.py"
from entities import *         # Importa entidades do jogo (tiro, inimigo, vida, etc.)
from collections import deque
import random

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

# Classe que tem o menu de Conexao com algum Host
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
    # Construtor
    def __init__(self, game):# "game" eh passado no construtor da classe "Game" do "main.py", sendo a instancia do jogo
        self.game = game # Recebe a instancia do jogo
        self.message = "Aguardando host iniciar o jogo..." # Mensagem que vai ser escrita nesse menu
        self.waiting = True # Marca se o Host iniciou ou nao a partida

    # Verifica se o Host iniciou ou nao a partida
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

        # Mantem a conexao ativa (envia heartbeat) para nao dar timeout
        if self.game.network.connected:
            self.game.network.send('heartbeat', {})

        # Volta ao menu principal se o usuario apertar "Esc"
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self.game.network.stop() # Fecha a conexao 
            self.game.change_state(MenuState(self.game)) # Volta para o menu principal

    # Desenha informacoes para o usario na tela
    def draw(self):
        # Limpa a tela
        pyxel.cls(COLOR_BG)
        
        # Escreve mensagens para o usuario para informar ele que o Host ainda nao iniciou o jogo
        pyxel.text(20, 75, self.message, COLOR_TEXT)
        pyxel.text(20, 105, "Pressione ESC para cancelar", COLOR_TEXT)

# Classe que contem o submenu para 'Hostear' um jogo
class HostGameState:
    # Construtor
    # Configura estado de hospedagem do jogo
    def __init__(self, game): # "game" eh passado no construtor da classe "Game" do "main.py", sendo a instancia do jogo
        self.game = game # Recebe a instancia do jogo
        self.message = "" # Mensagem de sucesso/erro de conexao 
        self.message_timer = 0 # Quanto tempo (frames) a mensagem de sucesso/erro de conexao ficara sendo exibida
        
        # Inicia host automaticamente
        if self.game.network.start_host():
            self.ip   = self.game.network.local_ip  # Pega o IP local
            self.port = self.game.network.port      # Pega a Porta 
        # Caso de algum erro ao inciar o host
        else:
            self.ip = "—"
            self.port = "—"
            self.message = "Erro ao iniciar host"
            self.message_timer = MESSAGE_DISPLAY_TIME
    

        
    # Controla inicio do jogo e saida do menu
    def update(self):
        # mantem cliente vivo (envia heartbeat) para evitar timeout
        if self.game.network.connected:
            self.game.network.send('heartbeat', {})

        # Se o usuario apertar "Enter", vai para o jogo normal e ativa o multiplayer (de forma assincrona)
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.game.network.send('game_start', {})
            self.game.change_state(GameState(self.game, is_multiplayer=True))
        
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
        pyxel.text(20, 30, "Hosting Game", COLOR_TEXT)
        pyxel.text(20, 60, f"IP: {self.ip}", COLOR_TEXT)
        pyxel.text(20, 90, f"Port: {self.port}", COLOR_TEXT)


        # Mostra status da conexao
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
            # TODO: Arruamar essa logica para se for o host, ele enviar todos os dados necessarios para o jogo funcionar, mesmo na tela de pause
            # TODO: Se for o cliente, ele deve enviar todos os seus dados tamebm na tela de pause (ele pode tomar dano enquanto esta no pause)
            self.game.previous_state.send_data('moviment', {'payload': [self.game.previous_state.player_x, self.game.previous_state.player_y]})  # Continua enviando dados
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
        pyxel.text(50, 60, "Jogo Pausado", COLOR_TEXT)

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

# Classe que gerencia o jogo principal (todos os estados, players, comunicacao via rede, etc.)
class GameState:
    # Construtor
    # Estado principal onde o jogo acontece
    def __init__(self, game, is_multiplayer=False, is_host=False, initial_seed=None, initial_rio_centro=None , initial_rio_largura=None): # "game" eh passado no construtor da classe "Game" do "main.py", sendo a instancia do jogo
        self.game = game # Recebe a instancia do jogo

        # Multiplayer
        self.is_multiplayer = is_multiplayer # Recebe se o jogo estah com multiplayer ativo ou nao
        
        # Flag para identificar se eh o host
        self.is_host = is_host  # Flag para identificar se é o host

        # Posicoes dos jogadores
        # Posicionamento inicial dos jogadores (host vs cliente)
        if is_host:
            # Host controla jogador 1 (esquerda)
            self.player_x, self.player_y = 59, 130  # Posicao inicial do jogador
            # Jogador 2 (cliente) começa à direita
            self.player2_x, self.player2_y = 79, 130  # Posicao inicial do segundo jogador
        else:
            # Cliente controla jogador 2 (direita)
            self.player_x, self.player_y = 79, 130   # Posicao inicial do jogador
            # Jogador 1 (host) começa à esquerda
            self.player2_x, self.player2_y = 59, 130  # Posicao inicial do segundo jogador

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

        # Inicializa o cenário de fundo
        self.background = Background(is_host=is_host , is_multiplayer=is_multiplayer) 

        # Sistema de invencibilidade
        self.invincible_timer_j1 = 0  # Temporizador de invencibilidade do jogador 1
        self.invincible_timer_j2 = 0  # Temporizador de invencibilidade do jogador 2
        self.INVINCIBILITY_DURATION = 90  # Duração em frames (1.5s a 60FPS)

        # Sincronização inicial do jogo (apenas multiplayer)
        if initial_seed is not None:
            # Sincroniza a seed aleatória para árvores
            self.background.tree_manager.random_seed = initial_seed
            random.seed(initial_seed)
            self.background.tree_manager.reset_arvores()
        
        if initial_rio_centro is not None and not is_host:
            # Sincroniza a posição do rio para clientes
            self.background.centro_rio_x = initial_rio_centro
            self.background.target_centro_x = initial_rio_centro
        
        if initial_rio_largura is not None and not is_host:
            self.background.largura_rio     = initial_rio_largura
            self.background.target_largura  = initial_rio_largura

        if is_multiplayer and not is_host:  # Apenas clientes multiplayer não atualizam
            self.background.tree_manager.update_arvores = lambda _: None  # Desabilita atualização de árvores para clientes

        # Controle do draw/update para a tela de pause:
        # Esse atributo ajuda a forcar o pyxel a rodar o draw depois do update
        # Evita que o jogo desenhe objetos em um estado "prematuro" antes do jogo atualizar a real posicao deles com o update
        # Isso eh basicamente usado no momento que o jogo sai da tela de pause (problemas com a engine do Pyxel)        
        self.last_update_frame = -1

    
    # Gerencia a logica do jogo
    def update(self):
        self.background.update()  # Atualiza o cenário

        # Envia e recebe dados do jogo se estiver no modo Multiplayer
        if self.is_multiplayer and self.game.network.connected:
            # 'update()' rodou nesse frame
            self.last_update_frame = pyxel.frame_count
            
            # Movimentacao
            self.send_data('moviment', {'payload': [self.player_x, self.player_y]}) # Envia dados

            # dados da HUD
            self.send_data('hud', {
                'fuel': self.current_fuel,
                'lives': self.current_lives
            })
            
            # mapa: seed, centro, largura do rio e arvores
            self.send_data('map', {
                'seed': self.background.tree_manager.random_seed,
                'rio_centro': self.background.centro_rio_x,
                'rio_largura': self.background.largura_rio,
                'arvores': self.background.tree_manager.get_tree_states()  # Adicione esta linha
            })

            # Invencibilidade
            self.send_data('status_player', {
                'invincible': self.invincible_timer_j1 if self.is_host else self.invincible_timer_j2,  # Timer de invencibilidade
            })
            

            # TODO: Arrumar o logica de recepcao de dados
            self.receive_data()  # Atualiza dados do segundo jogador

        # Logica de tiro:
        # Dispara localmente respeitando cooldown
        now = pyxel.frame_count / FPS # Pega o tempo atual (utilizando apenas o pyxel)
        
        # Se jogador atirou (apertou "Espaco") e se o tempo do ultimo tiro dado for maior que o cooldown do aviao 
        if pyxel.btn(pyxel.KEY_SPACE) and now - self._last_shot >= SHOT_COOLDOWN:
            # Cria o tiro no centro do aviao
            bx = self.player_x + PLAYER_WIDTH//2 - BULLET_WIDTH//2 # Posicao x do tiro = (posicao do jogador + (largura do jogador e do tiro) // 2)
            by = self.player_y # Posicao y do tiro
            b = Bullet(bx, by) # Cria o tiro local
            self.bullets.append(b) # Adiciona o tiro local dado na lista de tiros do jogador 1
            self._last_shot = now # Atualiza o tempo em que o tiro foi dado

            if self.is_multiplayer and self.game.network.connected:
                # Envia o evento de tiro imediatamente
                self.send_data('shot', {'x': bx, 'y': by})

        # Atualiza todos os tiros (locais e remotos)
        for lst in (self.bullets, self.remote_bullets):
            for bullet in lst:
                bullet.update()

        # Remove os tiros que sairam da tela (locais e remotos)
        self.bullets = [tiro for tiro in self.bullets if tiro.alive]
        self.remote_bullets = [tiro for tiro in self.remote_bullets if tiro.alive]



        # TODO: Implementar a atualizacao para elementos da HUD
        # Dranagem do combustivel:
        # Consome um pouco de combustivel a cada frame
        consumption_per_frame = FUEL_CONSUMPTION_RATE / FPS # Calcula qtd de gasolina para consumir neste frame (unidades por frame)
        self.current_fuel = max(0, self.current_fuel - consumption_per_frame) # Decrementa, garantindo que nunca fique negativo


        # Atualiza temporizadores de invencibilidade
        if self.invincible_timer_j1 > 0:
            self.invincible_timer_j1 -= 1 # Invencibilidade do jogador 1
        if self.invincible_timer_j2 > 0:
            self.invincible_timer_j2 -= 1 # Invencibilidade do jogador 2

        # Se o usuario apertar "Esc", pausa o jogo
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self.game.previous_state = self  # Guarda estado atual do jogo (passando a instancia)
            self.game.change_state(PauseMenuState(self.game)) # Troca o estado para o menu de pause
            return  # Sai da atualizacao


        # Logica de movimentacao:
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
        game_area_height = SCREEN_HEIGHT - HUD_HEIGHT
        self.player_y = max(0, min(self.player_y, game_area_height - PLAYER_HEIGHT))

        # Verificação de colisões
        self.check_all_collisions()
    
    # Envia dados do jogador para a rede
    def send_data(self, packet_type: str, data: dict):
        # packet_type = nome do fluxo ('moviment','shot','life',...)
        # data = os campos para cada tipo
        
        # Enviar dados se estiver em multiplayer e conectados (tanto host quanto cliente)
        if self.is_multiplayer and self.game.network.connected:
            self.game.network.send(packet_type, data)

    # Processa dados recebidos da rede
    def receive_data(self):
        # Processa todos os pacotes na fila, ordenados por prioridade
        while self.game.network.received_packets:
            pkt = self.game.network.received_packets.pop(0)  # Remove o primeiro da fila (com maior prioridade)
            
            if not isinstance(pkt, dict):
                continue  # Ignora pacotes invalidos
            
            type = pkt.get('type') # Recebe o tipo do pacote
            # Verifica cada pacote de acordo com o tipo e atualiza os dados recebidos
            if type == 'moviment': # Posicao do jogador 2
                x, y = pkt['payload']
                self.player2_x = x
                self.player2_y = y

            elif type == 'shot': # Tiro dado pelo jogador 2
                # Posicoes do tiro
                bx = pkt['x']
                by = pkt['y']

                # Extrai o momento exato em que o tiro foi dado (em segundos)
                spawn_time = pkt['timestamp']

                # Calcula a velocidade real do tiro em pixels/segundo:
                # BULLET_SPEED estah em pixels/frame. Multiplicando por FPS (frames/segundo), resulta em => pixels/segundo
                # O sinal negativo indica movimento para cima (eixo Y negativo)
                speed_per_sec = -BULLET_SPEED * FPS # Velocidade real do tiro em pixels/segundo
                
                # Calcula quanto tempo se passou desde o tiro ateh agora (idade do tiro)
                age = time.time() - spawn_time

                # Calcula onde o tiro DEVERIA estar AGORA, considerando:
                #   y_now = posicao_inicial + (velocidade * tempo_decorrido)
                y_now = by + speed_per_sec * age

                # Verifica se o tiro ja deveria ter saido da tela (posicao em 'Y' atual + altura < 0 (limite superior da tela))
                if y_now + BULLET_HEIGHT < 0:
                    continue # Ignora o tiro (nao adiciona ele na lista de tiros e nem cira a sua instancia)

                # Cria uma nova instancia de tiro remoto
                b = RemoteBullet(bx, by, spawn_time) 
                # Adiciona a nova instancia na lista de tiros remotos para serem atualizados e desenhados (dentro do GameState)
                self.remote_bullets.append(b)
            
            elif type == 'hud': # Elementos da HUD do segundo jogador (gasolina e qtd de vidas)
                # atualiza HUD do jogador remoto
                # Caso algum campo falhe (pacote corrompido), mantem o valor anterior como padrao
                self.current_fuel_p2 = pkt.get('fuel', self.current_fuel_p2)
                self.current_lives_p2 = pkt.get('lives', self.current_lives_p2)

            elif type == 'map':
                if not self.is_host:
                    self.background.centro_rio_x = pkt.get('rio_centro', self.background.centro_rio_x)
                    self.background.target_centro_x = pkt.get('rio_centro', self.background.target_centro_x)
                    self.background.largura_rio = pkt.get('rio_largura', self.background.largura_rio)
                    self.background.target_largura = pkt.get('rio_largura', self.background.target_largura)
                    
                    # Sincroniza árvores
                    if 'arvores' in pkt:
                        self.background.tree_manager.set_tree_states(pkt['arvores'])
                if 'seed' in pkt and pkt['seed'] != self.background.tree_manager.random_seed:
                    random.seed(pkt['seed'])
                    self.background.tree_manager.random_seed = pkt['seed']
                    self.background.tree_manager.reset_arvores()

            elif type == 'status_player':
                inv = pkt.get('invincible', 0)
                if self.is_host:
                    # host atualiza invencibilidade do cliente
                    self.invincible_timer_j2 = inv
                else:
                    # cliente atualiza invencibilidade do host
                    self.invincible_timer_j1 = inv

            # Ignora heartbeat (a propria rede, no 'network.py' ja lida com isso)
            elif type == 'heartbeat':
                continue


    # Renderiza mapa, jogadores e elementos do jogo
    def draw(self):
        # Limpa a tela
        pyxel.cls(COLOR_BG)

        # Desenha tiros locais
        for b in self.bullets:
            b.draw()

        # Desenha tiros remotos
        # So desenha remotos se 'update()' ja rodou este frame (evita problemas com a tela de pause)
        if self.last_update_frame == pyxel.frame_count:
            for b in self.remote_bullets:
                b.draw()

        # Desenha jogadores com invencibilidade piscante
        j1 = (self.invincible_timer_j1//5)%2==0 if self.invincible_timer_j1>0 else True
        j2 = (self.invincible_timer_j2//5)%2==0 if self.invincible_timer_j2>0 else True
        if j1:
            pyxel.rect(self.player_x, self.player_y, PLAYER_WIDTH, PLAYER_HEIGHT, COLOR_PLAYER)
        if self.is_multiplayer and j2:
            pyxel.rect(self.player2_x, self.player2_y, PLAYER_WIDTH, PLAYER_HEIGHT, COLOR_PLAYER2_GENERIC)

        # Separador da HUD (linha que divide o jogo da interface)
        sep_y = SCREEN_HEIGHT - HUD_HEIGHT # Posicao em 'Y' = Separador eh igual a altura da tela menos a altura da HUD
        pyxel.line(0, sep_y, SCREEN_WIDTH, sep_y, COLOR_HUD_LINE) # Desenha a linha horizontal da hud

        # Informacoes da hud Para o Multiplayer:
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


            # Barra de combustivel - Jogador 1
            # desenha barra do jogador 1
            pyxel.rectb(x1, y_bar, bar_w, FUEL_BAR_H, COLOR_FUEL_BORDER) # Desenha borda da barra
            filled1 = int((self.current_fuel / MAX_FUEL) * (bar_w - 2)) # Calcula o nivel de preenchimento da barra
            pyxel.rect(x1 + 1, y_bar + 1, filled1, FUEL_BAR_H - 2, COLOR_FUEL) # Preenche proporcionalmente a barra de gasolina

            # Barra de combustivel - Jogador 2 
            pyxel.rectb(x2, y_bar, bar_w, FUEL_BAR_H, COLOR_FUEL_BORDER) # Desenha borda da barra
            filled2 = int((self.current_fuel_p2 / MAX_FUEL) * (bar_w - 2)) # Calcula o nivel de preenchimento da barra
            pyxel.rect(x2 + 1, y_bar + 1, filled2, FUEL_BAR_H - 2, COLOR_FUEL) # Preenche proporcionalmente a barra de gasolina

            # Coracoes (vidas) em baixo das barras de gasolina
            y_heart = y_bar + FUEL_BAR_H + 2 # Posicao Y dos coracoes

            # Coracao - Jogador 1
            # Centraliza coracao abaixo da barra
            total_heart_w = MAX_LIVES * HEART_SIZE + (MAX_LIVES - 1) * HEART_GAP # Largura total dos coracoes
            start_x1 = x1 + (bar_w - total_heart_w) // 2 # Calcula posicao inicial para centralizar

            # Desenha cada coracao (cheio ou vazio)
            for i in range(MAX_LIVES):
                cx = start_x1 + i * (HEART_SIZE + HEART_GAP) # Posicao X do coracao atual

                # Escolhe cor baseada na vida restante e desenha o coracao
                color_heart = COLOR_HEART_FULL if self.current_lives > i else COLOR_HEART_EMPTY
                pyxel.rect(cx, y_heart, HEART_SIZE, HEART_SIZE, color_heart)

            # Coracao - Jogador 2 (ja foi calculado a largura total dos coracoes)
            start_x2 = x2 + (bar_w - total_heart_w) // 2 # Calcula posicao inicial para centralizar

            # Desenha cada coracao (cheio ou vazio)
            for i in range(MAX_LIVES):
                cx = start_x2 + i * (HEART_SIZE + HEART_GAP) # Posicao X do coracao atual

                # Escolhe cor baseada na vida restante e desenha o coracao
                color_heart = COLOR_HEART_FULL if self.current_lives_p2 > i else COLOR_HEART_EMPTY
                pyxel.rect(cx, y_heart, HEART_SIZE, HEART_SIZE, color_heart)

            # Texto de status (DEBUG) para mostrar conexao com o segundo jogador
            if self.game.network.connected:
                # Estah conectado com algum outro jogador
                pyxel.text(10, 10, "Multiplayer - Conectado", COLOR_TEXT_HIGHLIGHT)

            else:
                # Nao estah conectado com nenhum jogador
                pyxel.text(10, 10, "Multiplayer - Desconectado", COLOR_TEXT_HIGHLIGHT)
        
        
        # HUD para modo singleplayer
        else:
            # HUD centralizada
            cx = (SCREEN_WIDTH - FUEL_BAR_W) // 2 # Centraliza caoracao em 'X' na horizontal
            y_bar = sep_y + 2 # Posicao Y inicial das barras de gasolina (2px abaixo do separador da HUD)

            # Desenha uma unica barra de combustivel:
            pyxel.rectb(cx, y_bar, FUEL_BAR_W, FUEL_BAR_H, COLOR_FUEL_BORDER) # Desenha borda da barra
            filled = int((self.current_fuel / MAX_FUEL) * (FUEL_BAR_W - 2)) # Calcula o nivel de preenchimento da barra
            pyxel.rect(cx+1, y_bar+1, filled, FUEL_BAR_H-2, COLOR_FUEL) # Preenche proporcionalmente a barra de gasolina

            # Coracoes
            y_heart = y_bar + FUEL_BAR_H + 2 # Posicao Y dos coracoes (em baixo da barra de gasolina)
            start_x = (SCREEN_WIDTH - (MAX_LIVES*HEART_SIZE + (MAX_LIVES-1)*HEART_GAP)) // 2 # Calcula posicao inicial dos coracoes para centralizar

            # Desenha cada coracao (cheio ou vazio)
            for i in range(MAX_LIVES): 
                xh = start_x + i*(HEART_SIZE + HEART_GAP) # Posicao X do coracao atual

                # Escolhe cor baseada na vida restante e desenha o coracao
                color_heart = COLOR_HEART_FULL if self.current_lives > i else COLOR_HEART_EMPTY
                pyxel.rect(xh, y_heart, HEART_SIZE, HEART_SIZE, color_heart)

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
                    self.current_lives = max(0, self.current_lives - 1)  # Perde vida 
                    self.invincible_timer_j1 = self.INVINCIBILITY_DURATION  # Ativa invencibilidade

            # Lógica do cliente para jogador 2
            elif not self.is_host and self.invincible_timer_j2 <= 0:
                colisoes = check_tree_collision(
                    self.player_x, self.player_y,
                    self.background.tree_manager.arvores,
                    "Jogador 2"
                )
                if colisoes > 0:
                    self.current_lives_p2 = max(0, self.current_lives_p2 - 1)  # Perde vida
                    self.invincible_timer_j2 = self.INVINCIBILITY_DURATION  # Ativa invencibilidade
        else:
            # Lógica singleplayer
            if self.invincible_timer_j1 <= 0:
                colisoes = check_tree_collision(
                    self.player_x, self.player_y,
                    self.background.tree_manager.arvores,
                    "Jogador 1"
                )
                if colisoes > 0:
                    self.current_lives = max(0, self.current_lives - 1)  # Perde vida
                    self.invincible_timer_j1 = self.INVINCIBILITY_DURATION  # Ativa invencibilidade


class Background:
    def __init__(self, is_host=False , is_multiplayer=False):
        self.is_host = is_host
        self.is_multiplayer = is_multiplayer

        # movimento vertical
        self.velocidade_scroll = 1
        self.deslocamento = 0

        # largura do rio (agora animável)
        self.largura_rio = 45
        self.target_largura = self.largura_rio        # ← alvo para animação de largura
        self.largura_speed = .5                      # ← velocidade de ajuste da largura

        # centro do rio (já existente)
        self.centro_rio_x = pyxel.width / 2
        self.target_centro_x = self.centro_rio_x
        self.curve_speed = .5

        # histórico para “descer” curvas e larguras do topo
        self.centros_hist = deque([self.centro_rio_x] * pyxel.height,
                                  maxlen=pyxel.height)
        self.largura_hist = deque([self.largura_rio] * pyxel.height,
                                  maxlen=pyxel.height)       # ← novo

        self.cor_borda = 15
        self.pontos_brancos = [(3, 2), (10, 5), (15, 8), (25, 3), (30, 7), 
                             (5, 14), (20, 12), (28, 16), (12, 20), (18, 18)]
        self.tree_manager = TreeManager(self)


        # Novo estado para controle da animação
        self.animating_to_center = False
        self.max_largura = pyxel.width - 30  # Largura máxima igual ao KEY_3

        

    def obter_margens_rio(self, screen_y):
        centro = self.centros_hist[screen_y]
        largura = self.largura_hist[screen_y]           # ← histórico de largura
        meia = largura / 2
        return centro - meia, centro + meia

    def update(self):
        
        
        if self.is_host or not self.is_multiplayer:
            # —–– curvar (1/2)
            if pyxel.btnp(pyxel.KEY_1):
                self.target_centro_x = min(self.target_centro_x + 30,
                                        pyxel.width - self.largura_rio/2)
            if pyxel.btnp(pyxel.KEY_2):
                self.target_centro_x = max(self.target_centro_x - 30,
                                        self.largura_rio/2)

            # —–– ajustar centro suavemente
            diff_c = self.target_centro_x - self.centro_rio_x
            if abs(diff_c) > self.curve_speed:
                self.centro_rio_x += self.curve_speed * (1 if diff_c > 0 else -1)
            else:
                self.centro_rio_x = self.target_centro_x

            # —–– largura (3/4)
            if pyxel.btnp(pyxel.KEY_3):
                # aumenta até um máximo (por ex. metade da largura da tela)
                self.target_largura = min(self.target_largura + 10,
                                        self.max_largura)
                
            if pyxel.btnp(pyxel.KEY_4):
                # diminui até um mínimo (por ex. 20 px)
                self.target_largura = max(self.target_largura - 10, 20)

            # Novo controle KEY_5
            if pyxel.btnp(pyxel.KEY_5):
                self.animating_to_center = True
                self.target_centro_x = pyxel.width / 2  # Primeiro centraliza
                self.target_largura = 45  # Reset para largura inicial

            # atualiza árvores
            self.tree_manager.update_arvores(self.velocidade_scroll)
        
        # Lógica da animação automática
        if self.animating_to_center:
            # Verifica se já centralizou
            if abs(self.centro_rio_x - pyxel.width/2) < 1:
                # Começa a expandir após centralizar
                self.target_largura = self.max_largura
                
                # Desativa a animação quando chegar na largura máxima
                if abs(self.largura_rio - self.max_largura) < 1:
                    self.animating_to_center = False
            else:
                # Mantém largura pequena durante a centralização
                self.target_largura = 45

        diff_l = self.target_largura - self.largura_rio
        if abs(diff_l) > self.largura_speed:
            self.largura_rio += self.largura_speed * (1 if diff_l > 0 else -1)
        else:
            self.largura_rio = self.target_largura

        # —–– atualizar históricos
        self.centros_hist.appendleft(self.centro_rio_x)
        self.largura_hist.appendleft(self.largura_rio)   # ← novo
        
        
        self.deslocamento += self.velocidade_scroll

       

    def draw(self):
        pyxel.rect(0, 0, pyxel.width, pyxel.height, 9)
        for screen_y in range(pyxel.height):
            esq, dir = self.obter_margens_rio(screen_y)
            # bordas
            for i in range(4):
                pyxel.line(int(esq)-i, screen_y, int(esq), screen_y,
                           self.cor_borda)
                pyxel.line(int(dir), screen_y, int(dir)+i, screen_y,
                           self.cor_borda)
            # água
            pyxel.line(int(esq), screen_y, int(dir), screen_y, 12)
            # reflexos
            for dx, dy in self.pontos_brancos:
                pattern_y = (screen_y - self.deslocamento + dy) % 24
                if pattern_y == dy:
                    largura_atual = dir - esq
                    if largura_atual > 0:
                        x = esq + (dx % largura_atual)
                    if esq < x < dir:
                        pyxel.pset(int(x), screen_y, 7)
        
        self.tree_manager.draw_arvores()
