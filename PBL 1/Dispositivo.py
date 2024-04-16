import socket

# Endereço IP e porta do servidor
SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345

# Mensagem a ser enviada para o servidor
MESSAGE = "Olá, servidor!"

# Função para enviar a mensagem para o servidor
def send_message_to_server():
    try:
        # Cria o socket TCP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            # Conecta ao servidor
            client_socket.connect((SERVER_IP, SERVER_PORT))
            # Envia a mensagem
            client_socket.sendall(MESSAGE.encode())
            print("Mensagem enviada com sucesso para o servidor.")
    except Exception as e:
        print("Erro ao enviar mensagem para o servidor:", e)

# Função principal
def main():
    send_message_to_server()

if __name__ == "__main__":
    main()
