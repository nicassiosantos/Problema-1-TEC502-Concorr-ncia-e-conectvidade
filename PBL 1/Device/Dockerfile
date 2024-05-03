# Use a imagem base do Python
FROM python:3.8-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /Device

# Copia os arquivos necessários para o contêiner
COPY Tranca.py ./

# Define as variáveis de ambiente
ENV SERVER_IP=127.0.0.1
ENV SERVER_PORT_TCP=12346
ENV SERVER_PORT_UDP=54323


# Comando para iniciar a aplicação Flask
CMD ["python", "Tranca.py"]