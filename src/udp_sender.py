import socket
import json

class UDPSender:
    def _init_(self, ip='127.0.0.1', port=5005):
        self.address = (ip, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, data):
        try:
            json_data = json.dumps(data)
            self.sock.sendto(json_data.encode('utf-8'), self.address)
        except Exception as e:
            print(f"[ERROR] UDP Send Failed: {e}")