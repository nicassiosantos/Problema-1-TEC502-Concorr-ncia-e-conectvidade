import socket
import threading

SERVER_IP = '127.0.0.1'
TCP_PORT = 12345
UDP_PORT = 54321

# Função para lidar com conexões TCP
def handle_tcp_connection(client_socket, client_address):
    print(f"Conexão TCP estabelecida com {client_address}")
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        message = data.decode('utf-8')
        print(f"Mensagem TCP recebida de {client_address}: {message}")
        # Aqui você pode adicionar a lógica para processar a mensagem TCP, se necessário

    client_socket.close()
    print(f"Conexão TCP encerrada com {client_address}")

# Função para lidar com mensagens UDP
def handle_udp_messages():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((SERVER_IP, UDP_PORT))
    print(f"Servidor UDP aguardando mensagens em {SERVER_IP}:{UDP_PORT}")

    while True:
        data, address = udp_socket.recvfrom(1024)
        message = data.decode('utf-8')
        print(f"Mensagem UDP recebida de {address}: {message}")
        # Aqui você pode adicionar a lógica para processar a mensagem UDP, se necessário

# Função principal
def main():
    # Iniciando a thread para lidar com mensagens UDP
    udp_thread = threading.Thread(target=handle_udp_messages)
    udp_thread.start()

    # Iniciando o servidor TCP
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind((SERVER_IP, TCP_PORT))
    tcp_socket.listen(5)
    print(f"Servidor TCP aguardando conexões em {SERVER_IP}:{TCP_PORT}")

    while True:
        client_socket, client_address = tcp_socket.accept()
        # Iniciando uma nova thread para lidar com a conexão TCP
        tcp_connection_thread = threading.Thread(target=handle_tcp_connection, args=(client_socket, client_address))
        tcp_connection_thread.start()

if __name__ == "__main__":
    main()
