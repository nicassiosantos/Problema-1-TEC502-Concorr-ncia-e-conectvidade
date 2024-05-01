import requests

# URL base do servidor Flask
base_url = "http://127.0.0.1:5000"

# Função para obter a lista de dispositivos TCP
def get_tcp_clients():
    try:
        response = requests.get(f"{base_url}/tcp-clients/")
        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                devices = data["devices"]
                for device in devices:
                    print(device)  # Ou faça o que desejar com as informações dos dispositivos
            else:
                print("Erro:", data["message"])
        else:
            print("Erro:", response.status_code)
    except Exception as e:
        print("Erro ao fazer a solicitação:", str(e))

# Exemplo de utilização
get_tcp_clients() 


