import socket
import json

class NeuroSkyClient:
    def _init_(self, host='127.0.0.1', port=13854):
        self.host = host
        self.port = port
        self.sock = None

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        config = json.dumps({"enableRawOutput": False, "format": "Json"})
        self.sock.sendall((config + '\n').encode('utf-8'))
        print("[NeuroSkyClient] Conectado a NeuroSky MindWave")

    def read_data(self):
        if self.sock:
            buffer = b''
            while True:
                chunk = self.sock.recv(2048)
                buffer += chunk
                try:
                    parts = buffer.split(b'\r')
                    for part in parts[:-1]:
                        yield json.loads(part.decode('utf-8'))
                    buffer = parts[-1]
                except json.JSONDecodeError:
                    continue

    def close(self):
        if self.sock:
            self.sock.close()
            print("[NeuroSkyClient] Conexión cerrada")