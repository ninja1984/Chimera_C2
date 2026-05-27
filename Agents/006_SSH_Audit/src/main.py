#!/home/dan/Chimera_Project/venv/bin/python3
import socket
import sys
import os
import json
from datetime import datetime

class SSHAuditor:
    """
    Agent 06: SSH Protocol & Algorithm Auditor.
    Extracts banners and performs a KEXINIT (Key Exchange Init) to identify 
    weak ciphers, MACs, and legacy algorithms that allow for decryption or MitM.
    """
    def __init__(self, target, port=22):
        self.target = target
        self.port = int(port)
        self.loot_dir = "/home/dan/Chimera_Project/agents/06_SSH_Audit/loot"
        os.makedirs(self.loot_dir, exist_ok=True)

    def grab_banner(self):
        """Standard banner grab to identify SSH version and underlying OS."""
        try:
            with socket.create_connection((self.target, self.port), timeout=5) as s:
                banner = s.recv(1024).decode().strip()
                print(f"[+] SSH BANNER IDENTIFIED: {banner}")
                return banner
        except Exception as e:
            print(f"[!] Banner Grab Failed: {e}")
            return None

    def audit_algorithms(self):
        """
        Connects and requests the KEXINIT packet to see what the server supports.
        Identifies 'Simplicity' flaws where the server trusts legacy, weak crypto.
        """
        print(f"[*] AGENT 06: Auditing KEX/Ciphers on {self.target}:{self.port}...")
        
        # Professional-grade 'Legacy/Weak' list for downgrade analysis
        weak_ciphers = ['arcfour', 'arcfour128', 'arcfour256', 'blowfish-cbc', '3des-cbc', 'aes128-cbc']
        weak_macs = ['hmac-md5', 'hmac-sha1-96', 'hmac-sha1']
        weak_kex = ['diffie-hellman-group1-sha1', 'diffie-hellman-group-exchange-sha1']

        try:
            with socket.create_connection((self.target, self.port), timeout=5) as s:
                s.recv(1024) # Skip the initial banner
                
                # Send a raw, minimal KEXINIT trigger. 
                # We aren't completing the handshake (Stealth). We just want the response.
                dummy_kex = b"\x00\x00\x00\x00\x14\x02" + b"\x00"*16 + b"\x00\x00\x00\x00"
                s.send(dummy_kex)
                
                # The server will reply with its supported algorithms
                raw_response = s.recv(4096)
                data_str = str(raw_response)
                
                findings = []
                for wc in weak_ciphers:
                    if wc in data_str: findings.append(f"WEAK_CIPHER: {wc}")
                for wm in weak_macs:
                    if wm in data_str: findings.append(f"WEAK_MAC: {wm}")
                for wk in weak_kex:
                    if wk in data_str: findings.append(f"WEAK_KEX: {wk}")

                return findings
        except Exception as e:
            return [f"Audit failed: {e}"]

    def execute(self):
        print(f"--- [AGENT 06: SSH SECURITY AUDIT - {self.target}] ---")
        banner = self.grab_banner()
        vulnerabilities = self.audit_algorithms()

        if vulnerabilities:
            for v in vulnerabilities:
                print(f"    [!] DETECTED: {v}")
            
            # Commit Intelligence to Loot
            loot_path = f"{self.loot_dir}/ssh_{self.target}.json"
            with open(loot_path, 'w') as f:
                json.dump({
                    "timestamp": str(datetime.now()),
                    "target": self.target,
                    "banner": banner, 
                    "weaknesses": vulnerabilities
                }, f, indent=4)
            print(f"[!!!] INTELLIGENCE COMMITTED: {loot_path}")
        else:
            print("[+] No legacy/weak algorithms identified in initial pass.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./main.py <target_ip> [port]")
        sys.exit(1)
    
    target = sys.argv[1]
    port = sys.argv[2] if len(sys.argv) > 2 else 22
    SSHAuditor(target, port).execute()
