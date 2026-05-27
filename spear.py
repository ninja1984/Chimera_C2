#!/usr/bin/env python3
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2.0)
try:
    s.connect(("127.0.0.1", 2222))
    s.sendall(b"CHIMERA_WAKE")
    s.close()
    print("[+] Spear delivered.")
except:
    print("[!] Target offline.")
