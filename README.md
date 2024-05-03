# Problema-1-Internet das coisas

## Sistema de Controle de Trancas de Portas

Este é um sistema que permite controlar trancas de portas remotamente por meio de um broker central. Consiste em três componentes principais:

1. **Broker**: O servidor central responsável por coordenar a comunicação entre os dispositivos de controle de trancas de portas e os clientes que desejam interagir com esses dispositivos.

2. **Dispositivo de Tranca de Porta**: Um dispositivo físico que simula uma tranca de porta e se conecta ao broker para receber comandos de controle e enviar informações sobre o estado da porta.

3. **Cliente**: Uma interface web que permite aos usuários enviar comandos para as trancas de porta e visualizar informações sobre os dispositivos conectados.

## Funcionamento do Sistema

1. **Broker**:
   - O broker é o ponto central do sistema e deve ser iniciado primeiro.
   - Ele escuta as conexões dos dispositivos de tranca de porta e dos clientes em portas específicas.
   - Quando um dispositivo ou cliente se conecta, o broker gerencia a comunicação entre eles, encaminhando mensagens conforme necessário.

2. **Dispositivo de Tranca de Porta**:
   - O dispositivo de tranca de porta é simulado por meio de software e pode ser executado em um computador ou dispositivo compatível.
   - Ele se conecta ao broker por meio de uma conexão TCP para receber comandos de controle e enviar atualizações sobre o estado da porta.
   - O dispositivo de tranca de porta também pode ser controlado manualmente por meio de um menu de controle local.

3. **Cliente**:
   - O cliente é uma interface web acessível por meio de um navegador.
   - Permite aos usuários visualizar a lista de trancas de portas conectadas e enviar comandos para essas trancas, como destrancar, trancar, ligar e desligar.
   - Os clientes podem atualizar automaticamente a lista de dispositivos conectados a cada dois segundos.

## Como Utilizar os Produtos

### 1. Iniciando o Broker:

- Execute o código do broker em um ambiente compatível com Python.
- Certifique-se de que o broker esteja configurado com o endereço IP e as portas corretas para aguardar conexões de dispositivos e clientes.

### 2. Iniciando o Dispositivo de Tranca de Porta:

- Execute o código do dispositivo de tranca de porta em um ambiente compatível com Python.
- Certifique-se de que o dispositivo esteja configurado com o endereço IP e a porta correta do broker para se conectar.
- O dispositivo começará a simular o estado da porta e enviará atualizações ao broker.

### 3. Acessando o Cliente:

- Abra o arquivo HTML do cliente em um navegador da web.
- Certifique-se de que o cliente esteja configurado com o endereço IP e a porta correta do broker para enviar comandos.
- Use os botões na interface do cliente para interagir com as trancas de portas conectadas, como destrancar, trancar, ligar e desligar.
