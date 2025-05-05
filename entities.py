# Importações necessárias para o módulo
import pyxel          # Biblioteca para criação do jogo
import random         # Para geração de números aleatórios
from collections import deque  # Para estrutura de dados eficiente
from config import *  # Importa constantes do jogo

class Tree:
    """Classe que representa uma árvore no jogo"""
    def __init__(self, x, y):
        # Posição inicial da árvore
        self.x = x  # Coordenada X no mapa
        self.y = y  # Coordenada Y no mapa
        
        # Dimensões do sprite da árvore
        self.width = 16   # Largura do sprite
        self.height = 16  # Altura do sprite

        self.visible = True   # ← flag de visibilidade
        self.sprite_type = random.choice([0, 1])  # 0 = primeira árvore (0,0), 1 = segunda (16,0)

    def to_dict(self):
        return {
            'x': self.x, 
            'y': self.y, 
            'visible': self.visible,
            'sprite_type': self.sprite_type  # ← Novo
        }

    @property
    def hitbox(self):
        """Retorna a área de colisão da árvore (menor que o sprite visual)"""
        return (
            self.x + 2,          # Left: deslocada 2px para dentro
            self.y + 2,          # Top: deslocada 2px para dentro
            self.x + self.width - 2,  # Right: 2px antes da borda direita
            self.y + self.height - 2   # Bottom: 2px antes da borda inferior
        )

class TreeManager:
    """Gerenciador responsável por criar e controlar todas as árvores do jogo"""
    def __init__(self, background):
        # Referência ao background para verificar margens do rio
        self.background = background  
        # Distância mínima entre árvores e o rio
        self.distancia_rio = 2  
        # Margem lateral da tela onde árvores podem aparecer
        self.margem_lateral = 2  
        # Número máximo de árvores no jogo
        self.max_arvores = 20  
        # Largura do sprite da árvore
        self.tree_w = 16  
        # Lista de árvores ativas
        self.arvores = [self.criar_arvore_fora_tela() for _ in range(self.max_arvores)]  
        # Distância mínima entre árvores
        self.distancia_minima = 12  
        # Seed aleatória para geração consistente
        self.random_seed = random.randint(0, 1000000)  
        random.seed(self.random_seed)  # Define a seed para o random
    
    def get_tree_states(self):
        return [tree.to_dict() for tree in self.arvores]

    def set_tree_states(self, tree_states):
        self.arvores = []
        for state in tree_states:
            tree = Tree(state['x'], state['y'])
            tree.visible = state['visible']
            tree.sprite_type = state['sprite_type']  # ← Novo
            self.arvores.append(tree)

            
    def reset_arvores(self):
        """Reinicia todas as árvores usando a mesma seed aleatória"""
        random.seed(self.random_seed)
        self.arvores = [self.criar_arvore_fora_tela() for _ in range(self.max_arvores)]
        
    def _arvore_valida(self, nova_arvore):
        """Verifica se a nova árvore não está muito próxima das existentes"""
        for arv in self.arvores:
            # Checa distância mínima entre árvores
            if self._calcular_distancia(arv, nova_arvore) < self.distancia_minima:
                return False
        return True
    
    def _calcular_distancia(self, arv1, arv2):
        """Calcula distância euclidiana entre os centros das hitboxes"""
        # Centro X da primeira árvore
        x1 = (arv1.hitbox[0] + arv1.hitbox[2]) / 2  
        # Centro Y da primeira árvore
        y1 = (arv1.hitbox[1] + arv1.hitbox[3]) / 2  
        # Centro X da segunda árvore
        x2 = (arv2.hitbox[0] + arv2.hitbox[2]) / 2  
        # Centro Y da segunda árvore
        y2 = (arv2.hitbox[1] + arv2.hitbox[3]) / 2  
        # Fórmula de distância entre dois pontos
        return ((x2 - x1)**2 + (y2 - y1)**2)**0.5  
    
    def criar_arvore_fora_tela(self):
        """Cria nova árvore posicionada acima da tela visível"""
        # Posição Y aleatória acima da tela
        y = random.randint(-pyxel.height, 0)  
        # Obtém margens do rio no topo da tela
        esq0, dir0 = self.background.obter_margens_rio(0)  
        # Cria árvore fora do rio
        return self._novo_tree_fora(esq0, dir0, y)  

    def _novo_tree_fora(self, esq, dir, y):
        """Cria nova árvore garantidamente fora das margens do rio"""
        # Limites para árvores à esquerda do rio
        left_min = self.margem_lateral  
        left_max = int(esq - self.distancia_rio - self.tree_w)  
        # Limites para árvores à direita do rio
        right_min = int(dir + self.distancia_rio)  
        right_max = pyxel.width - self.margem_lateral - self.tree_w  

        # Loop até encontrar posição válida
        while True:
            # Escolhe aleatoriamente entre esquerda/direita (50% de chance)
            if left_min <= left_max and random.random() < 0.5:
                x = random.randint(left_min, left_max)  # Posição à esquerda
            elif right_min <= right_max:
                x = random.randint(right_min, right_max)  # Posição à direita
            else:
                x = self.margem_lateral  # Fallback

            # Verifica se está fora do rio
            if not (esq < x < dir):
                return Tree(x, y)  
            
            # Verifica colisão com outras árvores
            nova_arvore = Tree(x, y)
            if self._arvore_valida(nova_arvore):
                return nova_arvore

    def reposicionar_arvore(self, arvore):
        """Tenta reposicionar até 5 vezes; se falhar, faz fallback na beira do rio."""
        esq0, dir0 = self.background.obter_margens_rio(0)
        # 1) tenta 5 vezes numa posição aleatória
        for _ in range(5):
            y = random.randint(-pyxel.height, 0)
            nova = self._novo_tree_fora(esq0, dir0, y)
            if self._arvore_valida(nova):
                arvore.x, arvore.y = nova.x, nova.y
                arvore.visible = True  # ← Resetar visibilidade aqui
                return

        # 2) fallback: coloca à esquerda ou à direita, mas sempre fora do rio
        y = random.randint(-pyxel.height, 0)
        margem = self.distancia_rio + self.tree_w
        if esq0 - margem >= self.margem_lateral:
            arvore.x = int(esq0 - margem)
        else:
            arvore.x = int(dir0 + self.distancia_rio)
        arvore.y = y
        arvore.visible = True  # ← Garantir visibilidade ao reposicionar


    def update_arvores(self, velocidade_scroll):
        for arvore in self.arvores:
            arvore.y += velocidade_scroll

            # se saiu de baixo, reposiciona
            if arvore.y > pyxel.height:
                self.reposicionar_arvore(arvore)
                continue

            # se entrou no rio, reposiciona só uma vez
            screen_y = min(max(int(arvore.y), 0), pyxel.height - 1)
            esq, dir = self.background.obter_margens_rio(screen_y)
            if esq < arvore.x < dir:
                self.reposicionar_arvore(arvore)
                

    # Modifique o draw_arvores para usar sprites diferentes:
    def draw_arvores(self):
        """Desenha todas as árvores visíveis na tela"""
        for arvore in self.arvores:
            if not arvore.visible:
                continue

            # Escolhe o sprite baseado no tipo
            u = 0 if arvore.sprite_type == 0 else 16  # 0 ou 16 no eixo X
            v = 0  # Mesma coordenada Y para ambos
            
            pyxel.blt(
                arvore.x, arvore.y, 0,
                u, v,  # Coordenadas do sprite
                self.tree_w, self.tree_w,
                0
            )

def check_tree_collision(player_x, player_y, arvores, player_name):
    """Verifica colisões entre jogador e árvores"""
    # Define hitbox do jogador (menor que o sprite visual)
    jogador_left = player_x + 2  # Left: 2px para dentro
    jogador_right = player_x + PLAYER_WIDTH - 2  # Right: 2px para dentro
    jogador_top = player_y + 2  # Top: 2px para dentro
    jogador_bottom = player_y + PLAYER_HEIGHT - 2  # Bottom: 2px para dentro

    colisoes = 0  # Contador de colisões neste frame
    
    # Verifica colisão com cada árvore
    for arvore in arvores:
        if not arvore.visible:
           continue

        arv_left, arv_top, arv_right, arv_bottom = arvore.hitbox
        # Teste de interseção entre retângulos
        if (jogador_right > arv_left and
            jogador_left < arv_right and
            jogador_bottom > arv_top and
            jogador_top < arv_bottom):
            colisoes += 1  # Incrementa contador
            print(f"{player_name} colidiu com uma árvore! (-1 vida)")
    
    return colisoes  # Retorna total de colisões


class Shot:
    """Classe que representa um tiro disparado por um jogador."""
    def __init__(self, x, y, vy=-2):
        # posição inicial
        self.x = x
        self.y = y
        # velocidade vertical (vai para cima, por isso negativo)
        self.vy = vy
        # dimensões do tiro (ajuste a gosto)
        self.width = 2
        self.height = 4
        # cor do tiro (branco)
        self.color = 7

    def update(self):
        """Move o tiro."""
        self.y += self.vy

    def is_off_screen(self):
        """Retorna True se o tiro saiu da tela."""
        return self.y + self.height < 0

    def draw(self):
        """Desenha o tiro."""
        pyxel.rect(self.x, self.y, self.width, self.height, self.color)

    def to_dict(self):
        """Serializa estado para enviar pela rede."""
        return {'x': self.x, 'y': self.y, 'vy': self.vy}

    @classmethod
    def from_dict(cls, data):
        """Reconstrói um Shot a partir de dicionário."""
        return cls(data['x'], data['y'], data.get('vy', -2))
    

class Explosion:
    """Uma explosão que vive por alguns frames e depois some."""
    def __init__(self, x, y, tile_u, tile_v, width, height, duration=5):
        # posição da explosão (top‑left)
        self.x = x
        self.y = y
        # coordenadas do frame no tileset (u, v) e tamanho (w,h)
        self.tile_u = tile_u
        self.tile_v = tile_v
        self.width = width
        self.height = height
        # quantos updates ela ainda vai viver
        self.timer = duration

    def update(self):
        # decrementa o timer; quando chega a zero, indica que deve ser removida
        self.timer -= 1

    def draw(self):
        # só desenha enquanto timer > 0
        if self.timer > 0:
            # blt(x, y, img_bank, u, v, w, h, [colkey])
            pyxel.blt(self.x, self.y, 0, self.tile_u, self.tile_v, self.width, self.height, colkey=pyxel.COLOR_BLACK)

    def is_dead(self):
        return self.timer <= 0

    def to_dict(self):
           return {
               'x': self.x,
               'y': self.y,
               'tile_u': self.tile_u,
               'tile_v': self.tile_v,
               'width': self.width,
               'height': self.height,
               'timer': self.timer,
           }    
    
    @classmethod
    def from_dict(cls, data):
        exp = cls(
            data['x'], data['y'],
            data['tile_u'], data['tile_v'],
            data['width'], data['height'],
            duration=data['timer']
        )
        return exp
    

class Boat:
    """Classe que representa um barco inimigo que navega pelo rio."""
    def __init__(self, x, y, vy=1):
        self.x = x
        self.y = y
        self.vy = vy              # velocidade para baixo (scroll relativo)
        self.width = 16
        self.height = 16
        self.visible = True

    @property
    def hitbox(self):
        return (
            self.x + 1,
            self.y + 1,
            self.x + self.width - 1,
            self.y + self.height - 1,
        )

    def update(self):
        self.y += self.vy

    def draw(self):
        if self.visible:
            # sprite de barco em (32,16) no banco 0
            pyxel.blt(self.x, self.y, 0, 32, 16, self.width, self.height, colkey=0)

    def to_dict(self):
        return {'x': self.x, 'y': self.y, 'vy': self.vy, 'visible': self.visible}

    @classmethod
    def from_dict(cls, data):
        b = cls(data['x'], data['y'], data.get('vy', 1))
        b.visible = data.get('visible', True)
        return b


class BoatManager:
    """Gerencia criação, atualização e reposicionamento de barcos dentro do rio,
       evitando que nasçam muito próximos uns dos outros."""
    def __init__(self, background, max_boats=10, spawn_chance=0.02, min_spawn_distance=24):
        self.background = background
        self.max_boats = max_boats
        self.spawn_chance = spawn_chance    # chance por pixel de scroll
        self.min_spawn_distance = min_spawn_distance
        self.boats = []
        self._last_deslocamento = background.deslocamento

    def _can_spawn_at(self, x, y):
        """Retorna False se existir outro barco muito perto de (x,y)."""
        for b in self.boats:
            # distancia horizontal e vertical
            if abs(b.x - x) < self.min_spawn_distance and abs(b.y - y) < self.min_spawn_distance:
                return False
        return True

    def update(self):

        if self.background.animating_to_center:
            self.spawn_chance = 0.8
        else:
           self.spawn_chance = 0.02

        # printa a spawn chance
        # print(f"Spawn chance: {self.spawn_chance:.2f}")

        # 1) move todos
        for b in self.boats:
            b.update()

        if (self.background.is_host or not self.background.is_multiplayer):
        # 2) descarta os que saíram
            self.boats = [b for b in self.boats if b.y <= pyxel.height]

            # 3) spawn “por linha”, testando distância mínima
            delta = int(self.background.deslocamento) - int(self._last_deslocamento)
            for _ in range(delta):
                if len(self.boats) < self.max_boats and random.random() < self.spawn_chance:
                    esq, dir = self.background.obter_margens_rio(0)
                    largura_disponivel = int(dir - esq - 16)
                    if largura_disponivel > 0:
                        # tente até N vezes encontrar um x válido
                        for _ in range(5):
                            x = random.randint(int(esq), int(dir - 16))
                            y = -16
                            if self._can_spawn_at(x, y):
                                self.boats.append(Boat(x, y=y))
                                break
                            
        self._last_deslocamento = self.background.deslocamento

    def draw(self):
        for b in self.boats:
            b.draw()

    def get_states(self):
        return [b.to_dict() for b in self.boats]

    def set_states(self, states):
        self.boats = [Boat.from_dict(d) for d in states]

class GasolineBomb:
    """Bomba de gasolina que cai do topo e reabastece o jogador."""
    def __init__(self, x, y, vy=1):
        self.x = x
        self.y = y
        self.vy = vy
        self.width = 16
        self.height = 16
        self.visible = True

    @property
    def hitbox(self):
        return (
            self.x + 1,
            self.y + 1,
            self.x + self.width - 1,
            self.y + self.height - 1,
        )

    def update(self):
        self.y += self.vy

    def draw(self):
        if self.visible:
            # sprite em (48,16) no banco 0
            pyxel.blt(self.x, self.y, 0, 48, 16, self.width, self.height, colkey=0)

    def to_dict(self):
        return {'x': self.x, 'y': self.y, 'vy': self.vy, 'visible': self.visible}

    @classmethod
    def from_dict(cls, data):
        b = cls(data['x'], data['y'], data.get('vy', 1))
        b.visible = data.get('visible', True)
        return b


class GasolineBombManager:
    """
    Gera uma bomba de gasolina a cada intervalo fixo, até max_bombs simultâneas,
    evitando spawn sobre árvores ou barcos.
    """
    def __init__(self, background, boat_manager, max_bombs=5, spawn_interval_s=1):
        """
        background: Background (para acessar árvores e largura da tela).
        boat_manager: BoatManager (para checar colisão com barcos).
        max_bombs: número máximo de bombas simultâneas.
        spawn_interval_s: intervalo fixo em segundos entre spawns.
        """
        self.background = background
        self.boat_manager = boat_manager
        self.max_bombs = max_bombs
        self.spawn_interval_frames = int(spawn_interval_s * 60)  # 60 FPS
        self.bombs = []
        self._last_spawn_frame = pyxel.frame_count

    def _can_spawn(self, x, y):
        """Retorna False se (x,y) colidir com outra bomba, árvore ou barco."""
        # colisão com outras bombas
        for b in self.bombs:
            if abs(b.x - x) < b.width and abs(b.y - y) < b.height:
                return False

        # colisão com árvores
        for tree in self.background.tree_manager.arvores:
            if not tree.visible:
                continue
            left, top, right, bottom = tree.hitbox
            if (x + 16 > left and x < right and
                y + 16 > top  and y < bottom):
                return False

        # colisão com barcos
        for boat in self.boat_manager.boats:
            if not boat.visible:
                continue
            left, top, right, bottom = boat.hitbox
            if (x + 16 > left and x < right and
                y + 16 > top  and y < bottom):
                return False

        return True

    def update(self):
        # 1) Move todas as bombas
        for b in self.bombs:
            b.update()

        # 2) Remove as que saíram da tela ou foram destruídas
        self.bombs = [b for b in self.bombs if b.y <= pyxel.height and b.visible]

        # 3) Spawn garantido a cada intervalo
        current = pyxel.frame_count
        if (current - self._last_spawn_frame) >= self.spawn_interval_frames:
            if len(self.bombs) < self.max_bombs:
                # tenta até 5 posições aleatórias
                for _ in range(5):
                    x = random.randint(0, pyxel.width - 16)
                    y = -16
                    if self._can_spawn(x, y):
                        self.bombs.append(GasolineBomb(x, y))
                        break
            self._last_spawn_frame = current

    def draw(self):
        for b in self.bombs:
            b.draw()

    def get_states(self):
        return [b.to_dict() for b in self.bombs]

    def set_states(self, states):
        self.bombs = [GasolineBomb.from_dict(d) for d in states]