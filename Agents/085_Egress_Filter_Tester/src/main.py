#!/usr/bin/env python3
import socket
import sys
import os

def test_egress(callback_host):
    print(f"[*] [Agent 78] Egress-Filter-Tester: Probing outbound reachability to {callback_host}")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    loot_path = os.path.join(base_dir, "loot", "egress_report.txt")
    
    # Common ports used for exfiltration or command & control
    target_ports = [21, 22, 53, 80, 443, 8443, 8080, 5353]
    open_ports = []

    for port in target_ports:
        try:
            # Attempt a 1-second timeout connection
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.5)
            result = s.connect_ex((callback_host, port))
            
            if result == 0:
                msg = f"[!] ALLOWED: Outbound traffic on Port {port}"
                print(msg)
                open_ports.append(msg)
            else:
                print(f"[-] BLOCKED: Port {port}")
            s.close()
        except Exception:
            continue

    with open(loot_path, "w") as f:
        f.write(f"Callback Host: {callback_host}\n")
        f.write("--- Outbound Firewall Rules Audit ---\n")
        if open_ports:
            f.write("\n".join(open_ports))
        else:
            f.write("All tested outbound ports appear blocked (Strict Egress Filtering).")

    print(f"[*] Audit complete. Results saved to {loot_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <your_listener_ip_or_domain>")
        sys.exit(1)
    
    test_egress(sys.argv[1])
