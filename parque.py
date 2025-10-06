import socketserver, threading, json, time, logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

class ParkHandler(socketserver.StreamRequestHandler):
    def handle(self):
        logging.info(f"Nova ligação de {self.client_address}")
        while True:
            data = self.rfile.readline()
            if not data:
                break
            msg = data.decode().strip()
            logging.info(f"Recebido: {msg}")
            self.wfile.write(b"ACK\n")
        logging.info("Ligação terminada")

class ThreadedTCPServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 5000
    server = ThreadedTCPServer((HOST, PORT), ParkHandler)
    logging.info(f"Servidor Parque a correr em {HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logging.info("Encerrando servidor...")
        server.shutdown()
        server.server_close()
