import socket
import threading
import sys 
import time
import queue 

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

SERVER_IP = '127.0.0.1' 
SERVER_PORT_TCP = 12345
SERVER_PORT_UDP = 54321

# Dicionários para armazenar os IPs dos dispositivos conectados
tcp_clients = []
i = 1
HEADERSIZE = 10

# Fila para armazenar mensagens UDP
udp_message_queue = queue.Queue()

# Função para lidar com conexões TCP
def handle_tcp_connection(client_socket, address, i): 
    print(f"Conexão TCP estabelecida com {address}")
    dispositivo = {"Nome": f"Tranca{i}", address[0]: address[1]}
    tcp_clients.append(dispositivo)
    i += 1
    print("Clientes TCP:", tcp_clients)

    while True: 
        try:
            msg = input("""Digite o comando: 
[0] Trancar
[1] Destrancar 
                        
Opção: """) 
            if msg: 
                if msg == "0": 
                    client_socket.send(bytes("comando-trancar-", "utf-8")) 
                elif msg == "1": 
                    client_socket.send(bytes("comando-destrancar-", "utf-8")) 
                
            time.sleep(3)
        except (ConnectionResetError, BrokenPipeError):
            print(f"Conexão com {address} encerrada.")
            tcp_clients.remove(dispositivo)
            client_socket.close()
    
# Função para armazenar as mensagens que chegam via udp em uma fila
def handle_udp_connection(udp_socket):
    print("Aguardando mensagens UDP...")
    while True:
        data, address = udp_socket.recvfrom(1024)
        # Coloca a mensagem na fila
        udp_message_queue.put((data.decode('utf-8'), address))

# Função para tratar as mensagens que chegam na fila
def process_udp_messages():
    while True:
        if not udp_message_queue.empty():
            # Obtém a mensagem e o endereço da fila
            message, address = udp_message_queue.get()
            # Processa a mensagem como desejado
            print(f"Processando mensagem UDP de {address}: {message}")
            # Aqui você pode adicionar a lógica para processar a mensagem UDP

# Função para aguardar a entrada do teclado
def wait_for_input():
    input("Pressione ENTER para fechar o servidor...")
    print("Encerrando o servidor...")
    sys.exit()

def main():
    # Configuração do socket TCP
    tcp_socket.bind((SERVER_IP, SERVER_PORT_TCP))
    tcp_socket.listen(5)
    print("Servidor TCP aguardando conexões...")

    # Configuração do socket UDP
    udp_socket.bind((SERVER_IP, SERVER_PORT_UDP))
    print("Servidor UDP aguardando mensagens...")

    #Inicia uma thread para armazenar as mensagens Udp em uma Fila
    udp_thread = threading.Thread(target=handle_udp_connection, args=(udp_socket,))
    udp_thread.start()

    # Inicia uma thread para processar as mensagens UDP
    process_udp_thread = threading.Thread(target=process_udp_messages)
    process_udp_thread.start() 
    
    # Aceita conexões TCP e inicia uma thread para cada cliente
    while True: 
        client_socket, address = tcp_socket.accept() 
        tcp_thread = threading.Thread(target=handle_tcp_connection, args=(client_socket, address, i))
        tcp_thread.start() 

if __name__ == "__main__":
    main()