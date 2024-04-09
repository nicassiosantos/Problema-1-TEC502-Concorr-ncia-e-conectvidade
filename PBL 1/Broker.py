import socket
import threading

TCP_HOST = 'localhost'
TCP_PORT = 12345

UDP_HOST = 'localhost'
UDP_PORT = 54321

devices = {}

def handle_tcp_connection(client_socket, address):
    print(f"Device connected: {address}")
    
    while True:
        message = client_socket.recv(1024).decode('utf-8')
        print(message)
        if message == 'Trancar':
            print("Received command to lock the door")
            # Aqui você pode adicionar a lógica para trancar a porta
            devices[address] = 'Trancada'
        elif message == 'Destrancar':
            print("Received command to unlock the door")
            # Aqui você pode adicionar a lógica para destrancar a porta
            devices[address] = 'Destrancada'
        elif message == 'Estado':
            print("Received request to get the current state of the door")
            # Aqui você pode adicionar a lógica para enviar o estado atual da porta
            current_state = devices.get(address, 'Desconhecido')
            client_socket.sendall(current_state.encode())
        else:
            print("Unknown command received")

def handle_udp():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        udp_socket.bind((UDP_HOST, UDP_PORT))
        
        print(f"Listening for UDP messages at {UDP_HOST}:{UDP_PORT}")
        
        while True:
            data, address = udp_socket.recvfrom(1024)
            message = data.decode('utf-8')
            print(f"Received UDP message from {address}: {message}")

def main():
    # Thread para lidar com mensagens UDP
    udp_thread = threading.Thread(target=handle_udp)
    udp_thread.start()

    # TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
        tcp_socket.bind((TCP_HOST, TCP_PORT))
        tcp_socket.listen(5)
        
        print(f"Broker started at {TCP_HOST}:{TCP_PORT}")
        
        while True:
            client_socket, address = tcp_socket.accept()
            
            tcp_thread = threading.Thread(target=handle_tcp_connection, args=(client_socket, address))
            tcp_thread.start()

if __name__ == "__main__":
    main()

