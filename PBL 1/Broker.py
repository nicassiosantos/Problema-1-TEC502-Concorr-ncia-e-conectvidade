import socket
import threading
import sys 


tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

SERVER_IP = '127.0.0.1' 
SERVER_PORT_TCP = 12345
SERVER_PORT_UDP = 54321

# Dicionários para armazenar os IPs dos dispositivos conectados
tcp_clients = {}
udp_clients = {}

HEADERSIZE = 10


# Função para lidar com conexões TCP
def handle_tcp_connection(client_socket, address): 
    print(f"Conexão TCP estabelecida com {address}")
    # Armazena o IP do cliente TCP no dicionário tcp_clients
    tcp_clients[address[0]] = address[1]
    # Imprime o dicionário de clientes TCP
    print("Clientes TCP:", tcp_clients)

    msg = "Conexão realizada"
    msg = f'{len(msg):<{HEADERSIZE}}' + msg 

    client_socket.send(bytes("Conexão realizada", "utf-8"))


    
    #while True:
        #data = client_socket.recv(1024)
        #if not data:
            #break
        #print(f"Mensagem TCP de {address}: {data.decode('utf-8')}")
        # Aqui você pode adicionar a lógica para responder a mensagens TCP, se necessário
    
    #client_socket.send(bytes("Conexão Estabelecida", "utf-8")) 
    #print("mensagem enviada") 
    #print(f"Conexão TCP com {address} fechada")
    

# Função para lidar com conexões UDP
def handle_udp_connection(udp_socket):
    print("Aguardando mensagens UDP...")
    while True:
        data, address = udp_socket.recvfrom(1024)
        print(f"Mensagem UDP de {address}: {data.decode('utf-8')}")
        # Armazena o IP do cliente UDP no dicionário udp_clients
        udp_clients[address[0]] = address[1]
        # Imprime o dicionário de clientes UDP
        print("Clientes UDP:", udp_clients)

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

    # Inicia uma thread para lidar com conexões UDP
    udp_thread = threading.Thread(target=handle_udp_connection, args=(udp_socket,))
    udp_thread.start()

    # Inicia uma thread para aguardar a entrada do teclado
    input_thread = threading.Thread(target=wait_for_input)
    input_thread.start()

    # Aceita conexões TCP e inicia uma thread para cada cliente
    while True:
        client_socket, address = tcp_socket.accept()
        tcp_thread = threading.Thread(target=handle_tcp_connection, args=(client_socket, address))
        tcp_thread.start()

if __name__ == "__main__":
    main()