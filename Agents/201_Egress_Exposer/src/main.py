#!/usr/bin/env python3
import socket
import sys
import os

def check_egress(destination_host):
    print(f"[*] [Agent 188] Egress-Exposer: Testing outbound paths to {destination_host}")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    loot_path = os.path.join(base_dir, "loot", "egress_results.txt")
    
    # Common C2 and exfiltration ports
    ports = [21, 22, 53, 80, 443, 8080, 8443, 5353]
    allowed_ports = []

    for port in ports:
        try:
            # Set a short timeout so we don't hang on dropped packets
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((destination_host, port))
            
            if result == 0:
                print(f"[+] PORT {port}: OPEN (Egress Allowed)")
                allowed_ports.append(str(port))
            else:
                print(f"[-] PORT {port}: CLOSED/FILTERED")
            sock.close()
        except Exception as e:
            print(f"[!] Error testing port {port}: {e}")

    # Write findings to loot
    with open(loot_path, "w") as f:
        f.write(f"Target: {destination_host}\n")
        f.write(f"Allowed Egress Ports: {', '.join(allowed_ports)}\n")
    
    print(f"[*] Results saved to {loot_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Defaulting to a common public DNS or the user's provided listener
        print("Usage: python3 main.py <callback_host>")
        print("Example: python3 main.py 8.8.8.8")
        sys.exit(1)
    
    check_egress(sys.argv[1])
