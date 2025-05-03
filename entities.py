# entities.py
import pyxel
import random
from collections import deque

from config import *

class Tree:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.width = 16
        self.height = 16

    @property
    def hitbox(self):
        return (
            self.x + 2,
            self.y + 2,
            self.x + self.width - 2,
            self.y + self.height - 2
        )

class TreeManager:
    def __init__(self, background):
        self.background = background
        self.distancia_rio = 2
        self.margem_lateral = 2
        self.max_arvores = 40
        self.tree_w = 16
        self.arvores = [self.criar_arvore_fora_tela() for _ in range(self.max_arvores)]
        self.distancia_minima = 12
        self.random_seed = random.randint(0, 1000000)
        random.seed(self.random_seed)

    def reset_arvores(self):
        random.seed(self.random_seed)
        self.arvores = [self.criar_arvore_fora_tela() for _ in range(self.max_arvores)]
        
    def _arvore_valida(self, nova_arvore):
        """Verifica se a nova árvore não está muito próxima das existentes."""
        for arv in self.arvores:
            if self._calcular_distancia(arv, nova_arvore) < self.distancia_minima:
                return False
        return True
    
    def _calcular_distancia(self, arv1, arv2):
        """Calcula a distância entre os centros das hitboxes."""
        x1 = (arv1.hitbox[0] + arv1.hitbox[2]) / 2
        y1 = (arv1.hitbox[1] + arv1.hitbox[3]) / 2
        x2 = (arv2.hitbox[0] + arv2.hitbox[2]) / 2
        y2 = (arv2.hitbox[1] + arv2.hitbox[3]) / 2
        return ((x2 - x1)**2 + (y2 - y1)**2)**0.5
    
    def criar_arvore_fora_tela(self):
        y = random.randint(-pyxel.height, 0)
        # Margens no ponto em que a árvore aparecerá (screen_y == 0)
        esq0, dir0 = self.background.obter_margens_rio(0)
        return self._novo_tree_fora(esq0, dir0, y)

    def _novo_tree_fora(self, esq, dir, y):
        """Loop até achar x DEFINITIVAMENTE fora de (esq,dir)."""
        left_min  = self.margem_lateral
        left_max  = int(esq - self.distancia_rio - self.tree_w)
        right_min = int(dir + self.distancia_rio)
        right_max = pyxel.width - self.margem_lateral - self.tree_w

        # repete até sair do rio
        while True:
            if left_min <= left_max and random.random() < 0.5:
                x = random.randint(left_min, left_max)
            elif right_min <= right_max:
                x = random.randint(right_min, right_max)
            else:
                x = self.margem_lateral

            if not (esq < x < dir):
                return Tree(x, y)
            
            nova_arvore = Tree(x, y)
            if self._arvore_valida(nova_arvore):
                return nova_arvore

    def reposicionar_arvore(self, arvore):
        """Reposiciona ARVORE até que ela NÃO esteja sobre o rio."""
        while True: 
            # gera um y acima
            y = random.randint(-pyxel.height, 0)
            # obtem margens em screen_y == 0
            esq0, dir0 = self.background.obter_margens_rio(0)

            nova = self._novo_tree_fora(esq0, dir0, y)
            if self._arvore_valida(nova):
                arvore.x, arvore.y = nova.x, nova.y
                break

    def update_arvores(self, velocidade_scroll):
        for arvore in self.arvores:
            arvore.y += velocidade_scroll

            # se passou do bottom, reposiciona
            if arvore.y > pyxel.height:
                self.reposicionar_arvore(arvore)

            # AGORA garanta que ela NÃO esteja dentro do rio em NENHUMA circunstância
            # obtém screen_y válido
            screen_y = min(max(int(arvore.y), 0), pyxel.height - 1)
            esq, dir = self.background.obter_margens_rio(screen_y)

            # reposiciona até ficar fora
            while esq < arvore.x < dir:
                self.reposicionar_arvore(arvore)
                screen_y = min(max(int(arvore.y), 0), pyxel.height - 1)
                esq, dir = self.background.obter_margens_rio(screen_y)

    def draw_arvores(self):
        for arvore in self.arvores:
            if 0 <= arvore.y < pyxel.height:
                pyxel.blt(arvore.x, arvore.y, 0,
                          32, 0,
                          self.tree_w, self.tree_w,
                          0)


def check_tree_collision(player_x, player_y, arvores, player_name):
    jogador_left = player_x + 2
    jogador_right = player_x + PLAYER_WIDTH - 2
    jogador_top = player_y + 2
    jogador_bottom = player_y + PLAYER_HEIGHT - 2

    arvores_para_remover = []
    
    for arvore in arvores:
        arv_left, arv_top, arv_right, arv_bottom = arvore.hitbox
        if (jogador_right > arv_left and
            jogador_left < arv_right and
            jogador_bottom > arv_top and
            jogador_top < arv_bottom):
            arvores_para_remover.append(arvore)
            print(f"{player_name} colidiu com uma árvore!")
    
    for arvore in arvores_para_remover:
        if arvore in arvores:
            arvores.remove(arvore)
    
    return len(arvores_para_remover) > 0