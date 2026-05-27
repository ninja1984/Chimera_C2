#!/home/dan/Chimera_Project/venv/bin/python3
import socket
import select
import sys
import os

class PivotingProxy:
    """
    Agent 302: Lateral Movement Bridge.
    Implements a lightweight SOCKS5 proxy to allow external tools 
    to tunnel into the internal network through this host.
    """
    def __init__(self, host='0.0.0.0', port=1080):
        self.host = host
        self.port = port

    def handle_client(self, client_sock):
        """Standard SOCKS5 Handshake & Request Handling."""
        # 1. Greeting
        greeting = client_sock.recv(2)
        if not greeting: return
        client_sock.sendall(b"\x05\x00") # Version 5, No Auth

        # 2. Request
        data = client_sock.recv(4)
        if not data: return
        mode = data[1] # 1 = Connect
        addr_type = data[3]

        if addr_type == 1: # IPv4
            addr = socket.inet_ntoa(client_sock.recv(4))
        elif addr_type == 3: # Domain Name
            length = client_sock.recv(1)[0]
            addr = client_sock.recv(length).decode()
        
        port = int.from_bytes(client_sock.recv(2), 'big')

        try:
            # Connect to the internal destination
            remote_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remote_sock.connect((addr, port))
            print(f"[*] Tunnel Established: {addr}:{port}")
            client_sock.sendall(b"\x05\x00\x00\x01" + socket.inet_aton('0.0.0.0') + (0).to_bytes(2, 'big'))
        except Exception as e:
            print(f"[!] Tunnel Failed: {e}")
            return

        # 3. Data Transfer (Pipe)
        self._pipe(client_sock, remote_sock)

    def _pipe(self, src, dst):
        """Bridges two sockets for bi-directional data flow."""
        while True:
            read_ready, _, _ = select.select([src, dst], [], [])
            if src in read_ready:
                data = src.recv(4096)
                if dst.send(data) <= 0: break
            if dst in read_ready:
                data = dst.recv(4096)
                if src.send(data) <= 0: break

    def execute(self):
        print(f"--- [AGENT 302: PIVOTING PROXY ACTIVE ON {self.port}] ---")
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(5)

        try:
            while True:
                client, addr = server.accept()
                # For high-fidelity, we'd use threading here. 
                # For this primitive, it handles one session at a time.
                self.handle_client(client)
        except KeyboardInterrupt:
            print("[*] Proxy Shutting Down.")

if __name__ == "__main__":
    p = int(sys.argv[1]) if len(sys.argv) > 1 else 1080
    PivotingProxy(port=p).execute()
