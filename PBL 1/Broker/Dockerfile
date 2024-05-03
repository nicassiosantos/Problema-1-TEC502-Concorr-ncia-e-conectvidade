# Use a imagem base do Python
FROM python:3.8-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /Broker

# Copia os arquivos necessários para o contêiner
COPY Broker.py ./

# Instala as dependências e remove os arquivos temporários em uma única camada
RUN pip install Flask
RUN pip install flask-cors
    

# Define as variáveis de ambiente
ENV SERVER_IP=127.0.0.1
ENV SERVER_PORT_TCP=12346
ENV SERVER_PORT_UDP=54323
ENV HTTP_PORT=4587


# Comando para iniciar a aplicação Flask
CMD ["python", "Broker.py"]