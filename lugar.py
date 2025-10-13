import socket
import json
import time
import random
import logging
# etfgrh
# Configuração do logging (para mostrar mensagens informativas)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# Parâmetros de ligação
HOST = "127.0.0.1"  # endereço do servidor (localhost)
PORT = 5000         # porta do servidor
INTERVALO = 3       # segundos entre cada atualização
PO = 0.3            # probabilidade de mudar de livre -> ocupado
PL = 0.2            # probabilidade de mudar de ocupado -> livre

def main():
    # 1️⃣ criar socket TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    logging.info(f"Ligado ao servidor {HOST}:{PORT}")

    # converter o socket em streams de leitura e escrita
    reader = s.makefile('r', encoding='utf-8')
    writer = s.makefile('w', encoding='utf-8')

    # 2️⃣ enviar pedido de registo
    pedido = {"type": "REGISTER"}
    writer.write(json.dumps(pedido) + "\n")
    writer.flush()

    resposta = reader.readline()
    if not resposta:
        logging.error("Servidor fechou a ligação.")
        return

    logging.info(f"Resposta de registo: {resposta.strip()}")

    # 3️⃣ simular estado do lugar (livre/ocupado)
    estado = "free"

    while True:
        time.sleep(INTERVALO)

        # simular mudança de estado com base nas probabilidades
        if estado == "free" and random.random() < PO:
            estado = "occupied"
        elif estado == "occupied" and random.random() < PL:
            estado = "free"

        # 4️⃣ enviar atualização
        msg = {
            "type": "UPDATE",
            "sensor_id": "TEMP-ID",  # mais tarde o servidor pode atribuir um ID
            "state": estado,
            "ts": time.time()
        }
        writer.write(json.dumps(msg) + "\n")
        writer.flush()

        # 5️⃣ ler resposta do servidor
        resposta = reader.readline()
        if not resposta:
            logging.warning("Servidor fechou a ligação.")
            break

        logging.info(f"Resposta: {resposta.strip()}")

if __name__ == "__main__":
    main()
