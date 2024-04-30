import requests

# URL do servidor Flask
url = "http://127.0.0.1:5000/receive-message/"

# Função para enviar um comando para o servidor
def send_command(command):
    try:
        data = {"message": command}
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            return {"success": False, "message": "Erro ao enviar o comando"}
    except Exception as e:
        return {"success": False, "message": str(e)}

# Exemplo de uso
if __name__ == "__main__":
    command = input("Digite o comando a ser enviado para o servidor: ")
    result = send_command(command)
    print("Resposta do servidor:", result)