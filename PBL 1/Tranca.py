import socket 
import threading 
import time 
import random 

SERVER_IP = '127.0.0.1'
SERVER_PORT_TCP = 12346
SERVER_PORT_UDP = 54323




udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

Porta = {'Estado': 'fechada', 
          'Trava': 'destrancada', 
          'TempoAberta': 0,
          'Ligar': 'false' 
          }
  

#Funcao resposável por conectar a tranca ao servidor via TCP
def tente_conectar_broker_tcp(server_ip, server_port_tcp): 
    while True:
        try: 
            #Tenta conectar ao servidor 
            global tcp_socket
            tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp_socket.connect((server_ip, server_port_tcp)) 
            tcp_socket.settimeout(15)
            print("Sucesso ao conectar") 
            break
        except socket.error as e:
            if hasattr(e, 'winerror') and e.winerror == 10061:
                print("O Servidor ainda não está no ar")
                time.sleep(3)
                print("Tentando Reconexão...")
            else:
                print("O Servidor ainda não está no ar")
                time.sleep(3)
                print("Tentando Reconexão...")  

#Funcao responsavel por enviar uma mensagem via udp
def envio_mensagem_udp(mensagem, server_ip, server_port_udp): 
    try: 
        #Tenta enviar mensagem ao servidor via UDP
        udp_socket.sendto(mensagem.encode(), (server_ip, server_port_udp)) 
    except socket.error as e:
        print(f"Falha ao enviar mensagem via UDP: {e}") 

#Função responsavél por receber mensagens do servidor
def tratando_mensagens_tcp(): 
    while True:
        try:
            mensagem = tcp_socket.recv(1024).decode('utf-8')
            if not mensagem:
                break
            partes = mensagem.split('-')
            receptor_mensagens(partes)
        except ConnectionResetError:
            print("A conexão com o servidor foi redefinida pelo servidor. Aguarde o servidor estar no ar novamente") 
            tente_conectar_broker_tcp(SERVER_IP, SERVER_PORT_TCP)
        except Exception as e:
            print(f"Erro ao processar mensagem TCP: {e}")
            tente_conectar_broker_tcp(SERVER_IP, SERVER_PORT_TCP)
            time.sleep(3) 



# Função para simular a abertura e fechamento da porta
def simular_porta():
    def simular():
        while True:
            if Porta['Ligar'] == 'true':
                if Porta['Trava'] == 'destrancada': 
                    Porta['Estado'] = random.choice(["aberta", "fechada"])
                time.sleep(random.uniform(4, 8))  # Tempo aleatório antes de alterar o estado da porta
    thread = threading.Thread(target=simular)
    thread.daemon = True
    thread.start() 


#Função responsavél por verificar e fazer a contagem do tempo da porta no momento que ela é aberta 
def observar_porta():
    def monitorar():
        inicio_contagem = 0
        while True:
            if Porta['Ligar'] == 'true':
                if Porta['Estado'] == 'fechada':
                    Porta['TempoAberta'] = 0 
                    # Espera até que a porta seja aberta
                    while Porta['Estado'] == "fechada":
                        time.sleep(1)  # Verifica a cada segundo
                    inicio_contagem = time.time()  # Inicia a contagem de tempo
                elif Porta['Estado'] == "aberta":
                    if inicio_contagem == 0:
                        inicio_contagem = time.time()  # Inicia a contagem de tempo
                    Porta['TempoAberta'] = time.time() - inicio_contagem
                    # Espera até que a porta seja fechada
                    while Porta['Estado'] == "aberta":
                        Porta['TempoAberta'] = time.time() - inicio_contagem
                        time.sleep(1)  # Verifica a cada segundo 
                    inicio_contagem = 0
    thread = threading.Thread(target=monitorar)
    thread.daemon = True
    thread.start()

#Função responsavél por tratar mensagens que chegam a Tranca e mandar uma resposta de acordo 
def receptor_mensagens(partes): 
    tipo_mensagem = partes[0]
    if tipo_mensagem == 'comando':
        comando = partes[1]
        if comando == 'trancar':
            if Porta['Estado'] == "fechada": 
                Porta['Trava'] = "trancada"
                tcp_socket.send(bytes(f"comando_recebido-trancar-trancada-{Porta['Estado']}","utf-8"))
            else: 
                 tcp_socket.send(bytes(f"comando_recebido-trancar-destrancada-{Porta['Estado']}","utf-8"))
        elif comando == 'destrancar':
            if Porta['Trava'] == 'trancada': 
                Porta['Trava'] = "destrancada"
                tcp_socket.send(bytes(f"comando_recebido-destrancar-destrancada-{Porta['Estado']}","utf-8"))
            else:
                tcp_socket.send(bytes("comando_recebido-destrancar-destrancada-","utf-8"))
        elif comando == 'ligar': 
            if Porta['Ligar'] == 'false': 
                Porta['Ligar'] = 'true'
                tcp_socket.send(bytes(f"comando_recebido-ligar-ligada-{Porta['Estado']}","utf-8")) 
            else: 
                tcp_socket.send(bytes(f"comando_recebido-ligar-ligada-{Porta['Estado']}","utf-8"))
        elif comando == 'desligar': 
            if Porta['Ligar'] == 'true': 
                Porta['Ligar'] = 'false'
                tcp_socket.send(bytes(f"comando_recebido-desligar-ligada-{Porta['Estado']}","utf-8")) 
            else: 
                tcp_socket.send(bytes(f"comando_recebido-desligar-desligada-{Porta['Estado']}","utf-8"))

#Função responsável por tratar as mensagens vindas do menu de controle manual do dispositivo
def receptor_mensagens_menu(mensagem): 
    if mensagem == '0':
        if Porta['Estado'] == "fechada": 
            Porta['Trava'] = "trancada"
    elif mensagem == '1':
        if Porta['Trava'] == 'trancada': 
            Porta['Trava'] = "destrancada"
    elif mensagem == '2':
        if Porta['Ligar'] == 'false': 
            Porta['Ligar'] = "true"
    elif mensagem == '3':
        if Porta['Ligar'] == 'true': 
            Porta['Ligar'] = "false"
    
#Função do menu para controle manual da tranca
def menu_tranca(): 
    opcao = ""
    while opcao != "0" and opcao != "1" and opcao != '2' and opcao != '3':
        print("====Tranca Smart!=====")
        print("[0] Trancar")
        print("[1] Destrancar") 
        print("[2] Ligar")
        print("[3] Desligar")
        print("")
        opcao = input("Escolha sua opção: ")  
        if opcao != "0" and opcao != "1" and opcao != '2' and opcao != '3': 
            print("")
            print("Opção inválida por favor insira noavamente ") 
            print("")
            time.sleep(1)
    receptor_mensagens_menu(opcao)

#Função que envia informações do dispositivo para o broker a cada dois segundos
def envio_informações():
    def enviar(): 
        while True:
            if Porta['Ligar'] == 'true':
                estado = Porta["Estado"]
                trava = Porta["Trava"]
                tempo_aberta = Porta["TempoAberta"]
                mensagem = f"status-{estado}-{trava}-{tempo_aberta:.2f}"
                envio_mensagem_udp(mensagem, SERVER_IP, SERVER_PORT_UDP)
                time.sleep(2)  
            else: 
                mensagem = f"status- -desligada-0"
                envio_mensagem_udp(mensagem, SERVER_IP, SERVER_PORT_UDP)
                time.sleep(2)

    thread = threading.Thread(target=enviar)
    thread.daemon = True
    thread.start() 

def main():
    try:
        # Conexão da Tranca com o broker
        tente_conectar_broker_tcp(SERVER_IP, SERVER_PORT_TCP)

        # Cria e inicia a thread para recebimento de mensagens
        receive_thread = threading.Thread(target=tratando_mensagens_tcp, args=())
        receive_thread.daemon = True
        receive_thread.start()

        #Cria e inicia a thread que observa o estado da porta 
        observar_porta()

        #Cria e inicia a thread que aleatoriza o estado da porta para aberta e fechada
        simular_porta()

        #Cria e inicia a thread para enviar os dados do dispositvos para 
        envio_informações()

        while True:
            try:
                #Menu para controle manual da tranca 
                menu_tranca()
            except Exception as e:
                tcp_socket.close()
                udp_socket.close()
                break

    except Exception as e:
        print(f"Erro durante a execução do programa: {e}")
    


if __name__ == "__main__":
    main()


