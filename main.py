### Redes de Computadores
### Professor: Maxwell
### Alunos: Daniel Pedro Elias dos Santos e Gabriel Neves Silveira
###
### Arquivo principal que coordena todo o jogo
### Para mais detalhes sobre o projeto, consulte o arquivo "README.md" e os arquivos do codigo fonte
###
### Para executar: 
### 1. pyxel run main.py
### OU
### 2. make

# ============================================================================================================

# Bibliotecas
import pyxel
from network import NetworkManager
from states import MenuState, GameState, MultiplayerMenuState
from config import *

# Seguindo as recomendacoes do github oficial do Pyxel de encapsular o codigo do Pyxel em uma classe:
# Classe principal do jogo
class Game:
    # Construtor
    # Inicializa o jogo: configuracoes, rede e primeiro estado
    def __init__(self):
        self.is_fullscreen = True # Variavel que guarda se o jogo esta ou nao em tela cheia

        # Inicializa o estado inicial como sendo o menu principal
        self.current_state = MenuState(self) # Chama o menu principal passando a instancia do jogo e recebe o estado atual (que eh o proprio menu principal)
        self.previous_state = None  # Usado para tela de pause do jogo (se o usuario pausar, o jogo guarda o estado atual do jogo)
        self.network = NetworkManager(NETWORK_PORT) # Inicializa a conexao passando a porta que a aplicacao vai usar
        
        # Inicializa configuracoes iniciais do jogo
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, 
                  title="River Raid 3", 
                  fps=FPS,
                  quit_key=pyxel.KEY_NONE) # O proprio codigo pede para o pyxel fechar (para o usuario nao fechar acidentalmente)
        pyxel.fullscreen(self.is_fullscreen)
        pyxel.run(self.update, self.draw) # Inicializa o jogo
        pyxel.text(10, 10, str(id(self.game)), 7)  # Mostra ID da instância
    
    # Troca o estado atual do jogo (menus, jogo em si)
    def change_state(self, new_state):
        # Estado atual do jogo recebe o novo estado (seja menu, ou o jogo mesmo)
        self.current_state = new_state
    
    # Atualiza a logica do jogo a cada frame
    def update(self):
        # Verifica tecla F11 para alternar tela cheia
        if pyxel.btnp(pyxel.KEY_F11):
            self.is_fullscreen = not self.is_fullscreen # Pega o contrario do estado atual
            pyxel.fullscreen(self.is_fullscreen) # Fica ou nao em tela cheia

        # Chama o metodo "update" da classe "MenuState" (states.py) para verificar qual o estado atual
        self.current_state.update()
    
    # Desenha todos os elementos na tela a cada frame
    def draw(self):
        # Chama o metodo "draw" da classe "MenuState" (states.py) para atualizar o que vai ser desenhado na tela
        self.current_state.draw()
        


# Executa o jogo
Game()