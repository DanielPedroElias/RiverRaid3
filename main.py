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
### Para executar: pyxel run main.py

# ============================================================================================================

# Bibliotecas
from pyxel import * # Importa o pyxel (o ideal eh importar cada modulo separadamente)

init(160,120) # Cria uma tela de x por y polegadas
# load ("my_resource.pyxres") # Carrega banco de pixel arts
# Clear screen -> cls
cls(5) # Limpa a tela e coloca ela toda numa cor especifico
# show() # Mostra a tela (so utiliza para imagem estatica)


# Posicoes globais
# retangulo
x_ret = 10
y_ret = 10

# Circulo
player_x_circ = 50
player_y_circ = 50


# Funcao para colocar os status do jogo
# que vai ser chamada de tempo em tempo por segundo
# Eh chamado automaticamente pela biblioteca
def update():
    global x_ret, player_x_circ, player_y_circ # Usa a variavel global para posicoes

    x_ret = x_ret + 0.01 # Move o retangulo para a direita de x em x tempo

    # Movimentacao:
    if btn(KEY_D): # Direita
        player_x_circ += 1

    if btn(KEY_A): # Esquerda
        player_x_circ -= 1
    
    if btn(KEY_S): # Baixo
        player_y_circ += 1
    
    if btn(KEY_W): # Cima
        player_y_circ -= 1





# Funcao para desenhar algo na tela
# Essa funcao eh chamada por um certo numero de vezes por segundo
def draw():
    cls(5) # Limpa a tela e recria os objetos toda vez que eh chamado (para nao pintar a tela)
    rect(x_ret, y_ret, 20, 20, COLOR_RED) # Desenha um retangulo na tela (posicao 10x10. altura:20, largura:20, cor:vermelha)
    circ(30, 30, 10, COLOR_GREEN) # Desenha um circulo na tela  (posicao 30x30, raio:10, cor:Verde)
    rect(player_x_circ, player_y_circ, 10, 10, COLOR_ORANGE) # Player (teste)

    # Carrega imagem do pyxel edit
    # blt(player_x_circ, player_y_circ, 0, 0, 0, 16, 16, 0)
    


run(update,draw)