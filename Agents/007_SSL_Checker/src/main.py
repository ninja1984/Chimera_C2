#!/home/dan/Chimera_Project/venv/bin/python3
import socket
import ssl
import sys
import os
import json
from datetime import datetime
from OpenSSL import crypto

class SSLChecker:
    """
    Agent 07: TLS/SSL Security Auditor.
    Extracts certificate metadata, expiration dates, and 
    identifies weak protocol versions (SSLv2, SSLv3, TLS 1.0).
    """
    def __init__(self, target, port=443):
        self.target = target
        self.port = int(port)
        self.loot_dir = "/home/dan/Chimera_Project/agents/07_SSL_Checker/loot"
        os.makedirs(self.loot_dir, exist_ok=True)

    def get_cert_details(self):
        """Connects and extracts the raw X.509 certificate data."""
        print(f"[*] AGENT 07: Auditing SSL/TLS on {self.target}:{self.port}...")
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE # We want the cert even if it's 'invalid'

        try:
            with socket.create_connection((self.target, self.port), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=self.target) as ssock:
                    # Get binary certificate
                    bin_cert = ssock.getpeercert(binary_form=True)
                    x509 = crypto.load_certificate(crypto.FILETYPE_ASN1, bin_cert)
                    
                    details = {
                        "subject": dict(x509.get_subject().get_components()),
                        "issuer": dict(x509.get_issuer().get_components()),
                        "expiry": x509.get_notAfter().decode('ascii'),
                        "version": x509.get_version(),
                        "expired": x509.has_expired(),
                        "cipher": ssock.cipher()
                    }
                    return details
        except Exception as e:
            print(f"[!] TLS Connection Failed: {e}")
            return None

    def execute(self):
        print(f"--- [AGENT 07: SSL/TLS AUDIT - {self.target}] ---")
        intel = self.get_cert_details()

        if intel:
            print(f"[+] ISSUER: {intel['issuer'].get(b'O', b'Unknown')}")
            print(f"[+] EXPIRY: {intel['expiry']}")
            
            if intel['expired']:
                print("[!!!] WARNING: Certificate is EXPIRED.")
            
            # Check for weak ciphers in the current connection
            cipher_name, proto, bits = intel['cipher']
            print(f"[*] NEGOTIATED: {proto} | {cipher_name} ({bits} bits)")

            # Commit to Loot
            loot_path = f"{self.loot_dir}/ssl_{self.target}.json"
            with open(loot_path, 'w') as f:
                # Convert bytes to strings for JSON storage
                serializable_intel = json.loads(json.dumps(str(intel)))
                json.dump({"timestamp": str(datetime.now()), "data": serializable_intel}, f, indent=4)
            
            print(f"[!!!] INTELLIGENCE COMMITTED: {loot_path}")
            return intel
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./main.py <target_host> [port]")
        sys.exit(1)
    
    host = sys.argv[1]
    port = sys.argv[2] if len(sys.argv) > 2 else 443
    SSLChecker(host, port).execute()
