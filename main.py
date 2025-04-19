### Redes de Computadores
### Professor: Maxwell
### Alunos: Daniel Pedro Elias dos Santos e Gabriel Neves Silveira
###
### Arquivo com o código fonte do "River Raid 3"
### - Este codigo usa a engine Pyxel para criar a base do jogo.
### - O objetivo eh explorar o funcionamento de comunicacao entre cliente e servidor em um ambiente de jogo
###
### Para mais detalhes sobre o projeto, consulte o arquivo README.md
###
### Para executar: 
### 1. pyxel run main.py
### OU
### 2. make

# ============================================================================================================

# Bibliotecas
import pyxel

# Seguindo as recomendacoes do github oficial do Pyxel de encapsular o codigo do Pyxel em uma classe:
# Classe principal do jogo
class Game:
    # Construtor
    def __init__(self): # self eh o objeto atual
        ## Atributos
        # Tamanho da tela
        self.largura_tela = 160
        self.altura_tela = 120

        # Posicao do jogador
        self._player_x = 50
        self._player_y = 50

        # TODO: Implementar conexao em rede para poder dar utilidade para essa variavel
        # Posicao do segundo jogador
        self._player2_x = 50
        self._player2_y = 50

        # Pontuacao
        self.__pontuacao = 0
        self.tempo_atualizacao = 0 # Contador de tempo
        self.intervalo = (60 * 10) # Intervalo de quantos em quantos quadros a pontuacao vai aumentar (o pyxel roda em 60 FPS, entao 60 FPS equivalem a 1 segundo)


        # Objetos no mapa
        # TODO: Implementar melhor os objetos no mapa
        # Retangulo
        self.ret_x = 30
        self.ret_y = 30

        # Configuracoes iniciais
        pyxel.init(self.largura_tela, self.altura_tela, title="River Raid 3", fps=60, quit_key=pyxel.KEY_ESCAPE)
        pyxel.run(self.update, self.draw)

    # Metodo para colocar os status do jogo
    # que vai ser chamada automaticamente pelo Pyxel de "tempo em tempo por segundo"
    def update(self):
        # Exemplo de movimentacao de um objeto na tela
        self.ret_x += 0.01 # Move o retangulo para a direita de x em x tempo

        # Movimentacao:
        if pyxel.btn(pyxel.KEY_D): # Direita
            self._player_x += 1

        if pyxel.btn(pyxel.KEY_A): # Esquerda
            self._player_x -= 1
        
        if pyxel.btn(pyxel.KEY_S): # Baixo
            self._player_y += 1
        
        if pyxel.btn(pyxel.KEY_W): # Cima
            self._player_y -= 1
        
        ## Trava o player dentro da tela
        # TODO: Trocar "10" pela altura e largura do player
        # Player nao sai da tela no eixo X
        # - min(self._player_x, self.largura_tela - 10): impede que o jogador va alem do lado direito da tela
        # - max(0, ...): impede que o jogador va alem do lado esquerdo da tela
        # - "10" eh a largura do jogador (mudar depois)
        self._player_x = max(0, min(self._player_x, self.largura_tela - 10))

        # Player nao sai da tela no eixo Y
        # - min(self._player_y, self.altura_tela - 10): impede que o jogador va alem da parte inferior da tela
        # - max(0, ...): impede que o jogador va alem da parte superior da tela
        # - "10" eh a altura do jogador (mudar depois)
        self._player_y = max(0, min(self._player_y, self.altura_tela  - 10))


        # TODO: Implementar a pontuacao para o jogador (com base na referencia "River Raid")
        # Alguma coisa acontece e a pontuacao aumenta
        # Atualiza a pontuacao de acordo com o intervalo de tempo pre-definido
        if pyxel.frame_count - self.tempo_atualizacao >= self.intervalo:
            self.__pontuacao += 1
            self.tempo_atualizacao = pyxel.frame_count  # Reseta o tempo de atualizacao

    # Metodo para desenhar algo na tela
    # Esse Metodo eh chamada por um certo numero de vezes por segundo
    def draw(self):
        pyxel.cls(5) # Limpa a tela e recria os objetos toda vez que eh chamado (para nao pintar a tela)
        pyxel.rect(self.ret_x, self.ret_y, 20, 20, pyxel.COLOR_RED) # Desenha um retangulo na tela (posicao 10x10. altura:20, largura:20, cor:vermelha)
        pyxel.circ(30, 30, 10, pyxel.COLOR_GREEN) # Desenha um circulo na tela  (posicao 30x30, raio:10, cor:Verde)
        pyxel.rect(self._player_x, self._player_y, 10, 10, pyxel.COLOR_ORANGE) # Player (teste)
        pyxel.text(5, 5, f"Pontuacao: {self.__pontuacao}", pyxel.COLOR_WHITE) # Pontuacao (teste)

        # Carrega imagem do pyxel edit
        # blt(player_x_circ, player_y_circ, 0, 0, 0, 16, 16, 0)



# Executa o jogo
Game()