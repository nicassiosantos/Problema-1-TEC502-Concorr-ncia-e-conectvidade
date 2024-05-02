from flask import Flask, request, jsonify
from flask_cors import CORS
import socket
import threading
import sys 
import time
import queue 

app = Flask(__name__)
CORS(app)
global msg 
msg = ''

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

SERVER_IP = '127.0.0.1' 
SERVER_PORT_TCP = 12345
SERVER_PORT_UDP = 54321 

# Dicionários para armazenar os IPs dos dispositivos conectados
tcp_clients = []
HEADERSIZE = 10

# Fila para armazenar mensagens UDP
udp_message_queue = queue.Queue()
http_messages = queue.Queue()

# Função para lidar com conexões TCP
def Registrando_dispositivos_TCP(client_socket, address): 
    print(f"Conexão TCP estabelecida com {address}")
    dispositivo = {"socket": client_socket, "ip": address[0],  "porta_tcp": address[1], "estado": "", "trava": "desligada", "tempo_aberta": "0"}
    tcp_clients.append(dispositivo)
    print("Clientes TCP:", tcp_clients) 

# Função para verificar a conexão dos dispositivos TCP
def verificar_conexao_dispositivos():
    while True:
        for dispositivo in tcp_clients:
            try:
                print(f"Tentando verificar conexão com {dispositivo['ip']}:{dispositivo['porta_tcp']}...")
                # Enviar uma mensagem de verificação para o dispositivo
                dispositivo['socket'].send(bytes("Verificando",'utf-8'))
            except Exception as e:
                print(f"Erro: {e}")
                print(f"Conexão perdida com {dispositivo['ip']}:{dispositivo['porta_tcp']}")
                tcp_clients.remove(dispositivo)
                print("Clientes TCP atualizados:", tcp_clients)
        
        # Aguardar um tempo antes da próxima verificação
        time.sleep(10)  # Verificar a conexão a cada 60 segundos 

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
                    if dipositivo['ip'] == address[0]: 
                        dipositivo["estado"] = estado
                        dipositivo["trava"] = trava
                        dipositivo["tempo_aberta"] = tempo_aberta 


# Função para processar as mensagens recebidas via HTTP
def process_http_messages():
    while True:
        if not http_messages.empty():
            message = http_messages.get()
            partes = message.split("-")
            comando = partes[0] 
            ip_dispositivo = partes[1] 
            porta = int(partes[2]) 
            comando_dispositivo = partes[3]
            # Enviar a mensagem para os dispositivos TCP conectados
            for dispositivo in tcp_clients:
                if comando == "comando_para_dispositivo":
                    if dispositivo["ip"] == ip_dispositivo and dispositivo["porta_tcp"] ==  porta: 
                        mensagem = f"comando-{comando_dispositivo}"
                        dispositivo["socket"].send(mensagem.encode())  
                        msg = Recebimento_mensagem(dispositivo["socket"])

#Função responsável por verificar o recebimento de mensagens de resposta
def Recebimento_mensagem(socket): 
    try: 
        global msg 
        msg = socket.recv(1024).decode('utf-8') 
        return msg
    except Exception as e: 
        print(f"Erro ao processar mensagem TCP: {e}")
        time.sleep(3)

# Função para armazenar as mensagens recebidas via HTTP
@app.route("/send-message/", methods=["POST"])
def send_message():
    try:
        data = request.json
        message = data.get("message")
        # Coloca a mensagem na fila de mensagens HTTP
        http_messages.put(message)
        print("Mensagem recebida via HTTP:", message) 
        time.sleep(0.5)
        print("Mensagem recebida pelo dispositivo", msg)
        return jsonify({"success": True, "message": "Mensagem enviada com sucesso"}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    
# Função para obter a lista de dispositivos TCP
@app.route("/tcp-clients/", methods=["GET"])
def get_tcp_clients():
    try:
        # Criar uma lista de dicionários com informações dos dispositivos TCP
        devices_info = []
        for device in tcp_clients:
            device_info = {
                "ip": device["ip"],
                "porta_tcp": device["porta_tcp"],
                "estado": device["estado"],
                "trava": device["trava"],
                "tempo_aberta": device["tempo_aberta"]
            }
            devices_info.append(device_info)
        
        return jsonify({"success": True, "devices": devices_info}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    
def start_flask_server():
    app.run(host=SERVER_IP, port=5000)

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
        udp_thread.daemon = True
        udp_thread.start()

        # Inicia uma thread para processar as mensagens UDP
        process_udp_thread = threading.Thread(target=process_udp_messages)
        process_udp_thread.daemon = True
        process_udp_thread.start() 

        # Inicia uma thread para processar as mensagens HTTP
        http_thread = threading.Thread(target=process_http_messages)
        http_thread.daemon = True
        http_thread.start()
        
        verificar_conexao_thread = threading.Thread(target=verificar_conexao_dispositivos)
        verificar_conexao_thread.daemon = True  # Define a thread como um daemon para que ela seja encerrada quando o programa principal terminar
        verificar_conexao_thread.start() 

        # Aceita conexões TCP e inicia uma thread para cada cliente
        while True: 
            client_socket, address = tcp_socket.accept() 
            tcp_thread = threading.Thread(target=Registrando_dispositivos_TCP, args=(client_socket, address))
            tcp_thread.start()  

    except Exception as e: 
         print(f"Erro durante a execução do servidor: {e}")
if __name__ == "__main__":
    flask_thread = threading.Thread(target=start_flask_server)
    flask_thread.start()
    main()