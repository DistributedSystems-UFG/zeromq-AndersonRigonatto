[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/wa7oHGos)

# ZeroMQ – Tarefa Individual ASR 09

Exemplos adaptados de Tanenbaum & van Steen (2025) para ilustrar três padrões
de comunicação com ZeroMQ: **client-server**, **pub-sub** e **producer-consumer**.

Os arquivos originais (`zmq_client-server.py`, `zmq_pub-sub.py`,
`zmq_producer-worker.py`, `tasksrc.py`, `taskwork.py`, `constPipe.py`) foram
mantidos como referência. As novas implementações desta tarefa estão ao lado
deles.

## O que mudou em cada exemplo

- **client-server**: a aplicação base apenas anexava `*` à mensagem. Agora o
  servidor é uma calculadora — recebe operações `ADD/SUB/MUL/DIV` no formato
  `"OP A B"` e responde com o resultado. O cliente envia uma sequência fixa de
  5 operações e encerra com `STOP`.
- **pub-sub**: o exemplo original publicava um único tópico (`TIME`). O novo
  publisher emite leituras aleatórias em **três tópicos** (`TEMP`, `PRESS`,
  `HUM`) e o subscriber escolhe via CLI qual deles assinar, demonstrando a
  filtragem por tópico do ZMQ.
- **pipeline producer-consumer**: o original tinha 2 estágios (producer →
  worker). Agora há **3 estágios**:
  `producer → worker (eleva ao quadrado) → consumer (agrega min/max/soma/média)`.
  Cada estágio roda em uma máquina distinta.

## Execução em máquinas distintas (AWS EC2)

Três instâncias EC2 (Ubuntu 22.04/24.04, `t2.micro`), todas no mesmo Security
Group com as portas TCP **5555, 5556, 5557, 5558** abertas em inbound, além de
SSH (22).

Em cada instância:

```bash
sudo apt update && sudo apt install -y python3-pip git
pip install pyzmq --break-system-packages
git clone <URL_DESTE_REPO>
cd zeromq-AndersonRigonatto
```

### Distribuição de papéis

| Exemplo         | HostA (bind)        | HostB                                | HostC (opcional)                          |
| --------------- | ------------------- | ------------------------------------ | ----------------------------------------- |
| client-server   | `server.py`         | `client.py <HostA-IP>`               | —                                         |
| pub-sub         | `publisher.py`      | `subscriber.py <HostA-IP> TEMP`      | `subscriber.py <HostA-IP> PRESS` (extra)  |
| pipeline (3)    | `producer.py`       | `worker.py <HostA-IP>`               | `consumer.py <HostB-IP>`                  |

### Comandos prontos

**client-server**

```bash
# HostA
cd client-server && python3 server.py

# HostB
cd client-server && python3 client.py <HostA-IP>
```

**pub-sub**

```bash
# HostA
cd pub-sub && python3 publisher.py

# HostB
cd pub-sub && python3 subscriber.py <HostA-IP> TEMP

# HostC (opcional, mostra filtragem por tópico)
cd pub-sub && python3 subscriber.py <HostA-IP> PRESS
```

**pipeline (subir do fim pro começo para não perder mensagens iniciais)**

```bash
# HostC
cd pipeline_producer-consumer && python3 consumer.py <HostB-IP>

# HostB
cd pipeline_producer-consumer && python3 worker.py <HostA-IP>

# HostA
cd pipeline_producer-consumer && python3 producer.py
```

## Evidências de execução

Prints da execução de cada um dos três experimentos serão anexados abaixo:

- client-server: _print pendente_
- pub-sub: _print pendente_
- pipeline: _print pendente_
