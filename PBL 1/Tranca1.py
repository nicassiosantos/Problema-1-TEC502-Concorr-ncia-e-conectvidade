import socket

TCP_HOST = 'localhost'
TCP_PORT = 12345

UDP_HOST = 'localhost'
UDP_PORT = 54321

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.connect((TCP_HOST, TCP_PORT))

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

estado_porta = 'Destrancada'  # Inicialmente a porta está destrancada

def send_message_udp(message):
    udp_socket.sendto(message.encode(), (UDP_HOST, UDP_PORT))

def set_estado_porta(novo_estado):
    global estado_porta
    estado_porta = novo_estado
    print("Estado atual da porta:", estado_porta)

while True:
    command = input("Enter command (Trancar, Destrancar, Estado): ")
    tcp_socket.sendall(command.encode())
    
    data = tcp_socket.recv(1024).decode()
    print("Received from broker:", data)
    
    if command == 'Trancar':
        set_estado_porta('Trancada')
        send_message_udp("Porta trancada")
        print("Trancou")
    elif command == 'Destrancar':
        set_estado_porta('Destrancada')
        send_message_udp("Porta destrancada")
        print("Destrancou")
    elif command == 'Estado':
        print("Enviando estado atual da porta para o broker:", estado_porta)
        tcp_socket.sendall(estado_porta.encode())
