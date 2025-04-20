### Modulo de comunicacao em rede. Responsavel por:
### - Estabelecer conexoes UDP
### - Enviar/receber dados entre clientes
### - Gerenciar sockets e threads

# TODO: Implementar conexao em rede
class NetworkManager:
    # Construtor
    # Prepara conexao: cria socket, define porta e variaveis de estado
    def __init__(self, port):
        pass
    
    # Inicia servidor: abre porta e comeca a escutar conexoes
    def start_host(self):
        print("Host started (not implemented)")
    
    # Conecta a um servidor remoto usando IP e porta
    def connect(self, ip, port):
        print(f"Connecting to {ip}:{port} (not implemented)")
    

    # Envia dados para outro jogador/servidor
    def send(self, data):
        pass
    
    # Escuta dados recebidos em segundo plano (usando thread)
    def _receive(self):
        pass