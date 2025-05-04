### Modulo de comunicacao em rede. Responsavel por:
### - Estabelecer conexoes via UDP
### - Enviar e receber dados entre cliente e servidor
### - Gerenciar socket e threads

# Bibliotecas
import socket           # Responsavel por criar e gerenciar conexoes de rede usando protocolo UDP
import threading        # Permite criar e controlar threads para execucao paralela (nao vai congelar o jogo)
import time             # Usado para controlar intervalos de tempo e marcar timestamps
import json             # Usado para codificar e decodificar dados em formato JSON para envio pela rede
from config import *    # Importa constantes e configuracoes do arquivo "config.py"


class NetworkManager:
    # Construtor
    # Prepara conexao: cria socket, define porta e variaveis de estado
    def __init__(self, port):
        self.sock = None                # Objeto socket UDP que sera criado para enviar/receber dados
        self.port = port                # Porta local usada pelo servidor para escutar conexoes
        self.running = False            # Indica se a conexao esta ativa ou nao
        self.connected = False          # Indica se ha uma conexao ativa com outro jogador
        self.remote_addr = None         # Endereco do servidor remoto (no modo cliente)
        self.client_addr = None         # Endereco do cliente conectado (usado apenas no modo host)
        self.received_packets = []      # Fila de pacotes recebidos

        self.receive_thread = None      # Thread responsavel por escutar pacotes recebidos
        self.reconnect_thread = None    # Thread que tenta reconectar automaticamente se a conexao for perdida (no cliente)
        self.last_recv = None           # Marca o horario da ultima mensagem recebida
        self.local_ip = None            # IP local da maquina, utilizado para exibir no menu de multiplayer do host

        # # DEBUG:
        # # captura o conjunto de threads que ja existiam antes
        # self._initial_threads = set(t.name for t in threading.enumerate())
    
    # Inicia servidor: abre porta e comeca a escutar conexoes
    def start_host(self):
        try:
            self.stop() # Encerra conexoes anteriores (se tiver alguma)

            # Cria socket UDP
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.settimeout(0.1) # Define tempo maximo de espera ao receber pacotes

            # Tenta associar socket a porta especifica
            # Senao escolhe uma porta aleatoria escolhida pelo SO
            try:
                self.sock.bind(("", self.port))

            # Se porta estiver ocupada, escolhe uma porta livre automaticamente
            except OSError as bind_err:
                print(f"Porta {self.port} ocupada, escolhendo porta aleatoria: {bind_err}")
                self.sock.bind(("", 0)) # Porta "0" faz o SO escolher uma porta livre
                _, new_port = self.sock.getsockname() # Atualiza com a nova porta
                self.port = new_port

            # Pega o IP local da maquina para exibir no menu do Host
            self.local_ip = self._get_local_ip()

            # Marca que a conexao esta ativa
            self.running = True

            time.sleep(0.1) # Aguarda um pouco antes de iniciar a escuta (evita de dar conflitos)
            # Cria thread para escutar pacotes recebidos
            self.receive_thread = threading.Thread(
                target=self._receive_host,              # Funcao que escuta dados como host
                daemon=True,                            # Finaliza thread junto com o programa principal
                name=f"Network-HostRecv-{self.port}"    # Nome identificador da thread
            )
            self.receive_thread.start() # Inicia a thread
            return True
        
        # Se ocorrer qualquer erro, exibe mensagem e retorna False
        except Exception as e:
            print(f"Erro ao iniciar host: {e}")
            return False
    
    # Obtem o endereco de IP local da maquina
    def _get_local_ip(self):
        try:
            # Cria socket UDP temporario para tentar descobrir o IP local real
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))  # Estabelece conexao com servidor DNS do Google
                return s.getsockname()[0]   # Retorna o IP local usado nessa conexao
        
        # Se falhar, retorna o endereco padrao do loopback (localhost)
        except Exception as e:
            print(f"Erro ao obter IP: {e}")
            return "127.0.0.1" # IP padrao do localhost (loopback)

    # Conecta a um servidor remoto usando IP e Porta
    def connect(self, ip, port):
        try:
            self.stop() # Encerra conexoes anteriores (se tiver alguma)
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Cria socket UDP
            self.sock.settimeout(0.1) # Define tempo maximo de espera para receber dados
            
            # Define o endereco do servidor remoto (IP e porta)
            self.remote_addr = (ip, int(port))

            # Envia pacote inicial para iniciar a conexao
            self._send({'type': 'handshake'})  # Pacote inicial para iniciar a comunicacao
            self.running = True # Marca que a conexao esta ativa

            # Cria thread para receber dados como cliente
            self.receive_thread = threading.Thread(
                target=self._receive_client,            # Funcao que escuta dados como cliente
                daemon=True,                            # Finaliza thread junto com o programa principal
                name="Network-ClientRecv"               # Nome do identificador da thread
            )
            self.receive_thread.start() # Inicia a thread

            # Espera 1 segundo e inicia thread de tentativa de reconexao
            time.sleep(1) # Espera 1 segundo para tentar reconectar
            # Cria thread para tentar reestabelecer conexao com o host, caso ela tiver caido
            self.reconnect_thread = threading.Thread(
                target=self._reconnect_loop,            # Funcao que tenta reestabelecer conexao com o host
                daemon=True,                            # Finaliza thread junto com o programa principal
                name="Network-Reconnect"                # Nome do identificador da thread
            )
            self.reconnect_thread.start() # Inicia a thread
            return True
        
        # Se ocorrer erro, informa ele e marca como desconectado
        except Exception as e:
            print(f"Erro ao conectar: {e}")
            self.connected = False
            return False
    
    # Para as threads e reseta variaveis ao desconectar
    def stop(self):
        self.running = False  # Sinaliza para as threads pararem
        self.connected = False # Marca como desconectado
        self.received_packets.clear() # Reseta a fila de dados recebidos

        # Espera a thread de recepcao finalizar
        if self.receive_thread:
            self.receive_thread.join(timeout=0.1)  # Aguarda thread terminar
            self.receive_thread = None # Limpa a referencia

        # Espera a thread de reconexao finalizar
        if self.reconnect_thread:
            self.reconnect_thread.join(timeout=(RECONNECT_INTERVAL + 1))
            self.reconnect_thread = None # Limpa a referencia

        # Fecha o socket e limpa referencia
        if self.sock:
            self.sock.close() 
            self.sock = None

        self.client_addr = None # Reseta endereco do cliente
        self.remote_addr = None # Reseta endereco remoto


        # # DEBUG:
        # # Auditoria de threads
        # remaining = set(t.name for t in threading.enumerate())
        # leaked = {name for name in remaining if name.startswith("Network-")} - self._initial_threads
        # if leaked:
        #     print("[WARNING] Thread(s) ainda vivas apos stop():", leaked)
        # else:
        #     print("Nenhuma thread vazando")

    # Enquanto nao estiver conectado, reenvia handshake a cada periodo (RECONNECT_INTERVAL)
    def _reconnect_loop(self):
        while self.running:
            # Se estiver desconectado e tiver endereco remoto, reenvia o handshake
            if not self.connected and self.remote_addr:
                self._send({'type': 'handshake'})
                time.sleep(RECONNECT_INTERVAL)
            
            # Espera por x segundos para a proxima tentativa
            time.sleep(RECONNECT_INTERVAL)

    # Envia dados para outro jogador/servidor
    def send(self, packet_type: str, data: dict):
        # So tenta enviar se o socket estiver pronto e conectado com algum jogador
        if not (self.sock and self.connected):
            return

        # TODO: Adicionar os tipos de dados a serem enviados na rede aqui
        # Monta o pacote de acordo com o tipo
        if packet_type == 'moviment':
            packet = {
                'type': 'moviment',
                'payload': data.get('payload'),
                'timestamp': time.time()
            }
        elif packet_type == 'shot':
            packet = {
                'type': 'shot',
                'x': data['x'],
                'y': data['y'],
                'timestamp': time.time()
            }
        elif packet_type == 'heartbeat':
            packet = {
                'type': 'heartbeat',
                'payload': '',
                'timestamp': time.time()
            }
        elif packet_type == 'game_start':
            packet = {
                'type': 'game_start',
                'payload': '', # TODO: Colocar dados do tipo de aviao escolhido
                'timestamp': time.time()
            }
        elif packet_type == 'hud':
            packet = {
                'type': 'hud',
                'fuel': data['fuel'],
                'lives': data['lives'],
                'timestamp': time.time()
            }

        
        # Envia o pacote
        self._send(packet)
    
    # Metodo interno que empacota os dados em JSON e envia via UDP
    def _send(self, data):
        try:
            # Converte os dados em string JSON e depois em bytes
            json_data = json.dumps(data).encode('utf-8')

            # Se for cliente, envia para o servidor (remote_addr)
            if self.remote_addr:  # Cliente
                self.sock.sendto(json_data, self.remote_addr)

            # Se for host, envia para o cliente conectado (client_addr)
            elif self.client_addr:  # Host
                self.sock.sendto(json_data, self.client_addr)

        # Caso ocorra algum erro no envio, exibe mensagem
        except Exception as e:
            print(f"Erro ao enviar dados: {e}")

    # Escuta dados recebidos em segundo plano do host (usando thread)
    def _receive_host(self):
        # Enquanto a conexao estiver ativa, escuta pacotes recebidos
        while self.running:
            try:
                # Recebe dados do socket (dado e endereco de quem enviou)
                data, addr = self.sock.recvfrom(MAX_PACKET_SIZE) # Define um limite de tamanho para o pacote (em bytes)
                # Decodifica os dados JSON recebidos
                packet = json.loads(data.decode('utf-8')) # Usa a codificacao de caracteres padrao (uft-8)
                
                self._add_packet_to_queue(packet)  # Adiciona na fila de pacotes recebido

                # Se for um pacote inicial de conexao
                if packet['type'] == 'handshake':
                    # Novo cliente pediu para conectar -> salva o endereco
                    self.client_addr = addr
                    self.connected = True # Marca como conectado
                    self.last_recv = time.time() # Atualiza o tempo da ultima mensagem recebida
                    print(f"Cliente conectado: {addr}")

                    # Envia uma resposta de handshake (uma especie de 'ACK') para confirmar conexao com o cliente
                    self._send({'type': 'handshake'})

                # Se for outros tipos de dados, vindo do cliente conectado
                else:
                    # Atualiza o tempo da ultima mensagem recebida
                    self.last_recv = time.time()

                    # Se for um ping de heartbeat, responde de volta para manter a conexao ativa (evitar timeout)
                    if isinstance(packet, dict) and packet.get('type') == 'heartbeat':
                        self._send({'type': 'heartbeat'})

            # Se passar do tempo limite, marca como desconectado
            except socket.timeout:
                # Se tiver algum cliente e passou do tempo limite
                if self.client_addr and (time.time() - self.last_recv > TIMEOUT):
                    print("Cliente desconectado por timeout")
                    self.client_addr = None # Reseta o cliente
                    self.connected = False # Marca como desconectado
            
            # Se tiver qualquer outro erro, printa ele
            except Exception as e:
                print(f"Erro no host: {e}")


    # Escuta dados recebidos em segundo plano do cliente (usando thread)
    def _receive_client(self):
        # Enquanto a conexao estiver ativa, escuta pacotes do servidor
        while self.running and self.sock:
            try:
                # Recebe dados do socket
                data, _ = self.sock.recvfrom(MAX_PACKET_SIZE) # Define um limite de tamanho para o pacote (em bytes)
                # Decodifica os dados JSON recebidos
                packet = json.loads(data.decode('utf-8')) # Usa a codificacao de caracteres padrao (uft-8)
                
                self._add_packet_to_queue(packet)  # Adiciona na fila de pacotes recebido

                # Se for um pacote inicial de conexao do host (uma especie de 'ACK')
                if packet['type'] == 'handshake':
                    self.connected = True # Marca como conectado
                    self.last_recv = time.time() # Atualiza o tempo da ultima mensagem recebida

                # Se forem dados de jogo
                else:
                    self.last_recv = time.time() # Atualiza o tempo da ultima mensagem recebida
                    self.connected = True # Marca como conectado
                    

            # Se passar do tempo limite, marca como desconectado
            except socket.timeout:
                # Verifica se estah conectado e se passou do timeout
                if self.connected and (time.time() - self.last_recv > TIMEOUT):
                    # Se estiver conectado printa que a conexao caiu (para evitar de printar multiplas vezes)
                    if self.connected:
                        print("Conexão com host perdida")
                    self.connected = False # Marca como desconectado
            
            # Para qualquer outro erro, printa ele no terminal
            except Exception as e:
                print(f"Erro no cliente: {e}")
    
    # Metodo para gerenciar a fila. Adiciona pacotes na fila com prioridade e controla o overflow
    def _add_packet_to_queue(self, packet):
        # Remove pacote de menor prioridade se a fila estiver cheia
        if len(self.received_packets) >= MAX_QUEUED_PACKETS:
            # Encontra a menor prioridade atual na fila de pacotes recebidos
            lowest_priority = max(
                # Obtem a prioridade dos pacotes recebidos na fila (se nao tiver prioridade especificada, 
                # assume que o pacote tem a menor prioridade possivel "999", por padrao)
                NETWORK_PRIORITY.get(p['type'], 999)  
                for p in self.received_packets # procura em todos os pacotes recebidos
            )

            # Remove o primeiro pacote com a menor prioridade
            # "enumerate" retorna uma tupla com dois valores para cada elemento da lista:
                # idx: O indice (posicao) do elemento (pacote) na lista (received_packets).
                # p: O proprio elemento (o pacote).
            for idx, p in enumerate(self.received_packets):
                # Se a prioridade do pacote na lista for a menor prioridade encontrada
                if NETWORK_PRIORITY.get(p['type'], 999) == lowest_priority:
                    self.received_packets.pop(idx) # Remove ele da lista (pop)
                    break # Sai do loop
        
        # Insere o novo pacote na posicao correta baseado na prioridade 
        # (assume que se o pacote nao tiver um nivel especificado, ele tem prioridade "999")
        packet_priority = NETWORK_PRIORITY.get(packet.get('type'), 999) # Pega o nivel de prioridade do pacote recebido
        insert_pos = 0 # Index que determina a nova posicao do novo pacote
        while insert_pos < len(self.received_packets): # "insert_pos" vaid de 0 ateh o tamanho maximo de qtd de pacotes recebidos 
            # Pega a prioridade do pacote atual no loop pela fila
            current_prio = NETWORK_PRIORITY.get(
                self.received_packets[insert_pos].get('type'), # Pega o pacote de acordo com o tipo
                999 # Assume uma prioridade minima se o pacote nao for especificado na lista
            )

            # Se a prioridade do pacote atual no loop pela fila for menor do que o pacote a ser inserido
            if packet_priority < current_prio:
                break # Sai do loop
            insert_pos += 1 # Se a prioridade do pacote for maior ou igual, pula para o proximo pacote na fila
        
        # Insere o novo pacote de acordo com a sua prioridade, deslocando os outros pacotes de menor prioridade para a direita
        self.received_packets.insert(insert_pos, packet)
