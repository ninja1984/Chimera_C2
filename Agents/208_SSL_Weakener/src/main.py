#!/usr/bin/env python3
import ssl
import socket
import sys
import os
from datetime import datetime

def audit_ssl(target_host, port=443):
    print(f"[*] [Agent 195] SSL-Weakener: Auditing {target_host}:{port}")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    loot_path = os.path.join(base_dir, "loot", "ssl_audit.txt")
    
    if not os.path.exists(os.path.join(base_dir, "loot")):
        os.makedirs(os.path.join(base_dir, "loot"))

    context = ssl.create_default_context()
    try:
        with socket.create_connection((target_host, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=target_host) as ssock:
                cert = ssock.getpeercert()
                cipher = ssock.cipher()
                
                print(f"[+] Protocol: {ssock.version()}")
                print(f"[+] Cipher: {cipher[0]} ({cipher[2]} bits)")
                
                expiry_str = cert['notAfter']
                # Strip 'GMT' for cleaner parsing
                clean_date = expiry_str.replace(' GMT', '').strip()
                
                try:
                    # Standard OpenSSL format: %b %d %H:%M:%S %Y
                    expiry_date = datetime.strptime(clean_date, "%b %d %H:%M:%S %Y")
                    remaining = expiry_date - datetime.now()
                    print(f"[+] Certificate expires in: {remaining.days} days")
                except ValueError:
                    print(f"[!] Date Parse Warning - Raw: {expiry_str}")

                with open(loot_path, "w") as f:
                    f.write(f"Host: {target_host}\nProtocol: {ssock.version()}\nCipher: {cipher[0]}\nExpiry: {expiry_str}\n")

    except Exception as e:
        print(f"[!] Connection failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <target_host>")
        sys.exit(1)
    
    audit_ssl(sys.argv[1])
