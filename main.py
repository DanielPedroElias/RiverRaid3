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
import pyxel # Engine utilizada no jogo
from network import NetworkManager # Importa a classe NetworkManager para gerenciar conexoes de rede
from states import MenuState # Importa a classe do menu principal
from config import * # Importa todas as configuracoes definidas em config.py

# Seguindo as recomendacoes do github oficial do Pyxel de encapsular o codigo do Pyxel em uma classe:
# Classe principal do jogo
class Game:
    # Construtor
    # Inicializa o jogo: configuracoes, rede e primeiro estado
    def __init__(self):
        self.is_fullscreen = FULLSCREAM # Variavel que guarda se o jogo esta ou nao em tela cheia

        # Inicializa o estado inicial como sendo o menu principal
        self.current_state = MenuState(self) # Chama o menu principal passando a instancia do jogo e recebe o estado atual (que eh o proprio menu principal)
        self.previous_state = None  # Usado para tela de pause do jogo (se o usuario pausar, o jogo guarda o estado anterior do jogo, que era o proprio jogo)
        self.network = NetworkManager(NETWORK_PORT) # Inicializa a conexao passando a porta que a aplicacao vai usar
        
        # Inicializa configuracoes iniciais do jogo
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT,     # Tamanho do Jogo
                  title="River Raid 3",             # Titulo
                  fps=FPS,                          # FPS em que o jogo ira funcionar
                  quit_key=pyxel.KEY_NONE           # Define nenhuma tecla para fechar o jogo, pois o proprio codigo ja faz esse pedido (evita de fechar acidentalmente)
        )
        pyxel.fullscreen(self.is_fullscreen) # Define se o jogo vai abrir em tela cheia ou nao
        pyxel.load("artes.pyxres")  
        pyxel.run(self.update, self.draw) # Inicializa o jogo

    
    # Troca o estado atual do jogo (menus, o proprio jogo, etc.)
    def change_state(self, new_state):
        # Estado atual do jogo recebe o novo estado se houver alguma troca de estado
        self.current_state = new_state
    
    # Atualiza a logica do jogo a cada frame
    def update(self):
        # Verifica tecla F11 para alternar tela cheia
        if pyxel.btnp(pyxel.KEY_F11):
            self.is_fullscreen = not self.is_fullscreen # Pega o contrario do estado atual
            pyxel.fullscreen(self.is_fullscreen) # Fica ou nao em tela cheia

        # Chama o metodo "update" do estado atual em que o jogo estah (states.py)
        self.current_state.update()
    
    # Desenha todos os elementos na tela a cada frame
    def draw(self):
        # Chama o metodo "draw" do estado atual em que o jogo estah (states.py)
        self.current_state.draw()
        

# Executa o jogo
Game()