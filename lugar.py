import socket
import threading
import time
import random

CAPACIDADE = 25
PO = 0.3  # Probabilidade de passar a ocupado
PL = 0.2  # Probabilidade de passar a livre
N = 5     # Intervalo em segundos

# Códigos ANSI para cores
VERDE = "\033[92m"
VERMELHO = "\033[91m"
RESET = "\033[0m"

class Lugar(threading.Thread):
    def _init_(self, host, port):
        super()._init_()
        self.host = host
        self.port = port
        self.id_lugar = None
        self.estado = 'livre'
        self.estado_anterior = None

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((self.host, self.port))
                print(f"Ligado ao servidor {self.host}:{self.port}")
            except ConnectionRefusedError:
                print("Falha ao conectar com o servidor.")
                return

            # Solicitar ID único
            s.sendall(b'REQ_ID\n')
            resp = s.recv(1024).decode().strip()
            if resp.startswith("ID"):
                self.id_lugar = int(resp.split()[1])
                print(f"Resposta de registo: ACK (ID {self.id_lugar})")
            else:
                print(f"Falha ao iniciar lugar: {resp}")
                return

            while True:
                time.sleep(N)
                # Simular mudança de estado
                if self.estado == 'livre' and random.random() < PO:
                    self.estado = 'ocupado'
                elif self.estado == 'ocupado' and random.random() < PL:
                    self.estado = 'livre'

                # Enviar atualização
                try:
                    s.sendall(f"UPDATE {self.id_lugar} {self.estado}\n".encode())
                    resposta = s.recv(1024).decode().strip()
                    if self.estado != self.estado_anterior:
                        cor = VERDE if self.estado == 'livre' else VERMELHO
                        print(f"Resposta: {resposta} | Lugar {self.id_lugar} estado: {cor}{self.estado.upper()}{RESET}")
                        self.estado_anterior = self.estado
                    else:
                        print(f"Resposta: {resposta}")
                except:
                    print(f"Lugar {self.id_lugar} perdeu conexão com o servidor.")
                    break

if _name_ == "_main_":
    lugares = []
    for _ in range(CAPACIDADE):
        lugar = Lugar('127.0.0.1', 5000)
        lugar.start()
        lugares.append(lugar)