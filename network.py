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
        self.data = None                # Ultimos dados recebidos

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
        self.data = None # Reseta os dados recebidos

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
    def send(self, data):
        # Se o socket estiver ativo e estiver conectado, envia os dados do jogo
        if self.sock and self.connected:
            self._send({
                'type': 'game_data',        # Tipo do pacote
                'payload': data,            # Conteudo a ser enviado
                'timestamp': time.time()    # Marca o momento do envio
            })
    
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
                
                # Se for um pacote inicial de conexao
                if packet['type'] == 'handshake':
                    # Novo cliente pediu para conectar -> salva o endereco
                    self.client_addr = addr
                    self.connected = True # Marca como conectado
                    self.last_recv = time.time() # Atualiza o tempo da ultima mensagem recebida
                    print(f"Cliente conectado: {addr}")

                    # Envia uma resposta de handshake (uma especie de 'ACK') para confirmar conexao com o cliente
                    self._send({'type': 'handshake'})

                # Se for dados de jogo, vindo do cliente conectado
                elif packet['type'] == 'game_data' and addr == self.client_addr:
                    # Armazena os dados recebidos
                    self.data = packet['payload']
                    # Atualiza o tempo da ultima mensagem recebida
                    self.last_recv = time.time()

                    # Se for um ping de heartbeat, responda de volta para manter a conexao ativa (evitar timeout)
                    if isinstance(self.data, dict) and self.data.get('type') == 'heartbeat':
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
                
                # Se for um pacote inicial de conexao do host (uma especie de 'ACK')
                if packet['type'] == 'handshake':
                    self.connected = True # Marca como conectado
                    self.last_recv = time.time() # Atualiza o tempo da ultima mensagem recebida

                # Se forem dados de jogo
                elif packet['type'] == 'game_data':
                    self.data = packet['payload'] # Guarda o dado recebido
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