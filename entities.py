### Modulo de entidades do jogo. Responsavel por:
### - Definir classes de entidades (bala, inimigo, item, etc.)
### - Gerenciar logica de update() e draw() de cada entidade

import time
import pyxel
from config import *

# Classe base para todas as entidades do jogo (interface informal)
class Entity:
    # Cada entidade deve ter:
    # - x, y: coordenadas
    # - alive: se ainda esta ativa
    # - update(): logica por frame
    # - draw(): renderizacao por frame

    # Construtor
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = True


    # Atualiza a logica da entidade.
    # Deve ser sobrescrito nas subclasses.
    def update(self):
        pass

    # Desenha a entidade.
    # Deve ser sobrescrito nas subclasses.
    def draw(self):
        pass

# Classe que implementa o tiro disparado pelo aviao (Vai para cima a cada frame)
class Bullet(Entity):
    # Construtor
    def __init__(self, x, y, dy=-BULLET_SPEED): # BULLET_SPEED estah em pixels/frame
        # Herda da classe Entity e inicializa posicao (x, y)
        super().__init__(x, y)

        # dy = velocidade vertical (negativo = para cima)
        self.dy = dy
    
    # Atualiza a posicao do tiro e verifica se ele saiu da tela
    def update(self):
        self.y += self.dy # Atualiza a posicao do tiro (usando velocidade por FRAME)

        # Verifica se o tiro saiu da parte superior da tela
        #   Se (posicao 'Y' + altura do tiro) < 0 (fora da tela)
        if self.y + BULLET_HEIGHT < 0:
            self.alive = False # Marca o tiro para ser removido

    # Desenha o retangulo que representa o tiro
    def draw(self):
        pyxel.rect(self.x, self.y, BULLET_WIDTH, BULLET_HEIGHT, COLOR_BULLET)

# Classe que implementa o tiro disparado pelo aviao (Vai para cima a cada frame)
class RemoteBullet(Entity):
    # Construtor
    def __init__(self, x, y, spawn_time):
        # Herda da classe Entity e inicializa posicao (x, y)
        super().__init__(x, y)

        # Guarda a posicao Y inicial do tiro
        self.initial_y = y
        
        # Converte velocidade para pixels/SEGUNDO:
        self.speed = -BULLET_SPEED * FPS # px/frame * frames/sec = px/sec
        self.spawn_time = spawn_time # Momento exato do tiro (timestamp em segundos)

    # Atualiza a posicao do tiro e verifica se ele saiu da tela
    def update(self):
        # Calcula idade do tiro em SEGUNDOS
        age = time.time() - self.spawn_time # Segundos que o tiro estah vivo

        # Atualiza a posicao em 'Y' baseada no TEMPO PASSADO:
        # y = posicao_inicial + (velocidade * tempo)
        self.y = self.initial_y + (self.speed * age)

        # Verifica se o tiro saiu da tela (usa a mesma logica do tiro local)
        if self.y + BULLET_HEIGHT < 0:
            self.alive = False

    # Desenha o retangulo que representa o tiro
    def draw(self):
        pyxel.rect(self.x, self.y, BULLET_WIDTH, BULLET_HEIGHT, COLOR_BULLET)


# TODO: Implementar a classe para geracao de inimigos
class Enemy(Entity):
    # Entidade de inimigo. (Implementar logica de movimento e colisoes)
    def __init__(self, x, y, **kwargs):
        super().__init__(x, y)
        # adicionar atributos como velocidade, vida, etc.

    def update(self):
        # implementar movimento do inimigo
        pass

    def draw(self):
        # desenhar o inimigo
        # exemplo generico:
        # pyxel.rect(self.x, self.y, ENEMY_WIDTH, ENEMY_HEIGHT, COLOR_ENEMY)
        pass

# TODO: Implementar classe para gasolina
class Gasoline(Entity):
    # Entidade de item/collectable. (Implementar efeitos ao coletar)
    def __init__(self, x, y, **kwargs):
        super().__init__(x, y)
        # atributos de tipo de item, valor, etc.

    def update(self):
        # implementar movimento/gravitacao se necessario
        pass

    def draw(self):
        # desenhar o item
        # exemplo generico:
        # pyxel.rect(self.x, self.y, ITEM_WIDTH, ITEM_HEIGHT, COLOR_ITEM)
        pass
