import socket 
import threading 
import time 
import random 

SERVER_IP = '127.0.0.1'
SERVER_PORT_TCP = 12345
SERVER_PORT_UDP = 54321
HEADERSIZE = 10

Tranca = {'Estado': 'Fechada', 
          'Trava': 'Destrancada', 
          'TempoAberta': '0', 
          }

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Funcao resposável por conectar a tranca ao servidor via TCP
def try_connect_broker_tcp(server_ip, server_port_tcp): 
    try: 
        #Tenta conectar ao servidor 
        tcp_socket.connect((SERVER_IP, SERVER_PORT_TCP)) 
        print("Sucesso ao conectar")
    except socket.error as e:
        print(f"Falha ao conectar ao servidor via TCP: {e}")  

#Funcao responsavel por enviar uma mensagem via udp
def send_message_udp(mensagem, server_ip, server_port_udp): 
    try: 
        #Tenta enviar mensagem ao servidor via UDP
        udp_socket.sendto(mensagem.encode(), (server_ip, server_port_udp)) 
        print("Sucesso ao enviar mensagem via UDP")
    except socket.error as e:
        print(f"Falha ao enviar mensagem via UDP: {e}")

#Função responsavél por receber mensagens do servidor
def handling_message_tcp(): 
    try: 
        mensagem_completa = ''
        nova_msg = True
        
        mensagem = tcp_socket.recv(1024)
        if nova_msg: 
            print(f"tamanho da mensagem: { mensagem[:HEADERSIZE]}")
            tamanho_msg = int(mensagem[:HEADERSIZE])
            nova_msg = False 

        mensagem_completa += mensagem.decode('utf-8') 
        print(f"Mensagem recebida: {mensagem_completa}")  

        if len(mensagem_completa)-HEADERSIZE == tamanho_msg: 
            print("Recebimento da mensagem completa")
            print(tamanho_msg)  

        mensagem_completa = mensagem_completa[10:] 
        print(f"Mensagem cortada >{mensagem_completa}<") 

    except Exception as e: 
        print(f"Falha ao receber mensagem: {e}")
    finally:
        # Fecha o socket ao finalizar a thread
        tcp_socket.close()


#Função responsavél por 


#Função responsavél por aleatorizar o estado da porta 
def door_randomization(): 
    print()

    #Gera um intervalo em 

#Função responssavél por tratar mensagens que chegam a Tranca e mandar uma resposta de acordo 
def messsage_receiver(mensagem): 

    if mensagem == "0": 
        if Tranca['Estado'] == "Fechada": 
            Tranca['Trava'] = "Trancada"




def main():
    #Conexão da Tranca com o broker 
    try_connect_broker_tcp(SERVER_IP, SERVER_PORT_TCP) 

    # Cria e inicia a thread para recebimento de mensagens
    receive_thread = threading.Thread(target=handling_message_tcp, args=())
    receive_thread.start()

    # Aguarda a thread de recebimento de mensagens terminar
    receive_thread.join() 

    # Exemplo de envio de mensagem via UDP
    mensagem_udp = "Mensagem que enviei via UDP"
    send_message_udp(mensagem_udp, SERVER_IP, SERVER_PORT_UDP) 

    while True:
        try:
            # Alguma lógica adicional pode ser colocada aqui
            pass
        except KeyboardInterrupt:
            print("Encerrando o programa...")
            # Ao detectar um sinal de interrupção (Ctrl+C), encerra as threads e fecha o socket
            receive_thread.join()
            tcp_socket.close()
            udp_socket.close()
            break
    


if __name__ == "__main__":
    main()


