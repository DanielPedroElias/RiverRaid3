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
        self.max_arvores = 40  
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
                return

        # 2) fallback: coloca à esquerda ou à direita, mas sempre fora do rio
        y = random.randint(-pyxel.height, 0)
        # distância extra para não grudar na margem
        margem = self.distancia_rio + self.tree_w  
        # se couber mais espaço à esquerda, usa ali; senão, na direita
        if esq0 - margem >= self.margem_lateral:
            arvore.x = int(esq0 - margem)
        else:
            arvore.x = int(dir0 + self.distancia_rio)
        arvore.y = y


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
        arv_left, arv_top, arv_right, arv_bottom = arvore.hitbox
        # Teste de interseção entre retângulos
        if (jogador_right > arv_left and
            jogador_left < arv_right and
            jogador_bottom > arv_top and
            jogador_top < arv_bottom):
            colisoes += 1  # Incrementa contador
            print(f"{player_name} colidiu com uma árvore! (-1 vida)")
    
    return colisoes  # Retorna total de colisões