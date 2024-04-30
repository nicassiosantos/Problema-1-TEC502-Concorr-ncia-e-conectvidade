from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import socket
import threading

app = FastAPI()

SERVER_IP = '127.0.0.1'
SERVER_PORT_TCP = 12345

# Modelo para os dados da requisição
class Command(BaseModel):
    command: str

# Função para enviar mensagem TCP para o servidor
async def send_tcp_message(message):
    try:
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.connect((SERVER_IP, SERVER_PORT_TCP))
        tcp_socket.sendall(message.encode())
        response = tcp_socket.recv(1024)
        tcp_socket.close()
        return response.decode()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao enviar mensagem TCP: {e}")

# Rota para enviar comando ao servidor
@app.post("/send-command/")
async def send_command(command: Command):
    response = await send_tcp_message(command.command)
    return {"success": True, "response": response}

def run_api():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    # Roda a API em uma thread separada para que continue executando
    api_thread = threading.Thread(target=run_api)
    api_thread.start()