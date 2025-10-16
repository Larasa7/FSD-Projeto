Parque # parque_final.py
import socket
import threading

CAPACIDADE = 25  # Capacidade mínima

class ParqueEstacionamento:
    def _init_(self, nome, latitude, longitude, tarifa_base, tarifa_hora, tarifa_maxima):
        self.nome = nome
        self.latitude = latitude
        self.longitude = longitude
        self.tarifa_base = tarifa_base
        self.tarifa_hora = tarifa_hora
        self.tarifa_maxima = tarifa_maxima
        self.capacidade = CAPACIDADE
        self.lugares = {}  # id: estado ('livre' ou 'ocupado')
        self.next_id = 1
        self.lock = threading.Lock()

    def atribuir_id(self):
        with self.lock:
            if len(self.lugares) >= self.capacidade:
                return None
            _id = self.next_id
            self.next_id += 1
            self.lugares[_id] = 'livre'
            return _id

    def atualizar_estado(self, lugar_id, estado):
        with self.lock:
            if lugar_id in self.lugares and estado in ['livre', 'ocupado']:
                self.lugares[lugar_id] = estado
                return True
            return False

    def status_parque(self):
        with self.lock:
            return {
                "nome": self.nome,
                "latitude": self.latitude,
                "longitude": self.longitude,
                "tarifa_base": self.tarifa_base,
                "tarifa_hora": self.tarifa_hora,
                "tarifa_maxima": self.tarifa_maxima,
                "lugares": self.lugares.copy()
            }

def handle_client(conn, parque):
    try:
        while True:
            data = conn.recv(1024).decode().strip()
            if not data:
                break

            if data == 'REQ_ID':
                id_lugar = parque.atribuir_id()
                if id_lugar:
                    conn.send(f"ID {id_lugar}\n".encode())
                    print(f"Lugar {id_lugar} registrado.")
                else:
                    conn.send("ERROR parque cheio\n".encode())

            elif data.startswith('UPDATE'):
                parts = data.split()
                if len(parts) != 3:
                    conn.send("ERROR comando inválido\n".encode())
                    continue
                _, lugar_id, estado = parts
                try:
                    lugar_id = int(lugar_id)
                    if parque.atualizar_estado(lugar_id, estado):
                        conn.send("ACK\n".encode())
                        # Exibir estado completo do parque
                        status = parque.status_parque()
                        print(f"Estado atualizado do Lugar {lugar_id} para {estado}.")
                        print("Estado atual de todos os lugares:")
                        for lid, est in status['lugares'].items():
                            print(f"  Lugar {lid}: {est}")
                    else:
                        conn.send("ERROR id inválido\n".encode())
                except ValueError:
                    conn.send("ERROR comando inválido\n".encode())
            else:
                conn.send("ERROR comando inválido\n".encode())
    finally:
        conn.close()

def servidor_parque(host='0.0.0.0', port=5000):
    parque = ParqueEstacionamento(
        nome="Parque Central",
        latitude=38.736946,
        longitude=-9.142685,
        tarifa_base=2.0,
        tarifa_hora=1.5,
        tarifa_maxima=10.0
    )

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print("Servidor do Parque a correr...")
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, parque), daemon=True).start()

if _name_ == "_main_":
    servidor_parque()