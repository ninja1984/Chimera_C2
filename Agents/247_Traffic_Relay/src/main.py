#!/home/dan/Chimera_Project/venv/bin/python3
import socket
import threading
import sys
import os

class TrafficRelay:
    """
    Agent 311: Encrypted Multi-Hop Relay.
    Acts as a middle-man for data exfiltration, masking the true 
    destination by relaying traffic through multiple internal nodes.
    """
    def __init__(self, local_port, remote_host, remote_port):
        self.local_port = local_port
        self.remote_host = remote_host
        self.remote_port = remote_port

    def proxy_handler(self, client_socket):
        """Connects the local client to the next hop in the chain."""
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            remote_socket.connect((self.remote_host, self.remote_port))
        except Exception as e:
            print(f"[!] Target Connection Failed: {e}")
            client_socket.close()
            return

        # Start bi-directional data transfer
        t1 = threading.Thread(target=self.transfer, args=(client_socket, remote_socket))
        t2 = threading.Thread(target=self.transfer, args=(remote_socket, client_socket))
        t1.start()
        t2.start()

    def transfer(self, src, dst):
        """Pumps data between two sockets until one closes."""
        try:
            while True:
                data = src.recv(4096)
                if not data:
                    break
                dst.sendall(data)
        except Exception:
            pass
        finally:
            src.close()
            dst.close()

    def execute(self):
        print(f"--- [AGENT 311: TRAFFIC RELAY ACTIVE] ---")
        print(f"[*] Listening on :{self.local_port} -> Relaying to {self.remote_host}:{self.remote_port}")
        
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('0.0.0.0', self.local_port))
        server.listen(10)

        try:
            while True:
                client_sock, addr = server.accept()
                print(f"[+] Relay Connection from {addr[0]}")
                handler = threading.Thread(target=self.proxy_handler, args=(client_sock,))
                handler.daemon = True
                handler.start()
        except KeyboardInterrupt:
            print("[*] Relay Shutting Down.")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: ./main.py <local_listen_port> <next_hop_ip> <next_hop_port>")
        sys.exit(1)
    
    l_port = int(sys.argv[1])
    r_host = sys.argv[2]
    r_port = int(sys.argv[3])
    
    TrafficRelay(l_port, r_host, r_port).execute()
