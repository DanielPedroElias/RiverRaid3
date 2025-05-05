### Gerador procedural de mapas. Responsavel por:
### - Criar terreno aleatorio sincronizado
### - Gerenciar scroll automatico
### - Manter consistencia entre jogadores

from collections import deque
import pyxel
from entities import *

# Classe que gerencia o cenário do jogo (rio e margens)
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
        
        
        
        self.tree_manager = TreeManager(self)


        # Novo estado para controle da animação
        self.animating_to_center = False
        self.max_largura = pyxel.width - 30  # Largura máxima igual ao KEY_3

        self.comandos = deque([
            ("WAIT", 300),
            ("KEY_1", 1),   # ← só 1 frame pressionado
            ("WAIT", 150),
            ("KEY_1", 1),
            ("WAIT", 150),
            ("KEY_3", 1),
            ("WAIT", 300),
            ("KEY_2", 1),
            ("WAIT", 150),
            ("KEY_2", 1),
            ("WAIT", 150),
            ("KEY_2", 1),
            ("WAIT", 150),
            ("KEY_2", 1),
            ("WAIT", 150),
            ("KEY_2", 1),
            ("WAIT", 150),
            ("KEY_4", 1),
            ("WAIT", 300),
            ("KEY_4", 1),
            ("WAIT", 300),
            ("KEY_4", 1),
            ("WAIT", 300),
            ("KEY_1", 1),
            ("WAIT", 60),
            ("KEY_1", 1),
            ("WAIT", 60),
            ("KEY_1", 1),
            ("WAIT", 60),
            ("KEY_2", 1),
            ("WAIT", 60),
            ("KEY_1", 1),
            ("WAIT", 60),
            ("KEY_2", 1),
            ("WAIT", 60),
            ("KEY_1", 1),
            ("WAIT", 60),
            ("KEY_2", 1),
            ("WAIT", 60),
            ("KEY_5", 1),
            ("WAIT", 120),
        ])
        self.tempo_comando = 0

    def executar_comando_simulado(self):
        if not self.comandos:
            return

        comando, duracao = self.comandos[0]

        if comando == "WAIT":
            self.tempo_comando += 1
            if self.tempo_comando >= duracao:
                self.comandos.popleft()
                self.tempo_comando = 0
        else:
            # Executa o comando por 1 frame
            if comando == "KEY_1":
                self.target_centro_x = min(self.target_centro_x + 30, pyxel.width - self.largura_rio / 2)
            elif comando == "KEY_2":
                self.target_centro_x = max(self.target_centro_x - 30, self.largura_rio / 2)
            elif comando == "KEY_3":
                self.target_largura = min(self.target_largura + 10, self.max_largura)
            elif comando == "KEY_4":
                self.target_largura = max(self.target_largura - 10, 20)
            elif comando == "KEY_5":
                self.animating_to_center = True
                self.target_centro_x = pyxel.width / 2
                self.target_largura = 45

            # Remove imediatamente após 1 frame
            self.comandos.popleft()
            self.tempo_comando = 0

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
                

            self.executar_comando_simulado()

            # atualiza árvores
            self.tree_manager.update_arvores(self.velocidade_scroll)
        
        # Lógica da animação automática
        if self.animating_to_center:
            # Verifica se já centralizou
            if abs(self.centro_rio_x - pyxel.width/2) < 1:
                # Começa a expandir após centralizar
                self.target_largura = self.max_largura
                

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
            
        
        self.tree_manager.draw_arvores()
