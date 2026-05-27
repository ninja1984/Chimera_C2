import sys; sys.path.append('/home/dan/Chimera_Project')
import os
import sys
import socket
import threading
import logging

# GPS Line
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from core.db_handler import ChimeraDB

class Shadow_Socks_Proxy:
    def __init__(self, host='0.0.0.0', port=1080):
        self.agent_id = "96"
        self.name = "96_Shadow_Socks_Proxy"
        self.db = ChimeraDB()
        self.host, self.port = host, port

    def handle_client(self, connection):
        try:
            if connection.recv(1) != b'\x05': return
            nmethods = connection.recv(1)
            connection.recv(ord(nmethods))
            connection.sendall(b'\x05\x00')
            version, cmd, _, address_type = connection.recv(4)
            if address_type == 1: address = socket.inet_ntoa(connection.recv(4))
            elif address_type == 3: address = connection.recv(ord(connection.recv(1))).decode()
            port = int.from_bytes(connection.recv(2), 'big')
            remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remote.connect((address, port))
            connection.sendall(b'\x05\x00\x00\x01' + socket.inet_aton('0.0.0.0') + (0).to_bytes(2, 'big'))
            self.bridge(connection, remote)
        except: connection.close()

    def bridge(self, client, remote):
        def forward(src, dst):
            try:
                while True:
                    data = src.recv(4096)
                    if not data: break
                    dst.sendall(data)
            except: pass
            finally: src.close(); dst.close()
        threading.Thread(target=forward, args=(client, remote)).start()
        threading.Thread(target=forward, args=(remote, client)).start()

    def run(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(self.name)
        self.db.heartbeat(self.name)
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen(5)
        print(f"[*] Proxy Active on {self.port}")
        try:
            while True:
                c, _ = server.accept()
                threading.Thread(target=self.handle_client, args=(c,)).start()
        except: server.close(); self.db.close()

if __name__ == "__main__":
    agent = Shadow_Socks_Proxy()
    agent.run()
