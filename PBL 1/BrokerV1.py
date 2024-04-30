from flask import Flask, request, jsonify
import socket
import threading
import sys 
import time
import queue 

app = Flask(__name__)

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

SERVER_IP = '127.0.0.1' 
SERVER_PORT_TCP = 12345
SERVER_PORT_UDP = 54321 

# Dicionários para armazenar os IPs dos dispositivos conectados
tcp_clients = []
HEADERSIZE = 10
global msg 
msg = ""
global enviar
enviar = False


# Fila para armazenar mensagens UDP
udp_message_queue = queue.Queue()

# Função para lidar com conexões TCP
def handle_tcp_connection(client_socket, address, enviar): 
    print(f"Conexão TCP estabelecida com {address}")
    dispositivo = {"ip": address[0],  "porta_tcp": address[1], "estado": "0", "trava": "0", "tempo_aberta": "0"}
    tcp_clients.append(dispositivo)
    primeira = False 
    if dispositivo: 
        primeira = True
    print("Clientes TCP:", tcp_clients)

    while True:
        try:
            # Recebe a mensagem do cliente
            message = client_socket.recv(1024).decode()
            if enviar: 
                partes = msg.split("-")
                tipo = partes[0]
                device_ip = partes[1] 
                device_port = int(partes[2])
                comando = partes[3] 
                if (device_ip == address[0]) and (device_port == address[1]):
                    msg = f"{tipo}-{comando}" 
                    client_socket.send(msg.encode())
                    enviar = False
            if not message:
                break
            # Processar comando recebido do cliente e enviar para o dispositivo correspondente
            msg = message
            partes = msg.split('-')
            print(partes)
            if partes[0] == ("comando_para_dispositivo"):
                # Aqui você pode adicionar lógica para decidir qual dispositivo deve receber o comando
                device_ip = partes[1]
                device_port = partes[2] 
                msg = f"comando-{device_ip}-{device_port}-{partes[3]}" 
                enviar = True
                client_socket.send(bytes("Comando Recebido", "utf-8"))
            else:
                # Aqui você pode lidar com outros tipos de mensagens
                pass
        except Exception as e:
            print(f"Conexão com {address} encerrada.")
            print(f"Erro ao processar mensagem TCP 2: {e}")
            tcp_clients.remove(dispositivo)
            client_socket.close()  
            break
    time.sleep(1)  # Adicione um pequeno atraso antes de receber a próxima mensagem
    #print(f"Conexão com {address} encerrada.")
    #client_socket.close()
    
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
            #print(f"Processando mensagem UDP de {address}: {message}")
            partes = message.split('-') 
            tipo = partes[0] 
            estado = partes[1] 
            trava = partes[2] 
            tempo_aberta = partes[3] 
            if tipo == "status": 
                for dipositivo in tcp_clients: 
                    if (dipositivo['ip'] == address[0]) and (dipositivo['porta_tcp'] == address[1]):  
                        dipositivo["estado"] = estado
                        dipositivo["trava"] = trava
                        dipositivo["tempo_aberta"] = tempo_aberta 

            print(tcp_clients)

# Função para enviar mensagem TCP para um dispositivo específico
def send_tcp_message(device_ip, device_port, message):
    try:
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.connect((device_ip, device_port))
        tcp_socket.sendall(message.encode())
        response = tcp_socket.recv(1024)
        tcp_socket.close()
        return response.decode()
    except Exception as e:
        print(f"Erro ao enviar mensagem TCP 1: {e}")
        # Aqui você pode adicionar tratamento de erro, se necessário 

# Função para aguardar a entrada do teclado
def wait_for_input():
    input("Pressione ENTER para fechar o servidor...")
    print("Encerrando o servidor...")
    sys.exit()

def main():
    try:
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
            tcp_thread = threading.Thread(target=handle_tcp_connection, args=(client_socket, address, enviar))
            tcp_thread.start() 
    except Exception as e: 
         print(f"Erro durante a execução do servidor: {e}")
if __name__ == "__main__":
    main()