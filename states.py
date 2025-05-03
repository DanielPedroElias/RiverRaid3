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
                initial_rio_centro=d.get('rio_centro')
            ))
            return

        # Se estiver conectado, envia um sinal de "heartbeat" para manter a conexão
        if self.game.network.connected:
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
                'rio_centro': game_state.background.centro_rio_x  # Posição do rio
            }
            # Envia dados para o cliente
            self.game.network.send(initial_data)
            
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
        self.game = game  # Referência para o objeto principal do jogo
        self.selected = 0  # Opção selecionada no menu (0 = Continuar, 1 = Menu Principal)
        self.options = ["Continuar", "Menu Principal"]  # Opções do menu

    # Método para atualizar o estado a cada frame
    def update(self):
        # Se estava em jogo multiplayer, mantém a rede ativa
        if isinstance(self.game.previous_state, GameState) and self.game.previous_state.is_multiplayer:
            self.game.previous_state.send_data()  # Continua enviando dados
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
        pyxel.cls(COLOR_BG)  # Limpa a tela
        pyxel.text(50, 40, "Jogo Pausado", COLOR_TEXT)  # Título

        # Desenha as opções do menu
        for i, opt in enumerate(self.options):
            # Define a cor (destaque para opção selecionada)
            color = COLOR_TEXT if i != self.selected else COLOR_TEXT_HIGHLIGHT
            pyxel.text(50, 60 + (i*20), opt, color)  # Desenha cada opção


# Importa estrutura de dados deque
from collections import deque

# Classe principal que gerencia o estado do jogo (singleplayer/multiplayer)
class GameState:
    # Método de inicialização
    def __init__(self, game, is_multiplayer=False, is_host=False, initial_seed=None, initial_rio_centro=None):
        self.game = game  # Referência para o objeto principal do jogo
        self.is_multiplayer = is_multiplayer  # Flag para modo multiplayer
        self.is_host = is_host  # Flag para identificar se é o host

        # Posicionamento inicial dos jogadores (host vs cliente)
        if is_host:
            # Host controla jogador 1 (esquerda)
            self.player_x, self.player_y = 59, 104  
            # Jogador 2 (cliente) começa à direita
            self.player2_x, self.player2_y = 79, 104  
        else:
            # Cliente controla jogador 2 (direita)
            self.player_x, self.player_y = 79, 104  
            # Jogador 1 (host) começa à esquerda
            self.player2_x, self.player2_y = 59, 104  

        # Inicializa o cenário de fundo
        self.background = Background(is_host=is_host)

        # Sistema de vidas e invencibilidade
        self.vida_jogador1 = 3  # Vida do jogador 1 (host)
        self.vida_jogador2 = 3  # Vida do jogador 2 (cliente)
        self.invincible_timer_j1 = 0  # Temporizador de invencibilidade do jogador 1
        self.invincible_timer_j2 = 0  # Temporizador de invencibilidade do jogador 2
        self.INVINCIBILITY_DURATION = 90  # Duração em frames (1.5s a 60FPS)

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

    # Método para atualizar o estado do jogo a cada frame
    def update(self):
        self.background.update()  # Atualiza o cenário

        # Comunicação em rede (apenas multiplayer)
        if self.is_multiplayer:
            self.send_data()  # Envia dados do jogador local
            self.receive_data()  # Recebe dados do outro jogador

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

        # Limites da tela
        self.player_x = max(0, min(self.player_x, SCREEN_WIDTH - PLAYER_WIDTH))
        self.player_y = max(0, min(self.player_y, SCREEN_HEIGHT - PLAYER_HEIGHT))

        # Atualiza temporizadores de invencibilidade
        if self.invincible_timer_j1 > 0:
            self.invincible_timer_j1 -= 1 # Invencibilidade do jogador 1
        if self.invincible_timer_j2 > 0:
            self.invincible_timer_j2 -= 1 # Invencibilidade do jogador 2

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
                    self.vida_jogador1 = max(0, self.vida_jogador1 - 1)  # Perde vida 
                    self.invincible_timer_j1 = self.INVINCIBILITY_DURATION  # Ativa invencibilidade

            # Lógica do cliente para jogador 2
            elif not self.is_host and self.invincible_timer_j2 <= 0:
                colisoes = check_tree_collision(
                    self.player_x, self.player_y,
                    self.background.tree_manager.arvores,
                    "Jogador 2"
                )
                if colisoes > 0:
                    self.vida_jogador2 = max(0, self.vida_jogador2 - 1)  # Perde vida
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
                    self.vida_jogador1 = max(0, self.vida_jogador1 - 1)  # Perde vida
                    self.invincible_timer_j1 = self.INVINCIBILITY_DURATION  # Ativa invencibilidade

    # Método para enviar dados pela rede
    def send_data(self):
        if self.is_multiplayer and self.game.network.connected:
            data = {
                'player': [self.player_x, self.player_y],  # Posição atual
                'rio_centro': self.background.centro_rio_x,  # Posição do rio
                'seed': self.background.tree_manager.random_seed,  # Seed aleatória
                'invincible': self.invincible_timer_j1 if self.is_host else self.invincible_timer_j2,  # Timer de invencibilidade
                'type': 'game_update'  # Tipo de mensagem
            }
            self.game.network.send(data)  # Envia os dados

    # Método para receber dados da rede
    def receive_data(self):
        # Define a função receive_data como método da classe (self é a referência ao objeto)
        
        if self.is_multiplayer and isinstance(self.game.network.data, dict):
            # Verifica se o jogo está no modo multiplayer E se os dados recebidos da rede são um dicionário
            
            data = self.game.network.data
            # Armazena os dados recebidos da rede na variável local 'data' para facilitar acesso
            
            try:
                # Inicia um bloco try para capturar possíveis erros no processamento dos dados
                
                # Atualiza posição do outro jogador
                self.player2_x, self.player2_y = data['player']
                # Extrai as coordenadas x e y do outro jogador do dicionário de dados
                # e atualiza as posições do player2 no jogo local
                
                # Sincroniza temporizador de invencibilidade
                if self.is_host:    
                    # Verifica se esta instância é o host (jogador 1)
                    self.invincible_timer_j2 = data.get('invincible', 0)
                    # Host recebe o timer de invencibilidade do cliente (jogador 2)
                    # Usa .get() para evitar KeyError, retornando 0 se 'invincible' não existir
                else:
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
                    
                # Sincroniza seed aleatória se necessário
                if 'seed' in data and data['seed'] != self.background.tree_manager.random_seed:
                    # Verifica se existe uma seed nos dados E se é diferente da seed atual
                    self.background.tree_manager.random_seed = data['seed']
                    # Atualiza a seed aleatória no gerenciador de árvores
                    random.seed(data['seed'])
                    # Define a seed global do módulo random para manter consistência
                    self.background.tree_manager.reset_arvores()
                    # Reinicia as árvores com a nova seed para sincronizar a geração aleatória
                    
            except (KeyError, TypeError):
                # Captura exceções caso haja erro ao acessar chaves do dicionário ou tipos incorretos
                print("Erro na sincronização dos dados")
                # Imprime mensagem de erro (poderia ser tratado de forma mais robusta em produção)

    # Método para desenhar o jogo
    def draw(self):
        pyxel.cls(COLOR_BG)                                   # Limpa a tela com a cor de fundo definida
        
        self.background.draw()                                # Desenha o cenário de fundo

        # Lógica de piscar durante invencibilidade
        should_draw_j1 = (self.invincible_timer_j1 // 5) % 2 == 0 if self.invincible_timer_j1 > 0 else True  # Define se o jogador 1 deve piscar (quando invencível)
        should_draw_j2 = (self.invincible_timer_j2 // 5) % 2 == 0 if self.invincible_timer_j2 > 0 else True  # Define se o jogador 2 deve piscar (quando invencível)

        # Renderização do jogador 1
        if self.is_multiplayer and should_draw_j1:             # Verifica se é multiplayer E se deve desenhar o jogador 1
            if self.is_host:                                  # Se for o host (jogador 1)
                pyxel.blt(self.player_x, self.player_y, 0, 32, 0, PLAYER_WIDTH, PLAYER_HEIGHT, colkey=0)  # Desenha o avião (host)
                pyxel.text(10, 40, f"Suas Vidas: {self.vida_jogador1}", 0)  # Mostra contador de vidas do host
            else:                                              # Se for o cliente
                pyxel.blt(self.player2_x, self.player2_y, 0, 32, 0, PLAYER_WIDTH, PLAYER_HEIGHT, colkey=0)  # Desenha o avião do host na posição recebida

        # Renderização do jogador 2
        if self.is_multiplayer and should_draw_j2:             # Verifica se é multiplayer E se deve desenhar o jogador 2
            if self.is_host:                                  # Se for o host
                pyxel.blt(self.player2_x, self.player2_y, 0, 48, 0, PLAYER_WIDTH, PLAYER_HEIGHT, colkey=0)  # Desenha o helicóptero do cliente
            else:                                              # Se for o cliente
                pyxel.blt(self.player_x, self.player_y, 0, 48, 0, PLAYER_WIDTH, PLAYER_HEIGHT, colkey=0)  # Desenha o próprio helicóptero (cliente)
                pyxel.text(10, 60, f"Suas Vidas: {self.vida_jogador2}", 1)  # Mostra contador de vidas do cliente

        # Modo singleplayer
        if not self.is_multiplayer and should_draw_j1:         # Se não for multiplayer E deve desenhar o jogador
            pyxel.blt(self.player_x, self.player_y, 0, 32, 0, PLAYER_WIDTH, PLAYER_HEIGHT, colkey=0)  # Desenha o jogador único
            pyxel.text(10, 40, f"Suas Vidas: {self.vida_jogador1}", 0)  # Mostra contador de vidas

        # Debug: mostra posições
        if self.is_host:                                       # Se for o host
            pyxel.text(10, 20, f"Host: {self.player_x},{self.player_y}", 7)  # Mostra posição do host
            pyxel.text(10, 30, f"Cliente: {self.player2_x},{self.player2_y}", 7)  # Mostra posição do cliente
        else:                                                  # Se for o cliente
            pyxel.text(10, 20, f"Host: {self.player2_x},{self.player2_y}", 7)  # Mostra posição do host
            pyxel.text(10, 30, f"Cliente: {self.player_x},{self.player_y}", 7)  # Mostra posição do cliente

        # Status da conexão
        if self.game.network.connected:                        # Verifica se há conexão de rede
            pyxel.text(10, 10, "Multiplayer - Conectado", 0)   # Mostra status "Conectado"
        else:                                                  # Se não estiver conectado
            pyxel.text(10, 10, "Multiplayer - Desconectado", 0)  # Mostra status "Desconectado"

        # Debug: hitbox das árvores
        for arvore in self.background.tree_manager.arvores:    # Itera por todas as árvores
            arv_left, arv_top, arv_right, arv_bottom = arvore.hitbox  # Obtém coordenadas da hitbox
            pyxel.rectb(arv_left, arv_top, arv_right - arv_left, arv_bottom - arv_top, 8)  # Desenha retângulo da hitbox (para debug)

## Classe que gerencia o cenário do jogo (rio e margens)
class Background:
    def __init__(self, is_host=False):  # Construtor da classe Background
        self.is_host = is_host  # Define se esta instância é o host (controla o rio)
        
        # Configurações do rio
        self.velocidade_scroll = 1  # Velocidade de movimento vertical do cenário
        self.deslocamento = 0  # Acumulador de deslocamento vertical
        self.largura_rio = 45  # Largura fixa do rio em pixels
        self.cor_borda = 15  # Cor branca para as margens do rio (paleta Pyxel)
        self.centro_rio_x = pyxel.width / 2  # Posição horizontal inicial do centro do rio
        self.target_centro_x = self.centro_rio_x  # Alvo para animação suave das curvas
        self.curve_speed = 1.0  # Velocidade de ajuste das curvas do rio
        
        # Histórico de posições do rio (armazena posições anteriores para desenho)
        self.centros_hist = deque([self.centro_rio_x] * pyxel.height, maxlen=pyxel.height)
        
        # Pontos brancos no rio (detalhes visuais - padrão de ondulação)
        self.pontos_brancos = [(3, 2), (10, 5), (15, 8), (25, 3), (30, 7), 
                             (5, 14), (20, 12), (28, 16), (12, 20), (18, 18)]
        
        # Gerenciador de árvores (instância que controla a geração e desenho das árvores)
        self.tree_manager = TreeManager(self)

    # Calcula as margens do rio na posição Y especificada
    def obter_margens_rio(self, screen_y):  # Recebe uma coordenada vertical (y)
        centro = self.centros_hist[screen_y]  # Obtém a posição horizontal do centro do rio naquela linha
        meia = self.largura_rio / 2  # Calcula metade da largura do rio
        return centro - meia, centro + meia  # Retorna posições esquerda e direita das margens

    # Atualiza a posição do rio (chamado a cada frame)
    def update(self):
        # Controles para curvar o rio (teclas 1 e 2 - apenas host pode controlar)
        if (pyxel.btnp(pyxel.KEY_1) and self.is_host):  # Tecla 1 pressionada pelo host - curva para direita
            self.target_centro_x = min(self.target_centro_x + 30, pyxel.width - self.largura_rio/2)  # Limita ao limite direito da tela
        if (pyxel.btnp(pyxel.KEY_2) and self.is_host):  # Tecla 2 pressionada pelo host - curva para esquerda
            self.target_centro_x = max(self.target_centro_x - 30, self.largura_rio/2)  # Limita ao limite esquerdo da tela

        # Animação suave do rio (interpolação para movimento fluido)
        diff = self.target_centro_x - self.centro_rio_x  # Diferença entre alvo e posição atual
        if abs(diff) > self.curve_speed:  # Se a diferença for maior que a velocidade de ajuste
            self.centro_rio_x += self.curve_speed * (1 if diff > 0 else -1)  # Move gradualmente
        else:
            self.centro_rio_x = self.target_centro_x  # Chegou no alvo

        # Atualiza histórico de posições (para desenho consistente)
        self.centros_hist.appendleft(self.centro_rio_x)  # Adiciona nova posição no início
        self.deslocamento += self.velocidade_scroll  # Incrementa deslocamento vertical

        # Atualiza árvores (chama o gerenciador para mover as árvores)
        self.tree_manager.update_arvores(self.velocidade_scroll)

    # Desenha o rio e suas margens (chamado a cada frame)
    def draw(self):
        pyxel.rect(0, 0, pyxel.width, pyxel.height, 9)  # Preenche toda tela com azul (água)
        
        # Desenha margens do rio linha por linha
        for screen_y in range(pyxel.height):  # Itera por cada linha vertical da tela
            esq, dir = self.obter_margens_rio(screen_y)  # Obtém posições das margens
            
            # Bordas das margens (efeito de profundidade com 4 linhas)
            for i in range(4):  # Desenha linhas de contorno
                pyxel.line(int(esq)-i, screen_y, int(esq), screen_y, self.cor_borda)  # Margem esquerda
                pyxel.line(int(dir), screen_y, int(dir)+i, screen_y, self.cor_borda)  # Margem direita
            
            # Água do rio (linha central entre as margens)
            pyxel.line(int(esq), screen_y, int(dir), screen_y, 12)  # Azul mais claro
            
            # Detalhes visuais (pontos brancos que simulam reflexos/ondas)
            for dx, dy in self.pontos_brancos:  # Para cada ponto no padrão definido
                pattern_y = (screen_y - self.deslocamento + dy) % 24  # Calcula posição com deslocamento
                if pattern_y == dy:  # Se estiver na posição correta do padrão
                    x = esq + (dx % (dir - esq))  # Calcula posição horizontal dentro do rio
                    if esq < x < dir:  # Verifica se está dentro das margens
                        pyxel.pset(int(x), screen_y, 7)  # Desenha ponto branco
        
        # Desenha árvores (delega para o gerenciador de árvores)
        self.tree_manager.draw_arvores()