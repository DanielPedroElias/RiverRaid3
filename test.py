# Classe principal que gerencia o estado do jogo (singleplayer/multiplayer)
class GameState:
    # Método de inicialização
    def __init__(self, game, is_multiplayer=False, is_host=False, initial_seed=None, initial_rio_centro=None , initial_rio_largura=None):
        self.game = game  # Referência para o objeto principal do jogo
        self.is_multiplayer = is_multiplayer  # Flag para modo multiplayer
        self.is_host = is_host  # Flag para identificar se é o host

        # Fim de jogo
        self.death_delay = False        # Verifica se estah aguardando para entrar no game over 
        self.death_delay_timer = 0      # quantos frames faltam para o delay de morte acabar
        self.game_over = False          # flag de fim de jogo
        self.game_over_timer = 0        # temporizador em frames

        # Posicionamento inicial dos jogadores (host vs cliente)
        if is_host:
            # Host controla jogador 1 (esquerda)
            self.player_x, self.player_y = 55, 130  
            # Jogador 2 (cliente) começa à direita
            self.player2_x, self.player2_y = 90, 130  
        else:
            # Cliente controla jogador 2 (direita)
            self.player_x, self.player_y = 90, 130
            # Jogador 1 (host) começa à esquerda
            self.player2_x, self.player2_y = 55, 130  

        # Inicializa o cenário de fundo
        self.background = Background(is_host=is_host , is_multiplayer=is_multiplayer) 

        # HUD
        self.life_player1 = MAX_LIVES  # Vida do jogador 1 (host)
        self.fuel_player1 = MAX_FUEL # Gasolina do jogador 1 (Host)
        self.life_player2 = MAX_LIVES  # Vida do jogador 2 (cliente)
        self.fuel_player2 = MAX_FUEL # Gasolina do jogador 2 (Cliente)
        self.invincible_timer_j1 = 0  # Temporizador de invencibilidade do jogador 1
        self.invincible_timer_j2 = 0  # Temporizador de invencibilidade do jogador 2
        self.INVINCIBILITY_DURATION = 90  # Duração em frames (1.5s a 60FPS)
        self.score_player1 = 0  # Pontuação do jogador 1
        self.score_player2 = 0  # Pontuação do jogador 2

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
        
        if initial_rio_largura is not None and not is_host:
            self.background.largura_rio     = initial_rio_largura
            self.background.target_largura  = initial_rio_largura

        if is_multiplayer and not is_host:  # Apenas clientes multiplayer não atualizam
            self.background.tree_manager.update_arvores = lambda _: None  # Desabilita atualização de árvores para clientes

        # lista de tiros locais e da outra tela
        self.shots = []          # tiros deste jogador
        self.remote_shots = []   # tiros vindos pela rede

        self.explosions = []   # lista de Explosion ativos
        self.remote_explosions = []  # explosões vindas pela rede

        self.boat_manager = BoatManager(self.background)    # barcos locais (host gera)
        self.remote_boats = []                             # barcos sincronizados via rede



    def _collide_player(self, hitbox, px, py):
        left, top, right, bottom = hitbox
        return (px+PLAYER_WIDTH>left and px<right and
                py+PLAYER_HEIGHT>top and py<bottom)
    
    # Método para atualizar o estado do jogo a cada frame
    def update(self):
        # Apenas atualiza a lógica do jogo se não estiver em pause
        if not isinstance(self.game.current_state, PauseMenuState):
            self.background.update()  # ← Movido para fora da verificação de pause

        # Comunicação em rede (apenas multiplayer)
        if self.is_multiplayer:
            self.send_data()  # Envia dados do jogador local
            self.receive_data()  # Recebe dados do outro jogador

        # Se estiver em Game Over, apenas decrementa o timer
        if self.game_over:
            self.game_over_timer -= 1
            if self.game_over_timer <= 0:
                # volta ao menu principal
                self.game.network.stop()  # Encerra a conexao
                self.game.change_state(MenuState(self.game))
            return
        
        # Se estiver no “delay de morte”, decrementa o seu timer,
        # mas continuar rodando o jogo normalmente ateh acabar o timer:
        if self.death_delay:
            self.death_delay_timer -= 1
            if self.death_delay_timer <= 0:
                # passado o delay, o Game Over eh ativado
                self.death_delay      = False
                self.game_over        = True
                self.game_over_timer  = 5 * FPS   # 5 segundos de tela preta

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
            # Disparo: cria um tiro quando apertar SPACE
            if pyxel.btnp(pyxel.KEY_SPACE):
                # inicia no centro horizontal do avião, um pouco acima dele
                shot_x = self.player_x + PLAYER_WIDTH // 2 - 1
                shot_y = self.player_y
                self.shots.append(Shot(shot_x, shot_y))

        # Limites da tela
        self.player_x = max(0, min(self.player_x, SCREEN_WIDTH - PLAYER_WIDTH))

        game_area_height = SCREEN_HEIGHT - HUD_HEIGHT
        self.player_y = max(0, min(self.player_y, game_area_height - PLAYER_HEIGHT))

        # Gasolina:
        consumption_per_frame = FUEL_CONSUMPTION_RATE / FPS # Calcula qtd de gasolina para consumir neste frame (unidades por frame)
        # Atualizacao para o modo Singleplayer da gasolina:
        if not self.is_multiplayer:
            self.fuel_player1 = max(0, self.fuel_player1 - consumption_per_frame) # Decrementa, garantindo que nunca fique negativo
        if self.is_host:
            self.fuel_player1 = max(0, self.fuel_player1 - consumption_per_frame) # Decrementa, garantindo que nunca fique negativo
        else:
            self.fuel_player2 = max(0, self.fuel_player2 - consumption_per_frame) # Decrementa, garantindo que nunca fique negativo

        # Atualiza temporizadores de invencibilidade
        if self.invincible_timer_j1 > 0:
            self.invincible_timer_j1 -= 1 # Invencibilidade do jogador 1
        if self.invincible_timer_j2 > 0:
            self.invincible_timer_j2 -= 1 # Invencibilidade do jogador 2

        self.update_shots()
        
        # local
        for exp in self.explosions:
            exp.update()
        self.explosions = [e for e in self.explosions if not e.is_dead()]

        # remota
        for exp in self.remote_explosions:
            exp.update()
        self.remote_explosions = [
            e for e in self.remote_explosions if not e.is_dead()
        ]

        # atualiza barcos (host gera; ambos movem)
        self.boat_manager.update()
        # recebe remote_boats já populada em receive_data
        for b in self.remote_boats:
            b.update()

        
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
                    self.life_player1 = max(0, self.life_player1 - 1)  # Perde vida 
                    self.invincible_timer_j1 = self.INVINCIBILITY_DURATION  # Ativa invencibilidade

            # Lógica do cliente para jogador 2
            elif not self.is_host and self.invincible_timer_j2 <= 0:
                colisoes = check_tree_collision(
                    self.player_x, self.player_y,
                    self.background.tree_manager.arvores,
                    "Jogador 2"
                )
                if colisoes > 0:
                    self.life_player2 = max(0, self.life_player2 - 1)  # Perde vida
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
                    self.life_player1 = max(0, self.life_player1 - 1)  # Perde vida
                    self.invincible_timer_j1 = self.INVINCIBILITY_DURATION  # Ativa invencibilidade
        
        ## ————— Colisão Tiro × Árvore (host destrói; ambos removem tiro no primeiro hit) —————
        for shot_list in (self.shots, self.remote_shots):
            for shot in shot_list.copy():
                hit = False

                for tree in self.background.tree_manager.arvores:
                    # ignora árvores já destruídas
                    if not tree.visible:
                        continue

                    # calcula hitboxes
                    left, top, right, bottom = tree.hitbox
                    s_left = shot.x
                    s_right = shot.x + shot.width
                    s_top = shot.y
                    s_bottom = shot.y + shot.height
                    
                    if (s_right > left and s_left < right and
                        s_bottom > top and s_top < bottom):
                        # host marca a árvore como destruída
                        if (self.is_host or not self.is_multiplayer):
                            tree.visible = False

                            # Host destruiu uma arvore, aumenta a pontuacao
                            self.score_player1 += 2
                            # cria explosão no centro da árvore
                            cx = (left + right) // 2 - 16 // 2
                            cy = (top  + bottom) // 2 - 16 // 2
                            self.explosions.append(
                                Explosion(cx, cy, 16, 16, 16, 16, duration=8)
                            )
                        else:
                            # Cliente destruiu uma arvore, aumenta a pontuacao
                            self.score_player2 += 2
                        # qualquer um remove o tiro no primeiro contato
                        shot_list.remove(shot)
                        hit = True
                        break

                if hit:
                    # já tratou esse tiro—vai para o próximo
                    continue

                # se não colidiu e saiu da tela, também remove
                if shot.is_off_screen():
                    shot_list.remove(shot)

        ## ————— Colisão Tiro × Barco —————
        # percorre cada lista de tiros
        for shot_list in (self.shots, self.remote_shots):
            for shot in shot_list.copy():
                for boat in (self.boat_manager.boats if (self.is_host or not self.is_multiplayer) else self.remote_boats):
                    # só colisão em barcos visíveis
                    if not boat.visible:
                        continue
                    # hitbox do barco e do tiro
                    b_left, b_top, b_right, b_bottom = boat.hitbox
                    s_left = shot.x
                    s_right = shot.x + shot.width
                    s_top = shot.y
                    s_bottom = shot.y + shot.height

                    if (s_right > b_left and s_left < b_right and
                        s_bottom > b_top   and s_top < b_bottom):
                        # host é fonte da verdade: destrói o barco
                        if (self.is_host or not self.is_multiplayer):
                            boat.visible = False

                            # Host destruiu um barco, aumenta a pontuacao
                            self.score_player1 += 4
                            # spawn de explosão no centro do barco
                            cx = (b_left + b_right)//2 - 8   # metade de 16px
                            cy = (b_top  + b_bottom)//2 - 8
                            self.explosions.append(
                                Explosion(cx, cy, 16, 16, 16, 16, duration=8)
                            )
                        else:
                            # Cliente destruiu um barco, aumenta a pontuacao
                            self.score_player2 += 4
                        # em qualquer caso, remove o tiro no primeiro hit
                        shot_list.remove(shot)
                        break

        ## ————— Colisão Jogador × Barco —————
        # verifica invencibilidade e colisão para cada jogador
        # Jogador 1 (host)  
        if (self.is_host or not self.is_multiplayer) and self.invincible_timer_j1 <= 0:
            for boat in self.boat_manager.boats:
                if boat.visible:
                    left, top, right, bottom = boat.hitbox
                    j_left = self.player_x
                    j_right = self.player_x + PLAYER_WIDTH
                    j_top = self.player_y
                    j_bottom = self.player_y + PLAYER_HEIGHT
                    if (j_right > left and j_left < right and
                        j_bottom > top   and j_top < bottom):
                        # colisão: perde vida e fica invencível
                        self.life_player1 = max(0, self.life_player1 - 1)
                        self.invincible_timer_j1 = self.INVINCIBILITY_DURATION
                        break
        # Jogador 2 (cliente)  
        if not self.is_host and self.invincible_timer_j2 <= 0:
            for boat in self.remote_boats:
                if boat.visible:
                    left, top, right, bottom = boat.hitbox
                    j_left = self.player_x
                    j_right = self.player_x + PLAYER_WIDTH
                    j_top = self.player_y
                    j_bottom = self.player_y + PLAYER_HEIGHT
                    if (j_right > left and j_left < right and
                        j_bottom > top   and j_top < bottom):
                        self.life_player2 = max(0, self.life_player2 - 1)
                        self.invincible_timer_j2 = self.INVINCIBILITY_DURATION
                        break
        
        # Jogador 1 morreu?
        if self.life_player1 == 0 and not getattr(self, "_exploded_j1", False) and (self.is_host or not self.is_multiplayer):
            # marca que já acionou explosão
            self._exploded_j1 = True
            # centro do avião 1

            cx = self.player_x + PLAYER_WIDTH//2 - 8
            cy = self.player_y + PLAYER_HEIGHT//2 - 8
            self.explosions.append(
                Explosion(cx, cy, 16, 16, 16, 16, duration=30)
            )

        # Jogador 2 morreu?
        if self.is_multiplayer and self.life_player2 == 0 and not getattr(self, "_exploded_j2", False):
            self._exploded_j2 = True
            # posição do avião 2 depende se host ou client
            px, py = (self.player2_x, self.player2_y) if self.is_host else (self.player_x, self.player_y)
            cx = px + PLAYER_WIDTH//2 - 8
            cy = py + PLAYER_HEIGHT//2 - 8
            self.explosions.append(
                Explosion(cx, cy, 16, 16, 16, 16, duration=30)
            )

        # Fim de jogo:
        # Condição SINGLEPLAYER
        if not self.is_multiplayer and self.life_player1 == 0 and not self.death_delay:
            self.death_delay = True
            self.death_delay_timer = 2 * FPS   # 2 segundos de delay

        # Condição MULTIPLAYER
        elif self.is_multiplayer and self.life_player1 == 0 and (not self.game.network.connected or self.life_player2 == 0) and not self.death_delay:
            self.death_delay = True
            self.death_delay_timer = 2 * FPS    # 2 segundos de delay

       

    def update_shots(self):
        """Atualiza posição e descarta tiros fora da tela — usado tanto em play quanto em pause."""
        # locais
        for shot in self.shots:
            shot.update()
        self.shots = [s for s in self.shots if not s.is_off_screen()]

        # remotos
        for shot in self.remote_shots:
            shot.update()
        self.remote_shots = [s for s in self.remote_shots if not s.is_off_screen()]
        
    # Método para enviar dados pela rede
    def send_data(self):
        if self.is_multiplayer and self.game.network.connected:
            if self.is_host:
                data = {
                    'player': [self.player_x, self.player_y],  # Posição atual
                    'rio_centro': self.background.centro_rio_x,  # Posição do rio
                    'rio_largura': self.background.largura_rio,       # ← NOVO
                    'seed': self.background.tree_manager.random_seed,  # Seed aleatória
                    'invincible': self.invincible_timer_j1 if self.is_host else self.invincible_timer_j2,  # Timer de invencibilidade
                    'type': 'game_update', # Tipo de mensagem
                    'arvores': self.background.tree_manager.get_tree_states() , # Adicione esta linha
                    'shots': [shot.to_dict() for shot in self.shots],
                    'explosions': [exp.to_dict() for exp in self.explosions],
                    'boats': self.boat_manager.get_states(),
                    'player_type': 'host',
                    'fuel': self.fuel_player1,
                    'lives': self.life_player1
                }
            else:
                data = {
                    'player': [self.player_x, self.player_y],  # Posição atual
                    'rio_centro': self.background.centro_rio_x,  # Posição do rio
                    'rio_largura': self.background.largura_rio,       # ← NOVO
                    'seed': self.background.tree_manager.random_seed,  # Seed aleatória
                    'invincible': self.invincible_timer_j1 if self.is_host else self.invincible_timer_j2,  # Timer de invencibilidade
                    'type': 'game_update', # Tipo de mensagem
                    'arvores': self.background.tree_manager.get_tree_states() , # Adicione esta linha
                    'shots': [shot.to_dict() for shot in self.shots],
                    'explosions': [exp.to_dict() for exp in self.explosions],
                    'boats': self.boat_manager.get_states(),
                    'player_type': 'client',
                    'fuel': self.fuel_player2,
                    'lives': self.life_player2
                }
                                
            self.game.network.send(data)  # Envia os dados

    # Método para receber dados da rede
    def receive_data(self):
        # Define a função receive_data como método da classe (self é a referência ao objeto)
        
        if self.is_multiplayer and isinstance(self.game.network.data, dict):
            # Verifica se o jogo está no modo multiplayer E se os dados recebidos da rede são um dicionário
            
            data = self.game.network.data
            # Armazena os dados recebidos da rede na variável local 'data' para facilitar acesso
            if (len(data) > 1): # ignora heartbeat
                try:
                    # Inicia um bloco try para capturar possíveis erros no processamento dos dados
                    
                    # Atualiza posição do outro jogador
                    self.player2_x, self.player2_y = data['player']
                    # Extrai as coordenadas x e y do outro jogador do dicionário de dados
                    ## tanto host quanto cliente atualizam os remote_shots
                    if 'shots' in data:
                        self.remote_shots = [Shot.from_dict(d) for d in data['shots']]

                    if 'explosions' in data:
                            # reconstrói explosões que vieram do outro lado
                            self.remote_explosions = [
                                Explosion.from_dict(d) for d in data['explosions']
                            ]

                    # Atualiza barcos remotos (apenas cliente recebe)
                    if 'boats' in data and not self.is_host:
                        # cliente reconstrói lista de barcos
                        self.remote_boats = [Boat.from_dict(d) for d in data['boats']]

                
                    # Sincroniza temporizador de invencibilidade
                    if self.is_host:   
                        # Pega gasolina e vida se o host recebe um pacote do cliente
                        if data.get('player_type', -1) == 'client':
                            self.fuel_player2 = data.get('fuel', self.fuel_player2)
                            self.life_player2 = data.get('lives', self.life_player2) 
                        # Verifica se esta instância é o host (jogador 1)
                        self.invincible_timer_j2 = data.get('invincible', 0)
                        # Host recebe o timer de invencibilidade do cliente (jogador 2)
                        # Usa .get() para evitar KeyError, retornando 0 se 'invincible' não existir
                    else:
                        # Pega gasolina e vida se o cliente recebe um pacote do host
                        if data.get('player_type', -1) == 'host':
                            self.fuel_player1 = data.get('fuel', self.fuel_player1)
                            self.life_player1 = data.get('lives', self.life_player1)
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
                    
                    if not self.is_host and 'rio_largura' in data:
                        self.background.largura_rio    = data['rio_largura']
                        self.background.target_largura = data['rio_largura']
                        
                    # Sincroniza seed aleatória se necessário
                    if 'seed' in data and data['seed'] != self.background.tree_manager.random_seed:
                        # Verifica se existe uma seed nos dados E se é diferente da seed atual
                        self.background.tree_manager.random_seed = data['seed']
                        # Atualiza a seed aleatória no gerenciador de árvores
                        random.seed(data['seed'])
                        # Define a seed global do módulo random para manter consistência
                        self.background.tree_manager.reset_arvores()
                        # Reinicia as árvores com a nova seed para sincronizar a geração aleatória
                    # Sincroniza árvores
                    if 'arvores' in data and not self.is_host:
                        self.background.tree_manager.set_tree_states(data['arvores'])
                except (KeyError, TypeError):
                    # Captura exceções caso haja erro ao acessar chaves do dicionário ou tipos incorretos
                    print("Erro na sincronização dos dados")
                    # Imprime mensagem de erro (poderia ser tratado de forma mais robusta em produção)

    # Método para desenhar o jogo
    def draw(self):
        # Se o jogo acabou
        if self.game_over:
            # pinta tudo de preto
            pyxel.cls(0)
            # escreve no centro
            txt = "FIM DE JOGO"
            w = len(txt) * 4   # aprox largura em px de cada caractere
            x = (SCREEN_WIDTH  - w) // 2
            y = (SCREEN_HEIGHT - 8) // 2  # 8px de altura de texto
            pyxel.text(x, y, txt, 7)
            return

        pyxel.cls(COLOR_BG)                                   # Limpa a tela com a cor de fundo definida
        
        # Separador da HUD (linha que divide o jogo da interface)
        sep_y = SCREEN_HEIGHT - HUD_HEIGHT # Posicao em 'Y' = Separador eh igual a altura da tela menos a altura da HUD
        pyxel.clip(0, 0, SCREEN_WIDTH, sep_y) # Define o clip para a área de jogo

        self.background.draw()                                # Desenha o cenário de fundo

        # desenha barcos locais e remotos
        self.boat_manager.draw()
        for b in self.remote_boats:
            b.draw()

        # desenha tiros locais
        for shot in self.shots:
            shot.draw()
        # desenha tiros vindos pela rede
        for shot in self.remote_shots:
            shot.draw()

        # desenha explosões locais
        for exp in self.explosions:
            exp.draw()
        # desenha explosões vindas pela rede
        for exp in self.remote_explosions:
            exp.draw()

        # Lógica de piscar durante invencibilidade
        should_draw_j1 = (self.invincible_timer_j1 // 5) % 2 == 0 if self.invincible_timer_j1 > 0 else True  # Define se o jogador 1 deve piscar (quando invencível)
        should_draw_j2 = (self.invincible_timer_j2 // 5) % 2 == 0 if self.invincible_timer_j2 > 0 else True  # Define se o jogador 2 deve piscar (quando invencível)

        if self.is_multiplayer:
            if self.life_player1 > 0:
                # Renderização do jogador 1
                if should_draw_j1:             # Verifica se é multiplayer E se deve desenhar o jogador 1
                    if self.is_host:                                  # Se for o host (jogador 1)
                        pyxel.blt(self.player_x, self.player_y, 0, 32, 0, PLAYER_WIDTH, PLAYER_HEIGHT, colkey=0)  # Desenha o avião (host)
                    else:                                              # Se for o cliente
                        pyxel.blt(self.player2_x, self.player2_y, 0, 32, 0, PLAYER_WIDTH, PLAYER_HEIGHT, colkey=0)  # Desenha o avião do host na posição recebida
                
            if self.game.network.connected and self.life_player2 > 0:
                # Renderização do jogador 2 (helicóptero)
                if should_draw_j2:
                    # Animação da hélice (alterna entre dois frames a cada 5 frames)
                    helicopter_frame = (pyxel.frame_count // 5) % 2
                    
                    # Coordenadas dos frames na imagem (48,0) e (0,16)
                    u = 48 if helicopter_frame == 0 else 0
                    v = 0 if helicopter_frame == 0 else 16

                    if self.is_host:
                        pyxel.blt(
                            self.player2_x, self.player2_y,
                            0,            # Banco de imagens
                            u, v,         # Coordenadas do frame
                            PLAYER_WIDTH, PLAYER_HEIGHT,
                            colkey=0
                        )
                    else:
                        pyxel.blt(
                            self.player_x, self.player_y,
                            0,            # Banco de imagens
                            u, v,         # Coordenadas do frame
                            PLAYER_WIDTH, PLAYER_HEIGHT,
                            colkey=0
                        )

            
            # Status da conexão
            if self.game.network.connected:                        # Verifica se há conexão de rede
                pyxel.text(10, 10, "Multiplayer - Conectado", 0)   # Mostra status "Conectado"
            else:                                                  # Se não estiver conectado
                pyxel.text(10, 10, "Multiplayer - Desconectado", 0)  # Mostra status "Desconectado"

        # Modo singleplayer
        else:
            # Se não for multiplayer E deve desenhar o jogador e jogador tem vida maior que zero
            if should_draw_j1 and self.life_player1 > 0:         
                pyxel.blt(self.player_x, self.player_y, 0, 32, 0, PLAYER_WIDTH, PLAYER_HEIGHT, colkey=0)  # Desenha o jogador único

        # Desativa o clip (volta ao desenho em tela cheia)
        pyxel.clip()
        pyxel.line(0, sep_y, SCREEN_WIDTH, sep_y, COLOR_HUD_LINE) # Desenha a linha horizontal da hud
        if self.is_multiplayer:
           # Logica para as duas barras de combustivel (jogador 1 e 2):

            # Calcula largura das barras: (largura_total - (3*padding)) / 2
            # De forma que caiba duas barras + 3 *paddings (de espaco entre elas):
            bar_w = (SCREEN_WIDTH - 3 * PADDING) // 2

            # Posicoes X das duas barras:
            x1 = PADDING # Barra esquerda
            x2 = (PADDING * 2) + bar_w # Barra direita ((padding * 2) + largura da primeira barra)

            # Posicao Y inicial das barras (2px abaixo do separador da HUD)
            y_bar = sep_y + 2
            # Coracoes (vidas) em baixo das barras de gasolina
            y_heart = y_bar + FUEL_BAR_H + 2 # Posicao Y dos coracoes
            # Centraliza coracao abaixo da barra
            total_heart_w = MAX_LIVES * HEART_SIZE + (MAX_LIVES - 1) * HEART_GAP # Largura total dos coracoes
            
            # Desenha HUD do jogador 1 se ele estiver vivo
            if self.life_player1 > 0:
                # Barra de combustivel - Jogador 1
                # desenha barra do jogador 1
                pyxel.rectb(x1, y_bar, bar_w, FUEL_BAR_H, COLOR_FUEL_BORDER) # Desenha borda da barra
                filled1 = int((self.fuel_player1 / MAX_FUEL) * (bar_w - 2)) # Calcula o nivel de preenchimento da barra
                pyxel.rect(x1 + 1, y_bar + 1, filled1, FUEL_BAR_H - 2, COLOR_FUEL) # Preenche proporcionalmente a barra de gasolina

                # Coracao - Jogador 1
                start_x1 = x1 + (bar_w - total_heart_w) // 2 # Calcula posicao inicial para centralizar

                # Desenha cada coracao (cheio ou vazio)
                for i in range(MAX_LIVES):
                    cx = start_x1 + i * (HEART_SIZE + HEART_GAP) # Posicao X do coracao atual

                    if self.life_player1 > i:
                        pyxel.blt(cx, y_heart, 0, 0, 32, HEART_SIZE, HEART_SIZE, colkey=0)  # Desenha coracao cheio
                    else:
                        pyxel.blt(cx, y_heart, 0, 8, 32, HEART_SIZE, HEART_SIZE, colkey=0)  # Desenha coracao vazio
                
                # Pontuação jogador 1
                pyxel.text(
                    x1,                     # x centralizado
                    y_bar + FUEL_BAR_H + HEART_SIZE + 4,   # 1px abaixo dos corações
                    f"Score P1: {self.score_player1}",
                    COLOR_TEXT
                )

            # Desenha HUD do jogador 2 se ele estiver vivo e o jogo conectado
            if self.game.network.connected and self.life_player2 > 0:

                # Barra de combustivel - Jogador 2 
                pyxel.rectb(x2, y_bar, bar_w, FUEL_BAR_H, COLOR_FUEL_BORDER) # Desenha borda da barra
                filled2 = int((self.fuel_player2 / MAX_FUEL) * (bar_w - 2)) # Calcula o nivel de preenchimento da barra
                pyxel.rect(x2 + 1, y_bar + 1, filled2, FUEL_BAR_H - 2, COLOR_FUEL) # Preenche proporcionalmente a barra de gasolina


                # Coracao - Jogador 2 (ja foi calculado a largura total dos coracoes)
                start_x2 = x2 + (bar_w - total_heart_w) // 2 # Calcula posicao inicial para centralizar

                # Desenha cada coracao (cheio ou vazio)
                for i in range(MAX_LIVES):
                    cx = start_x2 + i * (HEART_SIZE + HEART_GAP) # Posicao X do coracao atual

                    if self.life_player2 > i:
                        pyxel.blt(cx, y_heart, 0, 0, 32, HEART_SIZE, HEART_SIZE, colkey=0)  # Desenha coracao cheio
                    else:
                        pyxel.blt(cx, y_heart, 0, 8, 32, HEART_SIZE, HEART_SIZE, colkey=0)  # Desenha coracao vazio

                # Pontuação jogador 2
                pyxel.text(
                    x2,                     # x centralizado
                    y_bar + FUEL_BAR_H + HEART_SIZE + 4,   # 1px abaixo dos corações
                    f"Score P2: {self.score_player2}",
                    COLOR_TEXT
                )

        # HUD para modo singleplayer
        else:
            # HUD centralizada
            cx = (SCREEN_WIDTH - FUEL_BAR_W) // 2 # Centraliza caoracao em 'X' na horizontal
            y_bar = sep_y + 2 # Posicao Y inicial das barras de gasolina (2px abaixo do separador da HUD)

            # Desenha HUD do jogador 1 se ele estiver vivo
            if self.life_player1 > 0:
                # Desenha uma unica barra de combustivel:
                pyxel.rectb(cx, y_bar, FUEL_BAR_W, FUEL_BAR_H, COLOR_FUEL_BORDER) # Desenha borda da barra
                filled = int((self.fuel_player1 / MAX_FUEL) * (FUEL_BAR_W - 2)) # Calcula o nivel de preenchimento da barra
                pyxel.rect(cx+1, y_bar+1, filled, FUEL_BAR_H-2, COLOR_FUEL) # Preenche proporcionalmente a barra de gasolina

                # Coracoes
                y_heart = y_bar + FUEL_BAR_H + 2 # Posicao Y dos coracoes (em baixo da barra de gasolina)
                start_x = (SCREEN_WIDTH - (MAX_LIVES*HEART_SIZE + (MAX_LIVES-1)*HEART_GAP)) // 2 # Calcula posicao inicial dos coracoes para centralizar

                # Desenha cada coracao (cheio ou vazio)
                for i in range(MAX_LIVES): 
                    xh = start_x + i*(HEART_SIZE + HEART_GAP) # Posicao X do coracao atual
                    if self.life_player1 > i:
                        pyxel.blt(xh, y_heart, 0, 0, 32, HEART_SIZE, HEART_SIZE, colkey=0)  # Desenha coracao cheio
                    else:
                        pyxel.blt(xh, y_heart, 0, 8, 32, HEART_SIZE, HEART_SIZE, colkey=0)  # Desenha coracao vazio

                # Pontuação Singleplayer
                pyxel.text(
                    cx,                     # x centralizado
                    y_bar + FUEL_BAR_H + HEART_SIZE + 4,   # 1px abaixo dos corações
                    f"Score: {self.score_player1}",
                    COLOR_TEXT
                )

        # # Debug: mostra posições
        # if self.is_host:                                       # Se for o host
        #     pyxel.text(10, 20, f"Host: {self.player_x},{self.player_y}", 7)  # Mostra posição do host
        #     pyxel.text(10, 30, f"Cliente: {self.player2_x},{self.player2_y}", 7)  # Mostra posição do cliente
        # else:                                                  # Se for o cliente
        #     pyxel.text(10, 20, f"Host: {self.player2_x},{self.player2_y}", 7)  # Mostra posição do host
        #     pyxel.text(10, 30, f"Cliente: {self.player_x},{self.player_y}", 7)  # Mostra posição do cliente        

        # # Debug: hitbox das árvores
        # for arvore in self.background.tree_manager.arvores:    # Itera por todas as árvores
        #     arv_left, arv_top, arv_right, arv_bottom = arvore.hitbox  # Obtém coordenadas da hitbox
        #     pyxel.rectb(arv_left, arv_top, arv_right - arv_left, arv_bottom - arv_top, 8)  # Desenha retângulo da hitbox
        # # debug: hitbox dos barcos
        # for b in self.boat_manager.boats:
        #     bar_left, bar_top, bar_right, bar_bottom = b.hitbox  # Obtém coordenadas da hitbox
        #     pyxel.rectb(bar_left, bar_top, bar_right - bar_left, bar_bottom - bar_top, 8)  # Desenha retângulo da hitbox
        # # # Debug: hitbox do jogador 1
        # pyxel.rectb(self.player_x, self.player_y, PLAYER_WIDTH, PLAYER_HEIGHT, 8)  # Desenha retângulo da hitbox do jogador 1

