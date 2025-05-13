import socket
import json

class NeuroSkyClient:
    def __init__(self, host='127.0.0.1', port=13854):
        self.host = host
        self.port = port
        self.sock = None

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        config = {
            "enableRawOutput": True,
            "format": "Json"
        }
        self.sock.sendall(json.dumps(config).encode('utf-8'))
        print(" Conectado a NeuroSky")

    def read_data(self):
        try:
            data = self.sock.recv(2048).decode('utf-8')
            for line in data.split('\r'):
                if line.strip():
                    return json.loads(line)
        except (json.JSONDecodeError, UnicodeDecodeError):
            print("[ERROR] Lectura de datos fallida: JSON inválido o incompleto")
        except Exception as e:
            print(f"[ERROR] Desconocido al leer datos: {e}")
        return {}

    def close(self):
        if self.sock:
            self.sock.close()
            print(" Conexión cerrada.")
